from django.db.models import QuerySet, Sum
from rest_framework import serializers
from .models import mqtt, gazoline, electricity
import datetime

class mqttSerializer(serializers.ModelSerializer):

    class Meta:
        model = mqtt
        fields = ('topic','payload','created_date' )
        

class gazSerializer(serializers.ModelSerializer):


    class Meta:
        model = gazoline
        fields = ('created_date','liters','millage','fuel_type')


        
class ElectricitySerializer(serializers.ModelSerializer):

    class Meta:
        model = electricity
        fields = ('param', 'created_date', 'measured_time', 'current',
            'energy', 'voltage', 'frequency' , 'pf', 'power')