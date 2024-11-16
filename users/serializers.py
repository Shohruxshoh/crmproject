from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Region, District


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'phone', 'role', 'telegram', 'percentage', 'region', 'district']

    def validate(self, attrs):
        if User.objects.filter(telegram=attrs['telegram']).exists():
            raise ValidationError({'telegram': 'Эта телеграмма уже существует.'})

        if User.objects.filter(phone=attrs['phone']).exists():
            raise ValidationError({'phone': 'Этот номер телефона уже существует.'})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['phone'],
            phone=validated_data['phone'],
            telegram=validated_data['telegram'],
            role=validated_data['role'],
            first_name=validated_data['first_name'],
            percentage=validated_data['percentage'],
            region=validated_data['region'],
            district=validated_data['district']
        )
        user.set_password(validated_data['phone'])
        user.is_active = True  # Agar tasdiqlashsiz faol qilishni xohlasangiz
        user.save()
        return user


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'phone', 'role', 'telegram', 'percentage', 'region', 'district']

    # def validate(self, attrs):
    #     if User.objects.filter(telegram=attrs['telegram']).exists():
    #         raise ValidationError({'telegram': 'Эта телеграмма уже существует.'})
    #
    #     if User.objects.filter(phone=attrs['phone']).exists():
    #         raise ValidationError({'phone': 'Этот номер телефона уже существует.'})
    #
    #     return attrs

    def update(self, instance, validated_data):
        phone1 = validated_data.get('phone')
        # Update only the fields that are provided in the request.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.username = phone1
        instance.set_password(phone1)
        instance.save()
        return instance


class PhoneTokenObtainSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    telegram = serializers.CharField()
    phone = serializers.CharField()

    def validate(self, data):
        phone_number = data.get("phone")
        password = data.get("phone")

        user = authenticate(username=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError("Номер телефона или пароль неверный.")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class PhoneTokenObtainAdminSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get("username")
        password = data.get("password")

        user = authenticate(username=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError("Номер телефона или пароль неверный.")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['title']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['title', 'region']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'phone', 'role', 'telegram', 'percentage', 'region', 'district', 'created_at',
                  'updated_at']
