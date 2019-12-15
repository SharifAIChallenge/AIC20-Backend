from django.contrib import admin

from homepage.models import Homepage, Screen, Photo, TimeLineEvent, PrizeText_En, PrizeText_Fa, Prize, Sponsor, Link, \
    Organizer

admin.site.register(Homepage)
admin.site.register(Screen)
admin.site.register(Photo)
admin.site.register(TimeLineEvent)
admin.site.register(Prize)
admin.site.register(Link)
admin.site.register(Sponsor)
admin.site.register(Organizer)
