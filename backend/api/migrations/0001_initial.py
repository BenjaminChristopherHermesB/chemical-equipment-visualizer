# Generated migration for EquipmentDataset model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('raw_data', models.JSONField(help_text='Original CSV data as list of dictionaries')),
                ('summary_stats', models.JSONField(help_text='Computed summary statistics')),
                ('row_count', models.IntegerField(default=0)),
                ('equipment_types', models.JSONField(default=list, help_text='List of equipment types')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Equipment Dataset',
                'verbose_name_plural': 'Equipment Datasets',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
