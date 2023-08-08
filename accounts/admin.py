from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile


# @admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'username', 'phone_number', 'role',
                    'is_admin', 'is_staff', 'is_superadmin', 'is_active', 'is_deleted',
                    'created_at', 'updated_at')
    list_per_page = 10
    list_editable = ('first_name', 'last_name',)
    search_fields = ('email', 'username')
    date_hierarchy = 'created_at'
    readonly_fields = ('id', 'is_superadmin', 'created_at', 'updated_at', 'date_joined', 'last_login')
    ordering = ('-date_joined',)
    list_display_links = ('email', 'username')
    filter_horizontal = ('groups', 'user_permissions')  # must be a many-to-many field
    list_filter = ('is_active', 'is_deleted')
    fieldsets = (
        ('Protected', {
            'fields': ('id', 'is_superadmin', 'created_at', 'updated_at')
        }),
        ('Personal Information', {
            'fields': ('email', 'first_name', 'last_name', 'username')
        }),
        ('Permissions & Key Flags', {
            'fields': ('is_admin', 'is_staff', 'is_active', 'is_deleted')
        }),
        ('Group Permission', {
            'fields': ('groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        })
    )


admin.site.register(User, CustomUserAdmin)        # IF REMOVE THIS, MUST ADD DECORATOR @admin.register(User)


class UserProfileAdminView(admin.ModelAdmin):
    list_display = ('id', 'auto_id', 'user', 'address_line_1', 'address_line_2', 'address_line_3',
                    'country', 'state', 'district', 'zip_code',
                    'creator', 'updater', 'created_at', 'updated_at',
                    'is_deleted')
    ordering = ('-created_at',)
    list_display_links = ('user', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(UserProfile, UserProfileAdminView)
