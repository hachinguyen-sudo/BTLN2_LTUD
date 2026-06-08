import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CleanSpace.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

if not User.objects.exists():
    print("Database is empty. Loading data.json...")
    call_command('loaddata', 'data.json')
else:
    print("Database already has data. Skipping loaddata.")
