  
from django.db import migrations

class Migration(migrations.Migration):
    """Empty migration - fields already added in initial migration"""

    dependencies = [
        ('recognition', '0002_create_helpdesk'),
    ]

    operations = []
  