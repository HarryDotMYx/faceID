from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0002_create_helpdesk'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='status_changed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='previous_status',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]