"""This file is loaded from apps.py"""

from django.contrib.auth.models import Group
from django.contrib.staticfiles import finders
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver

from geocity.apps.submissions.models import ComplementaryDocumentType

from .models import Report, ReportLayout, SectionAuthor, SectionMap, SectionParagraph


@receiver(post_save, sender=Group)
def create_default_report_for_integrator(sender, instance, created, **kwargs):
    if not created:
        return

    integrator = instance

    # Create report setup
    layout = ReportLayout(
        name="demo_layout",
        margin_top=30,
        margin_right=10,
        margin_bottom=20,
        margin_left=22,
        integrator=integrator,
    )
    _bg_path = finders.find("reports/report-letter-paper-template.png")
    background_image = open(_bg_path, "rb")
    layout.background.save("report-letter-paper.png", File(background_image), save=True)
    layout.save()

    report = Report(
        name="demo_report",
        layout=layout,
        integrator=integrator,
    )
    report.save()

    section_paragraph_1 = SectionParagraph(
        order=1,
        report=report,
        title="Example report",
        content="<p>This is an example report. It could be an approval, or any type of report related to a request.</p>",
    )
    section_paragraph_1.save()

    section_paragraph_2 = SectionParagraph(
        order=2,
        report=report,
        title="Demand summary",
        content="<p>This demand contains the following objects.</p><ul>{% for form in request_data.properties.submission_forms_names.values() %}<li>{{form}}</li>{% endfor %}</ul>",
    )
    section_paragraph_2.save()

    section_paragraph_3 = SectionParagraph(
        order=3,
        report=report,
        title="Raw request data",
        content="<pre>{{request_data}}</pre>",
    )
    section_paragraph_3.save()

    section_paragraph_4 = SectionParagraph(
        order=4,
        report=report,
        title="Raw wot data",
        content="<pre>{{wot_data}}</pre>",
    )
    section_paragraph_4.save()

    section_map = SectionMap(
        order=5,
        report=report,
    )
    section_map.save()

    section_author = SectionAuthor(
        order=6,
        report=report,
    )
    section_author.save()

    # Assign the report to each document type
    for dt in ComplementaryDocumentType.objects.filter(parent__isnull=False):
        dt.reports.add(report)
