from django.contrib import admin
from users.models import Users
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm

class UserAdminConfig(UserAdmin):
    model = Users
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    search_fields = ('user_name','user_email')
    list_filter = ('user_name','is_active','is_staff' )
    list_display = ('user_name', 'is_active','is_staff' )
    fieldsets = (
        (None, {'fields': ('user_name','password','user_email')}),
        ('Permissions', {'fields': ('is_active','is_staff')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name','user_email','password', 'is_active', 'is_staff')}
         ),
    )
    ordering = ('user_name','user_email')


admin.site.register(Users, UserAdminConfig)