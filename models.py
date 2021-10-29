from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Avg, Count, Sum, Min, Max
from django.utils.timezone import now

class mqtt(models.Model):
    topic = models.CharField(max_length=200)
    payload = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.topic

    #def __str__(self):
     #   return self.payload

class Payment(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=4)
    datetime = models.DateTimeField()



class gazoline(models.Model):
    created_date = models.DateField(default=timezone.now)

    Benzine = 'B'
    LPG = 'LPG'
    GAZ_TYPES_CHOICES = ((Benzine, 'B'), (LPG, 'LPG'),)
    fuel_type = models.CharField(max_length=7, blank=False,choices=GAZ_TYPES_CHOICES, default=LPG)

    liters = models.DecimalField(max_digits=7, decimal_places=2)
    millage = models.PositiveIntegerField(blank=False, default=240000)

    BRSM = 'BRSM'
    KLO = 'KLO'
    LPG = 'LPG'
    WOG = 'WOG'
    Other = 'Other'
    STATION_TYPES_CHOICES = ((BRSM, 'BRSM'), (KLO, 'KLO'), (LPG, 'LPG'), (WOG, 'WOG'), (Other, 'Other'))
    price_after_disc = models.DecimalField(max_digits=7, decimal_places=2)      
    price_liter = models.DecimalField(max_digits=7, decimal_places=2)
    station = models.CharField(max_length=6, blank=True, choices=STATION_TYPES_CHOICES, default=BRSM)
    

    @property
    def price_before_disc(self):
        return self.price_liter * self.liters

    @property
    def disc(self):
        return self.price_liter * self.liters - self.price_after_disc

    class Meta:
        ordering = ["-created_date", "-id"]


    def __float__(self):
        return (self.price)


    def agregates(self, start_date, end_date):
        cont = []
        start_date_final = str(start_date)+ '-01-01'
        # annual summary
        for y in range(start_date, end_date+1, 1):
            start_date = str(y) + '-01-01'
            end_date = str(y) + '-12-31'
            query = self.objects.all().filter(created_date__range=(start_date, end_date))

            query_Count = query.aggregate(Count('created_date'))["created_date__count"]
            query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]
            query_Liters = query.aggregate(Sum('liters'))["liters__sum"]
            query_Avg = query_Sum/query_Liters
            query_Min = query.aggregate(Min('millage'))["millage__min"]
            query_Max = query.aggregate(Max('millage'))["millage__max"]
            distance = query_Max - query_Min
            rashod = (query_Liters/distance)*100

            agr = {'start_date': start_date, 'end_date': end_date, 'query_Avg': query_Avg,
                   'query_Count': query_Count, 'query_Sum': query_Sum, 'query_Liters': query_Liters,
                   'query_Min': query_Min, 'query_Max': query_Max, 'distance': distance, 'rashod': rashod}

            cont.append(agr)
            #summary for whole period
        query = self.objects.all().filter(created_date__range=(start_date_final, end_date))
        query_Count = query.aggregate(Count('created_date'))["created_date__count"]
        query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]
        query_Liters = query.aggregate(Sum('liters'))["liters__sum"]
        query_Avg = query_Sum / query_Liters
        query_Min = query.aggregate(Min('millage'))["millage__min"]
        query_Max = query.aggregate(Max('millage'))["millage__max"]
        distance = query_Max - query_Min
        rashod = (query_Liters/distance)*100

        agr = {'start_date': start_date_final, 'end_date': end_date, 'query_Avg': query_Avg,
               'query_Count': query_Count, 'query_Sum': query_Sum, 'query_Liters': query_Liters,
                'query_Min': query_Min, 'query_Max': query_Max, 'distance': distance, 'rashod': rashod}

        cont.append(agr)

        return cont



class orbi_tmp(models.Model):

    distance = models.PositiveIntegerField(blank=False, default=0)
    time = models.DecimalField(max_digits=7, decimal_places=2)
    speed = models.DecimalField(max_digits=4, decimal_places=2, default = 0)
    created = models.DateTimeField(auto_now=True)
    #property
    #ef speeds(self):
    #   return float(self.distance / self.time) * 3.6


class orbitrack(models.Model):
    start = models.DateField(default=timezone.now)
    distance = models.PositiveIntegerField(blank=False, default=0)
    time = models.PositiveIntegerField(blank=False, default=0)
    speed = models.DecimalField(max_digits=4, decimal_places=2)

    @property
    def finish(self):
        return self.start +  self.time*1000
        
        
        
class electricity(models.Model):
    param = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    measured_time = models.DateTimeField(default=timezone.now)
    current = models.DecimalField(max_digits=10, decimal_places=3)
    energy = models.DecimalField(max_digits=10, decimal_places=3)
    voltage = models.DecimalField(max_digits=10, decimal_places=3)
    frequency = models.DecimalField(max_digits=10, decimal_places=3)
    pf = models.DecimalField(max_digits=10, decimal_places=3)
    
    def __str__(self):
        return self.param




        
        
        
