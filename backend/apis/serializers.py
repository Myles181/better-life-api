from .models import MyUser, PatientProfile, DoctorProfile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['firstname'] = user.first_name
        token['lastname'] = user.last_name
        token['email'] = user.email
        token['phone_number'] = user.phone_number # Assuming the user model has a phone_number field

        return token

class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email','password']

    def create(self, validated_data):
        user = MyUser.objects.create(**validated_data)
        return user

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get("refresh")

        try:
            RefreshToken(refresh)
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token")

        return {"refresh": refresh}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = MyUser.objects.filter(email=email).first()

            if user and user.check_password(password):
                return user
        raise serializers.ValidationError("Invalid email or password")

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True, validators=[validate_password])

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'identity', 'password', 'password2']

        # hide password
        extra_kwargs = {
            'password': {'write_only':True},
            'password2': {'write_only':True}
        }

    def create(self, validated_data):
        if validated_data['password']:
            validated_data['fullname'] = validated_data['first_name'] + ' ' + validated_data['last_name']
            password = validated_data.pop("password")
            user = MyUser.objects.create(**validated_data)
            user.set_password(password)
            user.save()

            return user
        else:
            return 
        return 

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['user', 'image', 'phone_number', 'location', 'medical_history']
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['user', 'image', 'phone_number', 'med_cetificate', 'location']
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

from .models import Session


class BookSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['doctor', 'time', 'meet_platform']

        
        


import jwt
from rest_framework.request import Request


def validated_token(secret, request: Request):
    authorization_header = request.headers.get('Authorization')
    
    if not authorization_header:
        return {'response': 'failed', 'error': 'Authorization header missing'}, None
    
    token_parts = authorization_header.split()
    if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
        return {'response': 'failed', 'error': 'Invalid Authorization header'}, None
    
    token = token_parts[1]

    if token and secret:
        try:
            data = jwt.decode(token, secret, algorithms=['HS256'])
            print(data)
            return {'response': 'success'}, data
        except jwt.ExpiredSignatureError:
            return {'response': 'failed', 'error': 'Expired token'}, None
        except jwt.InvalidTokenError as e:
            return {'response': 'failed', 'error': str(e)}, None
    else:
        return {'response': 'failed', 'error': 'Please provide all requirements'}, None

