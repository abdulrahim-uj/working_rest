from rest_framework import serializers
from vendors.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True, required=False)
    auto_id = serializers.SerializerMethodField(read_only=True, required=False)
    user = serializers.SerializerMethodField(read_only=True, required=False)
    user_profile = serializers.SerializerMethodField(read_only=True, required=False)
    slug = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta(object):
        model = Vendor
        # fields = ('id', 'company_name', 'company_email',
        #           'company_website', 'contact_person_name', 'contact_person_email',
        #           'contact_person_phone', 'country', 'company_logo', 'vendor_license', 'user_name')
        fields = ('id', 'auto_id', 'user', 'user_profile',
                  'company_name', 'slug', 'company_email',
                  'company_website', 'contact_person_name', 'contact_person_email',
                  'contact_person_phone', 'country', 'company_logo', 'vendor_license',
                  'updated_at', 'is_deleted', 'is_approved', 'user_name')

    def get_user_name(self, instance):
        if instance.user:
            return instance.user.username
        else:
            return ""

    def get_auto_id(self, instance):
        if instance:
            return instance.auto_id
        else:
            return ""

    def get_user(self, instance):
        if instance.user:
            return instance.user.pk
        else:
            return ""

    def get_user_profile(self, instance):
        if instance.user_profile:
            return instance.user_profile.pk
        else:
            return ""

    def get_slug(self, instance):
        if instance.slug:
            return instance.slug
        else:
            return ""
