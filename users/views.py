from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .models import User, Region, District
from .serializers import PhoneTokenObtainSerializer, RegisterSerializer, RegionSerializer, DistrictSerializer, \
    PhoneTokenObtainAdminSerializer, OperatorSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class OperatorUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OperatorSerializer


class PhoneTokenObtainView(APIView):
    @extend_schema(
        request=PhoneTokenObtainSerializer,
        responses={
            200: OpenApiResponse(
                description="Password changed successfully.",
                response=PhoneTokenObtainSerializer
            ),
            400: OpenApiResponse(
                description="Invalid data or old password incorrect."
            )
        }
    )
    def post(self, request):
        serializer = PhoneTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneTokenObtainAminView(APIView):
    @extend_schema(
        request=PhoneTokenObtainAdminSerializer,
        responses={
            200: OpenApiResponse(
                description="Password changed successfully.",
                response=PhoneTokenObtainAdminSerializer
            ),
            400: OpenApiResponse(
                description="Invalid data or old password incorrect."
            )
        }
    )
    def post(self, request):
        serializer = PhoneTokenObtainAdminSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionCreateAndListView(generics.ListCreateAPIView):
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer


class DistrictCreateAndListView(generics.ListCreateAPIView):
    queryset = District.objects.filter(is_active=True)
    serializer_class = DistrictSerializer
