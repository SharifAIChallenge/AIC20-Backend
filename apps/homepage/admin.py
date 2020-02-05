from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models

from martor.widgets import AdminMartorWidget

from .models import Intro, TimelineEvent, Prize, Stat, Sponsor, WhyThisEvent, Quote


@admin.register(Intro)
class IntroAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(TimelineEvent)
class TimelineEventAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Prize)
class PrizeAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Stat)
class StatAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Sponsor)
class SponsorAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(WhyThisEvent)
class WhyThisEventAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Quote)
class QuoteAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
