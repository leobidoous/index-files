# coding=utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import UserModel
from user.forms import UserAdminCreationForm, UserForm


class UserAdmin(admin.ModelAdmin):
    # add_form = UserAdminCreationForm
    # add_fieldsets = (
    #     (None, {
    #         'fields': ('email', 'username', 'password1', 'password2')
    #     }),
    # )
    # form = UserForm
    # fieldsets = (
    #     (None, {
    #         'fields': ('username', 'email', 'password')
    #     }),
    #     (
    #         'Permissões', {
    #             'fields': (
    #                 'is_active', 'is_staff', 'is_superuser', 'groups',
    #                 'user_permissions'
    #             )
    #         }
    #     ),
    # )
    # list_display = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    pass


admin.site.register(UserModel, UserAdmin)
