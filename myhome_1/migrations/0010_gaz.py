# Generated by Django 2.1.7 on 2020-12-25 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myhome_1', '0009_electricity'),
    ]

    operations = [
        migrations.CreateModel(
            name='gaz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200)),
            ],
        ),
    ]
