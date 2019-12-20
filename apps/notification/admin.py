from django.contrib import admin


# Register your models here.
from apps.notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
