from datetime import datetime

from django.contrib import auth
from django.http import Http404
from django.template.defaultfilters import slugify
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User, UserProfile
from basics.functions import get_auto_id
from vendors.models import Vendor
from .serializers import UserSerializer, UserLoginSerializer
from ..vendors.serializers import VendorSerializer


class UserApiView(APIView):

    # permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    @permission_classes((IsAuthenticated, ))
    def get(self, request, format=None):
        users = User.objects.filter(is_deleted=False)
        serialized = UserSerializer(users, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role=User.CUSTOMER)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsApiView(APIView):
    def get_object(self, pk):
        # Returns an object instance that should
        # be used for detail views.
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_detail = self.get_object(pk)
        serialized = UserSerializer(user_detail)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        user_detail = self.get_object(pk)
        serializer = UserSerializer(user_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_detail.set_password(request.data['password'])
            user_detail.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        user_detail = self.get_object(pk)
        serializer = UserSerializer(user_detail,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_detail = self.get_object(pk)
        user_detail.delete()
        response = {
            "statuscode": 204,
            "data": "",
            "message": "record deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class VendorApiView(APIView):
    def get(self, request, format=None):
        vendors = Vendor.objects.filter(is_deleted=False)
        vendor_serialized = VendorSerializer(vendors, many=True, context={'request': request})
        return Response(vendor_serialized.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user_serializer = UserSerializer(data=request.data)
        vendor_serializer = VendorSerializer(data=request.data)
        if user_serializer.is_valid() and vendor_serializer.is_valid():
            user_serializer.save(role=User.VENDOR)

            user = User.objects.get(pk=user_serializer.data['id'])
            user_profile = UserProfile.objects.get(user=user)
            auto_id = get_auto_id(Vendor)
            vendor_name = request.data['company_name']
            slug = slugify(vendor_name)
            creator_id = user.pk
            updater_id = user.pk
            logo = vendor_serializer.validated_data.get('company_logo')
            vendor_license = vendor_serializer.validated_data.get('vendor_license')

            vendor_serializer.save(
                user=user, user_profile=user_profile, auto_id=auto_id,
                creator_id=creator_id, updater_id=updater_id, slug=slug,
                company_logo=logo, vendor_license=vendor_license)

            return Response({'user': user_serializer.data, 'vendor': vendor_serializer.data},
                            status=status.HTTP_200_OK)
        else:
            erros = None
            if user_serializer.errors:
                erros += user_serializer.errors
            if vendor_serializer.errors:
                erros += vendor_serializer.errors
        return Response(erros, status=status.HTTP_200_OK)


class VendorDetailsApiView(APIView):
    def get_object(self, pk):
        # Returns an object instance that should
        # be used for detail views.
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vendor_detail = self.get_object(pk)
        serialized = VendorSerializer(vendor_detail, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):        # validation ERROR
        vendor_detail = self.get_object(pk)
        serializer = VendorSerializer(vendor_detail, data=request.data)
        if serializer.is_valid():
            # updater = request.user                # when authenticated
            slug = slugify(request.data['company_name'])
            updated_at = datetime.datetime.now()
            serializer.save(slug=slug, updated_at=updated_at)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        vendor_detail = self.get_object(pk)
        serializer = VendorSerializer(vendor_detail,
                                      data=request.data,
                                      partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vendor_detail = self.get_object(pk)
        user = User.objects.get(pk=vendor_detail.user.pk)
        user.delete()
        response = {
            "statuscode": 204,
            "data": "",
            "message": "record deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class UserLoginApiView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserSerializer(user)
        if user is not None:
            auth.login(request, user)
            token = RefreshToken.for_user(user)
        data = serializer.data
        if user.is_superadmin:
            data['role'] = "Superuser"
        elif user.role == User.VENDOR:
            data['role'] = "Vendor"
        elif user.role == User.CUSTOMER:
            data['role'] = "Customer"
        else:
            data['role'] = None
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class UserLogoutApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            auth.logout(request)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
