from django.contrib import admin

from bookworm.admin import bookworm_admin_site
from users.models import User


bookworm_admin_site.register(User)
