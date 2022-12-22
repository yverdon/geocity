from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group, Permission, User
from django.contrib.sites.admin import SiteAdmin as BaseSiteAdmin
from django.contrib.sites.models import Site
from django.contrib.staticfiles import finders
from django.core.files import File
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from knox.models import AuthToken

from geocity.apps.accounts.models import AdministrativeEntity, UserProfile
from geocity.apps.reports.models import (
    Report,
    ReportLayout,
    SectionAuthor,
    SectionMap,
    SectionParagraph,
)
from geocity.apps.submissions.models import Submission, SubmissionWorkflowStatus
from geocity.fields import GeometryWidget

from . import models, permissions_groups
from .users import get_integrator_permissions, get_users_list_for_integrator_admin

MULTIPLE_INTEGRATOR_ERROR_MESSAGE = _(
    "Un utilisateur ne peut être membre que d'un seul groupe 'Intégrateur'"
)
SELF_REMOVE_INTEGRATOR_ERROR_MESSAGE = _(
    "Un groupe 'Intégrateur' ne peut être retiré. Veuillez contacter un administrateur"
)

# Allow a user belonging to integrator group to see only objects created by this group
def filter_for_user(user, qs):
    if not user.is_superuser:
        qs = qs.filter(
            integrator__in=user.groups.filter(
                permit_department__is_integrator_admin=True
            )
        )
    return qs


def get_integrator_readonly_fields(user):
    if user.is_superuser:
        return []
    else:
        return ["integrator"]


class IntegratorFilterMixin:
    def save_model(self, request, obj, form, change):
        user = request.user
        if not user.is_superuser:
            obj.integrator = user.groups.get(
                permit_department__is_integrator_admin=True
            )
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        return get_integrator_readonly_fields(user)

    def get_queryset(self, request):
        user = request.user
        return filter_for_user(user, super().get_queryset(request))


class UserAdminForm(UserChangeForm):
    def clean_groups(self):
        groups = self.cleaned_data["groups"]

        edited_user_integrator_groups = groups.filter(
            permit_department__is_integrator_admin=True
        )

        if len(edited_user_integrator_groups) > 1:
            raise forms.ValidationError(MULTIPLE_INTEGRATOR_ERROR_MESSAGE)
        return groups


class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "is_sociallogin",
                )
            },
        ),
        (
            _("Groupes et Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Dates importantes"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_sociallogin",
        "last_login",
        "date_joined",
    )

    def has_add_permission(self, request):
        return False

    @admin.display(boolean=True)
    def is_sociallogin(self, obj):
        return obj.socialaccount_set.exists()

    is_sociallogin.admin_order_field = "socialaccount"
    is_sociallogin.short_description = "Social"

    change_form_template = "accounts/admin/user_change.html"

    def get_readonly_fields(self, request, obj=None):
        # limit editable fields to protect user data, superuser creation must be done using django shell
        if request.user.is_superuser:
            return [
                "is_superuser",
                "is_sociallogin",
            ]
        else:
            return [
                "email",
                "username",
                "user_permissions",
                "is_superuser",
                "is_sociallogin",
                "is_staff",
                "last_login",
                "date_joined",
            ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        user_being_updated = User.objects.get(
            id=(int(request.resolver_match.kwargs["object_id"]))
        )
        userprofile_being_updated = UserProfile.objects.get(user=user_being_updated)

        if db_field.name == "groups":
            if request.user.is_superuser:
                kwargs["queryset"] = Group.objects.all()
            else:
                kwargs["queryset"] = Group.objects.filter(
                    permit_department__integrator=request.user.groups.get(
                        permit_department__is_integrator_admin=True
                    ).pk,
                )

            # Do not allow anonymous user to be set in groups!!!
            if userprofile_being_updated.is_anonymous:
                kwargs["queryset"] = Group.objects.none()

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # Filter users that can be seen by integrator
    def get_queryset(self, request):
        return get_users_list_for_integrator_admin(request.user)

    def save_model(self, req, obj, form, change):
        """Set 'is_staff=True' when the saved user is in a integrator group.
        But let is_staff=True for super users.
        """
        if req.user.is_superuser:
            obj.is_staff = False if not obj.is_superuser else True
            for group in form.cleaned_data["groups"]:
                if group.permit_department.is_integrator_admin:
                    obj.is_staff = True
        # Prevent integrator from removing groups he hasn't access
        else:
            # Groups before editing the user
            groups_before = Group.objects.filter(user=obj.pk)

            # Groups the integrator has access to
            editable_groups = Group.objects.filter(
                permit_department__integrator=req.user.groups.get(
                    permit_department__is_integrator_admin=True
                ).pk,
            ).values("pk")

            # Groups assigned to the user and integrator hasn't access to (= groups before - editable groups)
            non_editable_groups = groups_before.exclude(pk__in=editable_groups)

            # Groups to keep on user (= groups the integrator has selected + groups the integrator hasn't access to)
            groups_to_keep = form.cleaned_data["groups"].union(non_editable_groups)

            # Edit cleaned_data to save the groups
            form.cleaned_data["groups"] = groups_to_keep

    def get_urls(self):
        urls = super().get_urls()

        return [
            path(
                "<int:user_id>/create-token/",
                self.admin_site.admin_view(self.create_auth_token),
                name="create_auth_token",
            )
        ] + urls

    def create_auth_token(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        # TODO: Define when a token needs to be deleted
        with transaction.atomic():
            authtoken, token = AuthToken.objects.create(user, expiry=None)

        messages.add_message(
            request,
            messages.SUCCESS,
            _(
                "Jeton créé avec succès. Veuillez le copier, il ne sera visible qu'une seule fois."
            ),
        )
        messages.add_message(request, messages.INFO, token)

        return redirect(
            reverse(
                "admin:auth_user_change",
                kwargs={"object_id": user_id},
            )
        )


class DepartmentAdminForm(forms.ModelForm):
    class Meta:
        model = models.PermitDepartment
        fields = [
            "description",
            "administrative_entity",
            "is_validator",
            "is_default_validator",
            "is_backoffice",
            "is_integrator_admin",
            "mandatory_2fa",
            "integrator_email_domains",
            "integrator_emails_exceptions",
            "integrator",
        ]

    # If the group is updated to be integrator, the users in this group should not be in another integrator group
    # If the group is updated to be integrator, the administrative_entity will be None. The integrator will create entities, so they don't exist yet
    def clean(self):
        group = self.cleaned_data["group"]

        # Integrator users don't have the field "is_integrator_admin" while creating a group
        if "is_integrator_admin" in self.cleaned_data:
            is_integrator_admin = self.cleaned_data["is_integrator_admin"]
        else:
            is_integrator_admin = False

        # Check only if the group passed from not integrator to integrator and has a user_set
        try:
            if (
                self.instance
                and not self.instance.is_integrator_admin
                and is_integrator_admin
                and group.user_set
            ):
                user_with_integrator_group = (
                    Group.objects.exclude(pk=group.pk)
                    .filter(
                        user__in=group.user_set.all(),
                        permit_department__is_integrator_admin=True,
                    )
                    .exists()
                )
                # Raise error if this group is integrator and user(s) is/are already in integrator group and this group
                if user_with_integrator_group:
                    raise forms.ValidationError(
                        {"is_integrator_admin": MULTIPLE_INTEGRATOR_ERROR_MESSAGE}
                    )
        except ValueError:
            # Upon creation of the group, there is no id, therefore no user_set
            pass

        # Raise error if group is not integrator and has no administrative_entity
        if (
            not is_integrator_admin
            and self.instance.is_integrator_admin
            and not self.cleaned_data["administrative_entity"]
        ):
            raise forms.ValidationError(
                {
                    "administrative_entity": _(
                        "Un groupe non intégrateur doit avoir une entité administrative"
                    )
                }
            )

        return self.cleaned_data


# Inline for group & department (1to1)
class PermitDepartmentInline(admin.StackedInline):
    model = models.PermitDepartment
    can_delete = False
    verbose_name_plural = "Service"
    inline_classes = ("collapse open",)
    form = DepartmentAdminForm
    min_num = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "administrative_entity":
            if request.user.is_superuser:
                kwargs["queryset"] = models.AdministrativeEntity.objects.all()
            else:
                kwargs["queryset"] = models.AdministrativeEntity.objects.filter(
                    integrator=request.user.groups.get(
                        permit_department__is_integrator_admin=True
                    )
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return [
                "integrator",
                "is_integrator_admin",
                "integrator_email_domains",
                "integrator_emails_exceptions",
            ]


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        help_texts = {
            "permissions": _(
                "Pour un rôle intégrateur, ajoutez toutes les permissions disponibles"
            ),
        }

    def clean_permissions(self):
        permissions = self.cleaned_data["permissions"]
        integrator_permissions = get_integrator_permissions()

        if "permit_department-0-is_integrator_admin" in self.data.keys():
            permissions = permissions.union(integrator_permissions)
        else:
            permissions = permissions.difference(
                integrator_permissions.exclude(
                    codename__in=permissions_groups.AVAILABLE_FOR_INTEGRATOR_PERMISSION_CODENAMES
                )
            )
        return permissions


class UserInline(admin.TabularInline):
    model = Group.user_set.through
    can_delete = False
    extra = 0
    verbose_name = _("Utilisateur membre du groupe")
    verbose_name_plural = _("Utilisateurs membres du groupe")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = get_users_list_for_integrator_admin(request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class GroupAdmin(admin.ModelAdmin):
    inlines = (PermitDepartmentInline, UserInline)
    form = GroupAdminForm
    list_display = [
        "__str__",
        "get__integrator",
        "get__is_validator",
        "get__is_default_validator",
        "get__is_backoffice",
        "get__mandatory_2fa",
    ]

    filter_horizontal = ("permissions",)
    search_fields = [
        "name",
    ]

    @admin.display(boolean=True)
    def get__is_validator(self, obj):
        return obj.permit_department.is_validator

    get__is_validator.admin_order_field = "permit_department__is_validator"
    get__is_validator.short_description = _("Validateur")

    @admin.display(boolean=True)
    def get__is_default_validator(self, obj):
        return obj.permit_department.is_default_validator

    get__is_default_validator.admin_order_field = (
        "permit_department__is_default_validator"
    )
    get__is_default_validator.short_description = _("Validateur par défaut")

    @admin.display(boolean=True)
    def get__is_backoffice(self, obj):
        return obj.permit_department.is_backoffice

    get__is_backoffice.admin_order_field = "permit_department__is_backoffice"
    get__is_backoffice.short_description = _("Secrétariat")

    def get__integrator(self, obj):
        return Group.objects.get(pk=obj.permit_department.integrator)

    get__integrator.admin_order_field = "permit_department__integrator"
    get__integrator.short_description = _("Groupe des administrateurs")

    @admin.display(boolean=True)
    def get__mandatory_2fa(self, obj):
        return obj.permit_department.mandatory_2fa

    get__mandatory_2fa.admin_order_field = "permit_department__mandatory_2fa"
    get__mandatory_2fa.short_description = _("2FA obligatoire")

    def get_queryset(self, request):

        if request.user.is_superuser:
            qs = Group.objects.all()
        else:
            qs = Group.objects.filter(
                Q(
                    permit_department__integrator=request.user.groups.get(
                        permit_department__is_integrator_admin=True
                    ).pk
                )
            ).exclude(permit_department__is_integrator_admin=True)
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.permit_department.integrator = request.user.groups.get(
                permit_department__is_integrator_admin=True
            ).pk
        super().save_model(request, obj, form, change)
        obj.permit_department.save()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # permissions that integrator role can grant to group
        if db_field.name == "permissions":

            if (
                not request.user.is_superuser
                and request.user.groups.get(
                    permit_department__is_integrator_admin=True
                ).pk
            ):
                integrator_permissions = Permission.objects.filter(
                    codename__in=permissions_groups.AVAILABLE_FOR_INTEGRATOR_PERMISSION_CODENAMES
                )
                kwargs["queryset"] = integrator_permissions

        return super().formfield_for_manytomany(db_field, request, **kwargs)


class SiteWithAdministrativeEntitiesField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.domain})"


def get_sites_field(user):
    qs = models.Site.objects.all()
    if not user.is_superuser:
        qs = qs.filter(
            Q(
                site_profile__integrator__in=user.groups.filter(
                    permit_department__is_integrator_admin=True
                )
            )
            | Q(domain=settings.DEFAULT_SITE)
        )

    return SiteWithAdministrativeEntitiesField(
        queryset=qs,
        widget=forms.CheckboxSelectMultiple,
        label=_("Sites").capitalize(),
    )


class AdministrativeEntityAdminForm(forms.ModelForm):
    """Form class to configure an administrative entity (commune, organisation)"""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["sites"] = get_sites_field(user)

    class Meta:
        model = models.AdministrativeEntityForAdminSite
        fields = [
            "name",
            "tags",
            "ofs_id",
            "sites",
            "expeditor_email",
            "expeditor_name",
            "custom_signature",
            "link",
            "archive_link",
            "general_informations",
            "phone",
            "additional_searchtext_for_address_field",
            "geom",
            "integrator",
        ]
        exclude = ["enabled_status"]
        widgets = {
            "geom": GeometryWidget(
                attrs={
                    "options": {
                        "map_width": "100%",
                        "map_height": 400,
                        "default_center": [2539057, 1181111],
                        "default_zoom": 10,
                        "display_raw": False,
                        "edit_geom": True,
                        "min_zoom": 5,
                        "wmts_capabilities_url": settings.WMTS_GETCAP,
                        "wmts_layer": settings.WMTS_LAYER,
                        "wmts_capabilities_url_alternative": settings.WMTS_GETCAP_ALTERNATIVE,
                        "wmts_layer_alternative": settings.WMTS_LAYER_ALTERNATIVE,
                        "restriction_area_enabled": False,
                        "geometry_db_type": "MultiPolygon",
                        "wms_layers": [],
                    },
                }
            ),
            "is_public": forms.RadioSelect(
                choices=models.PUBLIC_TYPE_CHOICES,
            ),
        }

    class Media:
        js = ("https://code.jquery.com/jquery-3.5.1.slim.min.js",)
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css",
                "css/admin.css",
            )
        }


class SubmissionWorkflowStatusInline(admin.TabularInline):
    model = SubmissionWorkflowStatus
    extra = 0
    verbose_name = _("Étape - ")
    verbose_name_plural = _("Flux (complet par défaut)")


@admin.register(models.AdministrativeEntityForAdminSite)
class AdministrativeEntityAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    # Pass the user from ModelAdmin to ModelForm
    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm

    change_form_template = "accounts/admin/administrative_entity_change.html"
    form = AdministrativeEntityAdminForm
    inlines = [
        SubmissionWorkflowStatusInline,
    ]
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    list_display = [
        "sortable_str",
        "expeditor_name",
        "expeditor_email",
        "ofs_id",
        "get_tags",
        "get_sites",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = "Entité administrative"

    def get_sites(self, obj):
        return [site["name"] for site in obj.sites.all().values("name")]

    get_sites.short_description = _("Sites")
    get_sites.admin_order_field = "sites__name"

    def get_tags(self, obj):
        return [tag["name"] for tag in obj.tags.all().values("name")]

    get_tags.short_description = _("Mots-clés")
    get_tags.admin_order_field = "tags__name"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "integrator":
            kwargs["queryset"] = Group.objects.filter(
                permit_department__is_integrator_admin=True,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):

        if not request.user.is_superuser:
            obj.integrator = request.user.groups.get(
                permit_department__is_integrator_admin=True
            )
        obj.save()
        has_workflow_status = SubmissionWorkflowStatus.objects.filter(
            administrative_entity=obj
        ).exists()
        if not has_workflow_status:
            for key, value in Submission.STATUS_CHOICES:
                SubmissionWorkflowStatus.objects.create(
                    status=key,
                    administrative_entity=obj,
                )

    def get_urls(self):
        urls = super().get_urls()

        return [
            path(
                "<int:administrative_entity_id>/create-anonymous-user/",
                self.admin_site.admin_view(self.create_anonymous_user),
                name="create_administrative_entity_anonymous_user",
            ),
            path(
                "<int:administrative_entity_id>/create-default-report/",
                self.admin_site.admin_view(self.create_default_report),
                name="create_administrative_entity_default_report",
            ),
        ] + urls

    def create_anonymous_user(self, request, administrative_entity_id):
        administrative_entity = get_object_or_404(
            AdministrativeEntity, pk=administrative_entity_id
        )

        administrative_entity.create_anonymous_user()

        messages.add_message(
            request, messages.SUCCESS, _("Utilisateur anonyme créé avec succès.")
        )

        return redirect(
            reverse(
                "admin:forms_administrativeentityforadminsite_change",
                kwargs={"object_id": administrative_entity_id},
            )
        )

    def create_default_report(self, request, administrative_entity_id):
        administrative_entity = get_object_or_404(
            AdministrativeEntity, pk=administrative_entity_id
        )

        layout, created = ReportLayout.objects.get_or_create(
            name="default " + administrative_entity.name,
            margin_top=30,
            margin_right=10,
            margin_bottom=20,
            margin_left=22,
            integrator=administrative_entity.integrator,
        )

        _bg_path = finders.find("reports/report-letter-paper-template.png")
        background_image = open(_bg_path, "rb")
        layout.background.save(
            "report-letter-paper.png", File(background_image), save=True
        )
        layout.save()

        report, created = Report.objects.get_or_create(
            name="default " + administrative_entity.name,
            layout=layout,
            integrator=administrative_entity.integrator,
        )

        SectionParagraph.objects.get_or_create(
            order=1,
            report=report,
            title="Example report",
            content="<p>This is an example report. It could be an approval, or any type of report related to a request.</p>",
        )

        SectionParagraph.objects.get_or_create(
            order=2,
            report=report,
            title="Demand summary",
            content="<p>This demand contains the following objects.</p><ul>{% for form in request_data.properties.submission_forms_names.values() %}<li>{{form}}</li>{% endfor %}</ul>",
        )

        SectionParagraph.objects.get_or_create(
            order=3,
            report=report,
            title="Raw request data",
            content="<pre>{{request_data}}</pre>",
        )

        SectionParagraph.objects.get_or_create(
            order=4,
            report=report,
            title="Raw form data",
            content="<pre>{{form_data}}</pre>",
        )

        SectionMap.objects.get_or_create(
            order=5,
            report=report,
        )

        SectionAuthor.objects.get_or_create(
            order=6,
            report=report,
        )

        if request and created:
            messages.add_message(
                request, messages.SUCCESS, _("Rapport créé avec succès.")
            )
        elif request:
            messages.add_message(request, messages.INFO, _("Rapport déjà existant."))

        return redirect(
            reverse(
                "admin:forms_administrativeentityforadminsite_change",
                kwargs={"object_id": administrative_entity_id},
            )
        )


@admin.register(models.TemplateCustomization)
class TemplateCustomizationAdmin(admin.ModelAdmin):
    list_display = [
        "sortable_str",
        "application_title",
        "application_subtitle",
        "has_background_image",
    ]
    list_filter = [
        "templatename",
        "application_title",
    ]
    search_fields = [
        "templatename",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "templatename"
    sortable_str.short_description = _("Page de login")

    @admin.display(boolean=True)
    def has_background_image(self, obj):
        try:
            return obj.background_image.url is not None
        except ValueError:
            return False

    has_background_image.admin_order_field = "background_image"
    has_background_image.short_description = "Image de fond"


# Inline for base Django Site
class SiteInline(admin.TabularInline):
    model = models.SiteProfile
    inline_classes = ("collapse open",)


class SiteProfileAdmin(BaseSiteAdmin):
    inlines = (SiteInline,)
    list_display = [
        "name",
        "domain",
    ]


admin.site.unregister(Site)
admin.site.register(Site, SiteProfileAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
