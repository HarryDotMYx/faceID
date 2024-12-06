from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_add_profile_fields'),
    ]

    operations = []  # Remove duplicate operations since they're in initial