from django.contrib import admin
from django.http import Http404


class CustomAdminSite(admin.AdminSite):
    def has_permission(self, request):
        user = request.user
        return user.is_active and (user.is_superuser or user.is_admin)

    def login(self, request, extra_context=None):
        if not self.has_permission(request):
            raise Http404()
        return super().login(request, extra_context)


bookworm_admin_site = CustomAdminSite(name="BookwormAdmin")
