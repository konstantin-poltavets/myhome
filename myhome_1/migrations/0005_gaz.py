# Generated by Django 2.1.7 on 2020-02-01 20:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myhome_1', '0004_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='gaz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('fuel_type', models.CharField(blank=True, choices=[('GAZ_95', 'Gaz_95'), ('GAZ_98', 'Gaz_98'), ('LPG', 'LPG')], default='LPG', max_length=6)),
                ('liters', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
