from django.core.management.base import BaseCommand, CommandError
from ...models import Section


class Command(BaseCommand):
    help = 'Reset All Sections uuids'

    def handle(self, *args, **options):
        sections = Section.objects.all()
        for section in sections:
            section.uuid = Section.generate_uuid
            section.save()
