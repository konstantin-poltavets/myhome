import random
from celery import shared_task
from django.http import request
from .models import electrozones, electricity
from datetime import date, datetime, timedelta, timezone
import numpy as np
from .views import close_to_time
import logging
import pytz
import os
from .constants import *


@shared_task(name="electro_zones")
def electro_zones():
    yesterday = datetime.today() - timedelta(days = 1)
    dat_00 = close_to_time(yesterday.year, yesterday.month, yesterday.day, 0,0,0)
    queryset_energy_0 = electricity.objects.all().filter(created_date = dat_00[0]).values_list('energy')[0][0]   
    dat_7 = close_to_time(yesterday.year, yesterday.month, yesterday.day, NIGHT_ELECTRO_TIME_E,0,0)
    queryset_energy_7 = electricity.objects.all().filter(created_date = dat_7[0]).values_list('energy')[0][0]
    dat_23 = close_to_time(yesterday.year, yesterday.month, yesterday.day,NIGHT_ELECTRO_TIME_B,0,0)
    queryset_energy_23 = electricity.objects.all().filter(created_date = dat_23[0]).values_list('energy')[0][0]
    dat_24 = close_to_time(yesterday.year, yesterday.month, yesterday.day,23,59,59)
    queryset_energy_24 = electricity.objects.all().filter(created_date = dat_24[0]).values_list('energy')[0][0]
    energy_night = queryset_energy_24 - queryset_energy_23 + queryset_energy_7 - queryset_energy_0
    energy_day = queryset_energy_23 - queryset_energy_7
    p = electrozones.objects.create(created_date=yesterday, energy_night=energy_night, energy_day=energy_day)
    

@shared_task(name="watchdog_electro")
def watchdog_electro():
    
    last_event = electricity.objects.all().order_by('-id')[:1].values_list('created_date')[0][0]
    delta = int(str(datetime.today().replace(tzinfo=pytz.timezone("UTC")) - last_event).split(":")[1])
    asctime = str(datetime.now())
    #logging.basicConfig()
    logger = logging.getLogger('my_django')

    if delta < 3:
        logger.info('%s: INFO: No electricity info during %s min.', asctime, delta)
    if 3 <= delta < 10:
        logger.warning ('%s: WARNING: No electricity info during %s min.', asctime, delta)
        os.system('sudo systemctl restart mqtt.py')
    if 10 <= delta < 30:
        logger.error('%s: ERROR: No electricity info during %s min.', asctime, delta)
        os.system('sudo systemctl restart mqtt.py')
    if 30 <= delta:
        logger.critical('%s: CRITICAL: No electricity info during %s min.', asctime, delta)
        os.system('sudo systemctl restart mqtt.py')
    

