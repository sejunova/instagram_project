from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from member.forms import SignUpForm


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('img_profile', 'age', 'like_posts', 'user_type', 'nickname')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {'fields': ('img_profile', 'age', 'nickname')}),
    )
    add_form = SignUpForm



User = get_user_model()
admin.site.register(User, UserAdmin)
