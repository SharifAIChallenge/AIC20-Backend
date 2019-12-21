from django.contrib import admin

# Register your models here.
from django.db import models
from martor.widgets import AdminMartorWidget

from apps.notification.models import Notification, Subscriber


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
