# Generated by Django 2.2.2 on 2019-06-24 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0009_auto_20190619_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='boards',
            name='scetch',
            field=models.FileField(blank=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='modules',
            name='type1',
            field=models.CharField(blank=True, choices=[('TEMP', 'Temperature'), ('HUM', 'Humidity'), ('IR_R', 'IR_Receiver'), ('IR_T', 'IR_Transmitter'), ('ALT', 'Altitude')], default='TEMP', max_length=6),
        ),
        migrations.AddField(
            model_name='modules',
            name='type2',
            field=models.CharField(blank=True, choices=[('TEMP', 'Temperature'), ('HUM', 'Humidity'), ('IR_R', 'IR_Receiver'), ('IR_T', 'IR_Transmitter'), ('ALT', 'Altitude')], default='', max_length=6),
        ),
        migrations.AddField(
            model_name='modules',
            name='type3',
            field=models.CharField(blank=True, choices=[('TEMP', 'Temperature'), ('HUM', 'Humidity'), ('IR_R', 'IR_Receiver'), ('IR_T', 'IR_Transmitter'), ('ALT', 'Altitude')], default='', max_length=6),
        ),
        migrations.AddField(
            model_name='modules',
            name='type4',
            field=models.CharField(blank=True, choices=[('TEMP', 'Temperature'), ('HUM', 'Humidity'), ('IR_R', 'IR_Receiver'), ('IR_T', 'IR_Transmitter'), ('ALT', 'Altitude')], default='', max_length=6),
        ),
        migrations.AlterField(
            model_name='boards',
            name='processor',
            field=models.ForeignKey(default=82, on_delete=django.db.models.deletion.DO_NOTHING, related_name='processor', to='iot.Modules'),
        ),
        migrations.AlterField(
            model_name='boards',
            name='sensor1',
            field=models.ForeignKey(default=82, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sensor1', to='iot.Modules'),
        ),
        migrations.AlterField(
            model_name='boards',
            name='sensor2',
            field=models.ForeignKey(default=82, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sensor2', to='iot.Modules'),
        ),
        migrations.AlterField(
            model_name='boards',
            name='sensor3',
            field=models.ForeignKey(default=82, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sensor3', to='iot.Modules'),
        ),
        migrations.AlterField(
            model_name='boards',
            name='sensor4',
            field=models.ForeignKey(default=82, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sensor4', to='iot.Modules'),
        ),
    ]