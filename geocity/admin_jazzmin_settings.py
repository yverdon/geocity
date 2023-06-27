"""
Configuration of the admin site style and layout
All options: https://django-jazzmin.readthedocs.io/configuration/
"""

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Geocity",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Geocity",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Geocity",
    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "books/img/logo.png",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Bienvenue sur le site d'administration de Geocity",
    # Copyright on the footer
    "copyright": "Geocity",
    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    "search_model": ["auth.User", "auth.Group"],
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {
            "name": "Home",
            "url": "admin:index",
        },
        {
            "name": "Site",
            "url": "submissions:submission_select_administrative_entity",
        },
        # external url that opens in a new window (Permissions can be added)
        {
            "name": "Documentation",
            "url": "https://github.com/yverdon/geocity/wiki",
            "new_window": True,
        },
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [{"model": "auth.user"}],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "auth",
        "forms",
        "submissions",
        "reports",
        "accounts",
        "sites",
        "constance",
    ],
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "account.EmailAddress": "fas fa-envelope",
        "accounts.TemplateCustomization": "fas fa-home",
        "auth.Group": "fas fa-users",
        "auth.User": "fas fa-user",
        "auth": "fas fa-users-cog",
        "axes.AccessAttempt": "fas fa-user-shield",
        "axes.AccessLog": "fas fa-align-left",
        "constance.Config": "fas fa-cogs",
        "django_cron.CronJobLog": "fas fa-tasks",
        "forms.AdministrativeEntityForAdminSite": "fas fa-landmark",
        "forms.ContactTypeForAdminSite": "fas fa-address-card",
        "forms.PaymentSettings": "fas fa-shopping-cart",
        "forms.Price": "fas fa-coins",
        "forms.Field": "fas fa-list-ol",
        "forms.Form": "fas fa-book",
        "forms.FormCategory": "fas fa-object-ungroup",
        "forms.MapWidgetConfiguration": "fa fa-map",
        "knox.AuthToken": "fas fa-user-secret",
        "reports.Report": "fas fa-print",
        "reports.ReportLayout": "fas fa-file-alt",
        "sites.Site": "fas fa-sitemap",
        "reports.ComplementaryDocumentTypeForAdminSite": "fas fa-copy",
        "submissions.Submission": "fas fa-search",
        "submissions.SubmissionAmendField": "fas fa-list-alt",
        "submissions.SubmissionInquiry": "fas fa-calendar",
        "taggit.Tag": "fas fa-bookmark",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": False,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "single",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "forms.form": "horizontal_tabs",
        "forms.administrativeentityforadminsite": "horizontal_tabs",
        "reports.report": "horizontal_tabs",
    },
    # Add a language dropdown into the admin
    "language_chooser": False,
}
