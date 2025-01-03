  
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('technical', 'Technical Issue'), ('account', 'Account Related'), ('feature', 'Feature Request'), ('other', 'Other')], max_length=20)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('new', 'New'), ('open', 'Open'), ('review', 'Under Review'), ('hold', 'On Hold'), ('cancelled', 'Cancelled'), ('closed', 'Closed')], default='new', max_length=20)),
                ('response', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('closed_at', models.DateTimeField(null=True, blank=True)),
                ('status_changed_at', models.DateTimeField(null=True, blank=True)),
                ('previous_status', models.CharField(blank=True, max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
  