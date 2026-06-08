import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CleanSpace.settings')
django.setup()

from django.core.management import call_command
from apps.services.models import Service

if not Service.objects.exists():
    print("Database is missing services. Loading data.json...")
    call_command('loaddata', 'data.json')
else:
    print("Database already has data. Skipping loaddata.")
