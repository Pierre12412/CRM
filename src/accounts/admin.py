from importlib._common import _

from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email',]
    list_display = ('email', 'first_name', 'last_name', 'is_staff','is_admin','user_type')
    list_filter = ('is_active','user_type')
    filter_horizontal = ()
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','user_type'),
        }),
    )
    def save_model(self, request, obj, form, change):
            if obj.user_type == 4:
                obj.is_staff = True
                obj.is_admin = True
                obj.save()
            else:
                obj.save()

admin.site.register(User, CustomUserAdmin)