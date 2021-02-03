from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'email',
        'is_superuser',
    )


admin.site.unregister(Group)
