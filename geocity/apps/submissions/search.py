import dataclasses
import datetime
import enum
import functools
import operator
import re
from typing import Optional

from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.contrib.postgres.lookups import Unaccent
from django.contrib.postgres.search import TrigramSimilarity
from django.db import connection
from django.db.models import (
    Case,
    CharField,
    Count,
    DateField,
    F,
    Q,
    TextField,
    Value,
    When,
)
from django.db.models.functions import Cast, Concat, Greatest
from django.db.models.lookups import PostgresOperatorLookup
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from geocity.apps.forms.models import Field

from . import models


class TrigramStrictWordSimilarity(TrigramSimilarity):
    function = "STRICT_WORD_SIMILARITY"


class TrigramStrictWordSimilar(PostgresOperatorLookup):
    lookup_name = "trigram_strict_word_similar"
    postgres_operator = "<<%%"


CharField.register_lookup(TrigramStrictWordSimilar)
TextField.register_lookup(TrigramStrictWordSimilar)


@dataclasses.dataclass
class PartialDate:
    day: int
    month: int


class MatchType(enum.Enum):
    AUTHOR = "author"
    FIELD = "field"
    CREATED_AT = "created_at"
    CONTACT = "contact"
    TIME = "time"


@dataclasses.dataclass
class SearchResult:
    submission_id: int
    submission_status: int
    submission_created_at: datetime.date
    author_name: str
    field_label: Optional[str]
    field_value: str
    score: float
    match_type: MatchType


def match_type_label(match_type):
    return {
        MatchType.AUTHOR: _("Auteur‧e"),
        MatchType.FIELD: _("Propriété"),
        MatchType.CREATED_AT: _("Date de création"),
        MatchType.CONTACT: _("Contact"),
        MatchType.TIME: _("Date"),
    }.get(match_type)


def extract_date(search_str):
    date_pattern = re.compile(r"(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?")
    date_match = date_pattern.search(search_str)
    if date_match:
        day, month, year = [int(val) if val else None for val in date_match.groups()]

        if year:
            return datetime.date(year, month, day)

        return PartialDate(month=month, day=day)

    return None


def date_to_filters(field_name, date_or_partial_date):
    """
    Transform a `PartialDate` or a `datetime.date` object into a dict suitable to use in
    a filter() method.
    """
    if isinstance(date_or_partial_date, datetime.date):
        return {
            f"{field_name}__date": date_or_partial_date,
        }

    return {
        f"{field_name}__day": date_or_partial_date.day,
        f"{field_name}__month": date_or_partial_date.month,
    }


def add_score(qs, fields, search_str):
    """
    Add a `score` column on the given queryset `qs`, with the greatest score among the
    given `fields` matched against `search_str` using a trigram match. The resulting
    querystring also has a `scored_field` field containing the name of the field with
    the greatest score.
    """
    field_names = [(field, f"{field.replace('__', '_')}_score") for field in fields]

    score_annotation = {
        score_field_name: TrigramStrictWordSimilarity(
            Unaccent(field_name), Unaccent(Value(search_str))
        )
        for field_name, score_field_name in field_names
    }
    score_case = [
        When(
            **{score_field_name: F("score")},
            then=Value(field_name),
        )
        for field_name, score_field_name in field_names
    ]

    trigram_filters = [
        Q(
            **{
                f"{field_name}__unaccent__trigram_strict_word_similar": Unaccent(
                    Value(search_str)
                )
            }
        )
        for field_name in fields
    ]

    return (
        qs.annotate(
            **score_annotation,
            score=Greatest(
                *[score_field_name for field_name, score_field_name in field_names]
            )
            if len(fields) > 1
            else F(field_names[0][1]),
            scored_field=Case(
                *score_case,
                default=Value(""),
                output_field=CharField(),
            ),
        )
        # Filtering using Postgresql’s similarity lookups seems to be faster than
        # computing all the scores and then filtering on them
        .filter(functools.reduce(operator.or_, trigram_filters)).order_by("-score")
    )


def search_contacts(search_str, submissions_qs, limit=None):
    contact_search_fields = [
        "contact_full_name",
        "contact__company_name",
        "contact__vat_number",
        "contact__email",
    ]

    fields_label = {
        "contact_full_name": _("Nom"),
        "contact__company_name": _("Entreprise"),
        "contact__vat_number": _("Num. TVA"),
        "contact__email": _("Courriel"),
    }

    qs = models.SubmissionContact.objects.filter(
        submission__in=submissions_qs
    ).annotate(
        author_full_name=Concat(
            "submission__author__first_name",
            Value(" "),
            "submission__author__last_name",
        ),
        contact_full_name=Concat(
            "contact__first_name", Value(" "), "contact__last_name"
        ),
    )

    qs = (
        add_score(
            qs,
            contact_search_fields,
            search_str,
        )
        .values(
            *contact_search_fields,
            "contact_full_name",
            "submission_id",
            "submission__status",
            "submission__created_at",
            "score",
            "scored_field",
        )
        .order_by("-score", "-submission__created_at")
    )

    if limit is not None:
        qs = qs[:limit]

    return [
        SearchResult(
            submission_id=result["submission_id"],
            submission_status=result["submission__status"],
            submission_created_at=result["submission__created_at"],
            author_name=result["author_full_name"],
            field_label=fields_label[result["scored_field"]],
            field_value=result[result["scored_field"]],
            score=result["score"],
            match_type=MatchType.CONTACT,
        )
        for result in qs
    ]


def search_fields(search_str, submissions_qs, limit=None):
    qs = (
        add_score(
            models.FieldValue.objects.filter(
                field__input_type__in=[
                    Field.INPUT_TYPE_ADDRESS,
                    Field.INPUT_TYPE_LIST_MULTIPLE,
                    Field.INPUT_TYPE_LIST_SINGLE,
                    Field.INPUT_TYPE_NUMBER,
                    Field.INPUT_TYPE_TEXT,
                    Field.INPUT_TYPE_REGEX,
                ],
                selected_form__submission__in=submissions_qs,
            ).annotate(
                txt_value=Cast(
                    KeyTextTransform("val", "value"), output_field=TextField()
                ),
            ),
            ["txt_value"],
            search_str,
        )
        .annotate(
            author_full_name=Concat(
                "selected_form__submission__author__first_name",
                Value(" "),
                "selected_form__submission__author__last_name",
            )
        )
        .values(
            "selected_form__submission_id",
            "selected_form__submission__status",
            "selected_form__submission__created_at",
            "author_full_name",
            "field__name",
            "txt_value",
            "score",
        )
        .order_by("-score", "-selected_form__submission__created_at")
    )

    if limit is not None:
        qs = qs[:limit]

    return [
        SearchResult(
            submission_id=result["selected_form__submission_id"],
            submission_status=result["selected_form__submission__status"],
            submission_created_at=result["selected_form__submission__created_at"],
            author_name=result["author_full_name"],
            field_label=result["property__name"],
            field_value=result["txt_value"],
            score=result["score"],
            match_type=MatchType.FIELD,
        )
        for result in qs
    ]


def search_authors(search_str, submissions_qs, limit=None):
    qs = submissions_qs.annotate(
        author_full_name=Concat(
            "author__first_name",
            Value(" "),
            "author__last_name",
        ),
    )

    qs = (
        add_score(
            qs,
            [
                "author_full_name",
            ],
            search_str,
        )
        .values("id", "status", "score", "author_full_name", "created_at")
        .order_by("-score", "-created_at")
    )

    if limit is not None:
        qs = qs[:limit]

    return [
        SearchResult(
            submission_id=result["id"],
            submission_status=result["status"],
            submission_created_at=result["created_at"],
            author_name=result["author_full_name"],
            field_label=None,
            field_value=result["author_full_name"],
            score=result["score"],
            match_type=MatchType.AUTHOR,
        )
        for result in qs
    ]


def search_submission_created_at(date_or_partial_date, submissions_qs, limit=None):
    qs = (
        submissions_qs.filter(**date_to_filters("created_at", date_or_partial_date))
        .annotate(
            author_full_name=Concat(
                "author__first_name",
                Value(" "),
                "author__last_name",
            ),
        )
        .values("id", "status", "author_full_name", "created_at")
        .order_by("-created_at")
    )

    if limit is not None:
        qs = qs[:limit]

    return [
        SearchResult(
            submission_id=result["id"],
            iosubsubmission_status=result["status"],
            submission_created_at=result["created_at"],
            author_name=result["author_full_name"],
            field_label=None,
            field_value=result["created_at"].strftime("%d.%m.%Y"),
            score=1,
            match_type=MatchType.CREATED_AT,
        )
        for result in qs
    ]


def search_geo_times(date_or_partial_date, submissions_qs, limit=None):
    def field_label(field):
        if field == "starts_at":
            return _("Date de début")
        elif field == "ends_at":
            return _("Date de fin")

        return ""

    start_date_filter = date_to_filters("starts_at", date_or_partial_date)
    end_date_filter = date_to_filters("ends_at", date_or_partial_date)

    qs = (
        models.SubmissionGeoTime.objects.filter(
            Q(**start_date_filter) | Q(**end_date_filter),
            permit_request__in=submissions_qs,
        )
        .annotate(
            matching_date=Case(
                When(
                    **start_date_filter,
                    then=F("starts_at__date"),
                ),
                default=F("ends_at__date"),
                output_field=DateField(),
            ),
            matching_date_field=Case(
                When(
                    **start_date_filter,
                    then=Value("starts_at"),
                ),
                default=Value("ends_at"),
                output_field=CharField(),
            ),
            author_full_name=Concat(
                "submission__author__first_name",
                Value(" "),
                "submission__author__last_name",
            ),
        )
        .values(
            "submission_id",
            "submission__status",
            "submission__created_at",
            "matching_date",
            "matching_date_field",
            "author_full_name",
        )
        .annotate(nb_per_submission=Count("submission_id"))
        .order_by("-submission__created_at")
    )

    if limit is not None:
        qs = qs[:limit]

    return [
        SearchResult(
            submission_id=result["submission_id"],
            submission_status=result["submission__status"],
            submission_created_at=result["submission__created_at"],
            author_name=result["author_full_name"],
            field_label=field_label(result["matching_date_field"]),
            field_value=result["matching_date"].strftime("%d.%m.%Y"),
            score=1,
            match_type=MatchType.TIME,
        )
        for result in qs
    ]


def search_submissions(search_str, limit, submissions_qs):
    search_date = extract_date(search_str)

    # The `pg_trgm.strict_word_similarity_threshold` setting is used by the
    # TrigramStrictWordSimilar operator
    with connection.cursor() as cursor:
        cursor.execute("SET pg_trgm.strict_word_similarity_threshold = 0.1", [])

    return list(
        sorted(
            search_contacts(search_str, limit=limit, submissions_qs=submissions_qs)
            + search_fields(search_str, limit=limit, submissions_qs=submissions_qs)
            + (
                search_submission_created_at(
                    search_date, limit=limit, submissions_qs=submissions_qs
                )
                if search_date
                else []
            )
            + search_authors(search_str, limit=limit, submissions_qs=submissions_qs)
            + (
                search_geo_times(
                    search_date, limit=limit, submissions_qs=submissions_qs
                )
                if search_date
                else []
            ),
            key=lambda result: result.score,
            reverse=True,
        )
    )


def search_result_to_json(result):
    return {
        "submission": {
            "id": result.submission_id,
            "url": reverse(
                "permits:submission_detail",
                kwargs={
                    "submission_id": result.submission_id,
                },
            ),
            "author": result.author_name,
            "status": result.submission_status,
            "createdAt": result.submission_created_at.strftime("%d.%m.%Y"),
        },
        "match": {
            "fieldLabel": result.field_label,
            "fieldValue": result.field_value,
            "score": result.score,
            "type": result.match_type.value,
            "typeLabel": match_type_label(result.match_type),
        },
    }
