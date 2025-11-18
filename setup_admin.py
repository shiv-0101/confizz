import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confizz.settings')
django.setup()

from django.contrib.auth.models import User

# Create new superuser
username = "admin"
email = "admin@example.com"
password = "admin@123"

try:
    user = User.objects.create_superuser(username, email, password)
    print(f"✓ Superuser created successfully!")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
except Exception as e:
    print(f"Error: {str(e)}")
