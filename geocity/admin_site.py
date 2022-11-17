from django.contrib.admin import AdminSite, site


# TODO: delete ?
class PermitsAdminSite(AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry.update(site._registry)
