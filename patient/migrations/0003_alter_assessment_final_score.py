# Generated by Django 5.0.6 on 2024-06-07 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_patientdetail_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='final_score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]