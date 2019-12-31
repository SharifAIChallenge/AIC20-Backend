from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from apps.accounts.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'firstname_fa',
        'firstname_en',
        'lastname_fa',
        'lastname_en',
        'birth_date',
        'university',
    ]


@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):
    def username(self, obj):
        try:
            uid = urlsafe_base64_decode(obj.uid).decode('utf-8')
            qs = User.objects.filter(id=uid)
            if qs.count() == 1:
                return qs.get().username
        except:
            pass
        return "SHIT REPORT THIS TO TECH-ADMIN"

    list_display = ['username']


@admin.register(ActivateUserToken)
class ActivateUserTokenAdmin(admin.ModelAdmin):
    def username(self, obj):
        try:
            email = urlsafe_base64_decode(obj.eid).decode('utf-8')
            qs = User.objects.filter(email=email)
            if qs.count() == 1:
                return qs.get().username
        except:
            pass
        return "SHIT REPORT THIS TO TECH-ADMIN"

    list_display = ['username']

