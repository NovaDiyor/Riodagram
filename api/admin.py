from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'is_active']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_('Extra'), {'fields': ('status', 'number', 'img', 'bio', 'following', 'followers', 'publications', 'saved',
                                 'liked', 'site')}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(Chat)
admin.site.register(Stories)
admin.site.register(Comment)
admin.site.register(Posts)
admin.site.register(LikedPost)
admin.site.register(Follow)
admin.site.register(Image)
admin.site.register(Alp)
