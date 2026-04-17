from django.core.management.base import BaseCommand
from django.db import connection
from profiles.models import Profile

class Command(BaseCommand):
    help = 'Check database status'

    def handle(self, *args, **options):
        # Check if table exists
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='profiles_profile'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            count = Profile.objects.count()
            self.stdout.write(self.style.SUCCESS(f'Table exists! Total profiles: {count}'))
        else:
            self.stdout.write(self.style.ERROR(' Table does not exist!'))