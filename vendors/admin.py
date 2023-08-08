from django.contrib import admin
from .models import Vendor


class VendorAdminView(admin.ModelAdmin):
    list_display = ('id', 'auto_id', 'user', 'user_profile',
                    'company_name', 'slug', 'company_email',
                    'company_website', 'contact_person_name', 'contact_person_email',
                    'contact_person_phone', 'country', 'company_logo', 'vendor_license',
                    'updated_at', 'is_deleted', 'is_approved')
    ordering = ('-created_at',)
    list_display_links = ('user', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Vendor, VendorAdminView)
