from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User, UserProfile
from basics.models import BaseModel


class Vendor(BaseModel):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile',
                                        on_delete=models.CASCADE)
    company_name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=128, unique=True)
    company_email = models.EmailField()
    company_website = models.CharField(max_length=180, blank=True, null=True)
    contact_person_name = models.CharField(max_length=180, blank=True, null=True)
    contact_person_email = models.EmailField(blank=True, null=True)
    contact_person_phone = models.CharField(max_length=180, blank=True, null=True)
    country = models.CharField(max_length=180, blank=True, null=True)
    company_logo = models.ImageField(upload_to='vendors/company/logos/', blank=True, null=True)
    vendor_license = models.ImageField(upload_to='vendors/license/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'vendors_vendor'
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')
        ordering = ('-created_at', 'user')

    def __str__(self):
        return self.user.email
