from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class MyUser(AbstractUser):
    class Identity(models.TextChoices):
        patient = 'Patient'
        doctor = 'Doctor'

    email = models.EmailField(unique=True)
    username = models.CharField(null=True)
    fullname = models.CharField(null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    identity = models.CharField(max_length=15,
                                choices=Identity.choices)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class PatientProfile(models.Model):
    user = models.OneToOneField(MyUser,
                                on_delete=models.CASCADE,
                                primary_key=True)
    image = models.ImageField()
    phone_number = models.CharField(max_length=11)
    location = models.CharField(max_length=255)
    medical_history = models.CharField(max_length=255) # Change Eventually
    otp_verified = models.BooleanField(default=False) #Once OTP verification Success: True
    kyc_verified = models.BooleanField(default=False) #Once Medical history Success: True



class DoctorProfile(models.Model):
    user = models.OneToOneField(MyUser,
                                on_delete=models.CASCADE,
                                primary_key=True)
    image = models.ImageField()
    phone_number = models.CharField(max_length=11)
    med_cetificate = models.ImageField(default=None)
    location = models.CharField(max_length=255)
    otp_verified = models.BooleanField(default=False) #Once OTP verification Success: True
    kyc_verified = models.BooleanField(default=False) #Once Medical Education Success: True



    """
    BOOKING SESSIONS WITH ACTIVE DOCTOR'S
    """

class Session(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='sessions')
    time = models.DateTimeField(default=timezone.now)
    meet_platform = models.CharField(max_length=30)

