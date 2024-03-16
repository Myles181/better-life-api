from django.contrib import admin
from .models import MyUser, DoctorProfile, PatientProfile

class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'date_of_birth', 'identity']


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user_id', 'phone_number', 'medical_history', 'otp_verified', 'kyc_verified']
    list_editable = ['otp_verified']

    def get_user_id(self, obj):
        return obj.myuser.id # Assuming 'user' is a ForeignKey to MyUser
    get_user_id.short_description = 'User ID'

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user_id', 'phone_number',  'med_cetificate', 'otp_verified', 'kyc_verified']
    list_editable = ['otp_verified']

    def get_user_id(self, obj):
        return obj.myuser.id # Assuming 'user' is a ForeignKey to MyUser
    get_user_id.short_description = 'User ID'


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
