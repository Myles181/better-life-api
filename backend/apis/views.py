from .models import MyUser
from .serializers import (MyUserSerializer, LoginSerializer, RefreshTokenSerializer, 
                          RefreshToken, validated_token, PatientProfileSerializer, DoctorProfileSerializer, DoctorProfile)

from django.shortcuts import get_object_or_404
# from .serializers import CustomTokenObtainPairSerializer
from django.http import JsonResponse
from backend.settings import SECRET_KEY

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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


class LoginView(APIView):
    authentication_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            token = CustomTokenObtainPairSerializer.get_token(user)

            return Response({
                'refresh': str(refresh),
                'access': str(token.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

# Test API
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def testView(request):
    message, token = validated_token(SECRET_KEY, request)

    print(token)
    print(message)
    return Response({"token": token, "message": message})

# Logout
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def logoutView(request):
    message, token = validated_token(SECRET_KEY, request)

    print(token)
    print(message)
    if message['response'] == 'success' and token:
        if request.method == 'POST':
            try:
                refresh_token = request.data["refresh_token"]
                logout_token = RefreshToken(refresh_token)
                logout_token.blacklist()
                return Response({'message': 'successful'}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({'error': 'Invalid or missing refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid or missing refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def update_patient_profile(request):
    message, token = validated_token(SECRET_KEY, request)

    if message['response'] == 'success' and token:
        if request.method == 'POST':
            
            user_id = token['user_id']
            user = get_object_or_404(MyUser, id=user_id)
            # user = MyUser.objects.filter(id=user_id).first()
            request.data['user'] = user

            serializer = PatientProfileSerializer(data=request.data)
            if serializer.is_valid():
                # data = serializer.validated_data
                serializer.save()
                return Response({"message": "Success"}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def update_doctor_profile(request):
    message, token = validated_token(SECRET_KEY, request)

    if message['response'] == 'success' and token:
        if request.method == 'POST':

            user_id = token['user_id']
            user = get_object_or_404(MyUser, id=user_id)
            # user = MyUser.objects.filter(id=user_id).first()
            request.data['user'] = user

            serializer = DoctorProfileSerializer(data=request.data)
            if serializer.is_valid():
                # data = serializer.validated_data
                serializer.save()
                return Response({"message": "Success"}, status=status.HTTP_200_OK)

from .serializers import BookSessionSerializer


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def create_session(request):
    message, token = validated_token(SECRET_KEY, request)

    if message['response'] == 'success' and token:
        if request.method == 'POST':
            serializer = BookSessionSerializer(data=request.data)
            if serializer.is_valid():
                doctor_id = request.data.get('doctor_id')
                doctor_profile = DoctorProfile.objects.get(user__id=doctor_id)
                serializer.save(doctor=doctor_profile, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

