from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .serializers import mqttSerializer, gazSerializer, ElectricitySerializer
from rest_framework import filters, generics
from .models import mqtt, gazoline, orbi_tmp, electricity, electrometr, electrozones
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render_to_response
from qsstats import QuerySetStats
from datetime import date, datetime, timedelta, timezone
from .forms import MyForm, gazForm, orbiForm
from django.http import HttpResponse, JsonResponse, request
from django.db.models import F, Count, Value, Avg, Sum,  Min, Max
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db.models.functions import Extract
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .script import stock ,orbitrack, orbi_stop
from time import gmtime, strftime
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from django.utils import timezone
from django.contrib.auth.models import User
import pytz
import csv
import numpy as np
import logging
from .constants import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin





class GazListjson(generics.ListAPIView):
    queryset=gazoline.objects.all().filter(fuel_type = 'LPG')
    serializer_class = gazSerializer


class mqttList(generics.ListAPIView):
    queryset = mqtt.objects.all()
    serializer_class = mqttSerializer


class mqttDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = mqtt.objects.all()
    serializer_class = mqttSerializer


class mqttViewSet(viewsets.ModelViewSet):
    __basic_fields = ('topic','payload','created_date',)
    #queryset = mqtt.objects.all().filter(topic = "temp")
    queryset = mqtt.objects.all()
    serializer_class = mqttSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = __basic_fields
    search_fields = __basic_fields



class gazListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = gazoline
    fields = '__all__'
   # paginate_by = 3views.indicator_mqtt


def graph_1(request):
    return render(request, 'graph1.html')


def publish_1(request):
    return render(request, 'publish.html')

@login_required
def select(request):
    queryset = mqtt.objects.all().filter(topic = "temperature")[::0]
    #queryset = mqtt.objects.get(Q(topic = "home/bath/esp1/humidity"))
    return render(request, "select.html", {"mqtt": queryset})

@login_required
def search(request):
    return render_to_response('search.html')

@login_required
def search_result(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']

    if 'r' in request.GET and request.GET['r']:
        r = int(request.GET['r'])

        queryset = mqtt.objects.filter(topic = q)[::r]
        return render_to_response('search_result.html',
            {'mqtt': queryset, 'query': q, 'skipped_rows': r})
    else:
        return HttpResponse('Please submit a search term.')

@login_required
def publish(request):
    if request.method == "POST":
        queryset_temp = mqtt.objects.all().filter(topic = "temperature")[::0]
        queryset_hum = mqtt.objects.all().filter(topic = "humidity")[::0]
        date = POST['datepicker']
        return render(request.POST, "line_chart.html", {"my_date": date, "my_data_temp": queryset_temp, "my_data_hum": queryset_hum})
    else:
        form = MyForm()
        return render(request, 'calendar_2.html', {'form': form})

@login_required
def view_func_iii(request):
    start_date = date(2016, 3, 12)
    end_date = date(2016, 3, 16)
    queryset = mqtt.objects.all()
    qsstats = QuerySetStats(queryset, date_field='created_date')
    values = qsstats.time_series(start_date, end_date, interval='days', aggregate=Count('created_date'))
    summary = qsstats.time_series(start_date, end_date,  aggregate=Count('payload'))
    return render_to_response('template_2.html', {'values': values, 'summary': summary})

@login_required
def view_func(request):
    queryset_temp = mqtt.objects.all().filter(topic = "home/poliv/temp")[::]
    queryset_hum = mqtt.objects.all().filter(topic = "home/poliv/water").order_by('-created_date')
    return render(request, "line_chart.html", {"my_data_temp": queryset_temp, "my_data_hum": queryset_hum})

@login_required
def google_graphs(request):
    return render_to_response('graph1.html')
@login_required
#@csrf_exempt
def google_rest_int(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        mqtt_data = mqtt.objects.all().filter(payload__lte =  22.5).filter(topic = "home/poliv/temp")
        serializer = mqttSerializer(mqtt_data, many=True)
        return JsonResponse(serializer.data, safe=False)


@login_required
def google_rest(request):
        return render_to_response('test2020.html')


def indicator(request):
    return render_to_response('indicator_2.html')


def indicator_mqtt(request):
    orbitrack.main()
    return render_to_response('indicator_mqtt.html')

def orbiStop(request):
    orbi_stop.main()
    return render_to_response('index_1.html')



class gazDetailView(generic.DetailView):
    """Generic class-based list view for a list of authors."""
    model = gazoline


@login_required
def gaz_add(request):
    if request.method == "POST":
        form = gazForm(request.POST, request.FILES)
        if form.is_valid():
            boards = form.save(commit=False)
            #modules.name = form['name'].value()
            boards.save()
            return redirect('gaz_list')
    else:
        form = gazForm()
    return render(request, 'myhome_1/gazoline_add.html', {'form': form})


@login_required
def gaz_template(request):
    start_date = 2012
    end_date = 2013
    start_date = int(request.GET['year_1'])
    end_date = int(request.GET['year_2'])

    cont = gazoline.agregates(gazoline, start_date, end_date)

    values_count = [t["query_Count"] for t in cont]
    values_dat = [t["start_date"][:4] for t in cont]
    values_sum = [t["query_Sum"] for t in cont]
    values_avg = [t["query_Avg"] for t in cont]
    values_liters = [t["query_Liters"] for t in cont]
    values_rashod = [t["rashod"] for t in cont]
    values_distance = [t["distance"] for t in cont]

    values_count.pop(), values_dat.pop(),values_sum.pop()
    values_avg.pop(), values_liters.pop(), values_distance.pop(), values_rashod.pop()


    #print("disc", gazoline().disc())
   # print("values_dat", values_dat)
    #captions_a = [t[0].year for t in values_dat]

    return render(request, 'template_gaz_func.html', {'cont': cont,
                                                      'values_dat': values_dat,
                                                      'values_count': values_count,
                                                      'values_sum': values_sum,
                                                      'values_avg': values_avg,
                                                      'values_liters': values_liters,
                                                      'values_distance': values_distance,
                                                      'values_rashod': values_rashod
                                                      })

@login_required
def gazoline_edit(request, pk):
    g = get_object_or_404(gazoline, pk=pk)
    if request.method == "POST":
        form = gazForm(request.POST,  request.FILES, instance=g)
        if form.is_valid():
            form.save()
            return redirect('gazoline_edit_view', pk=pk)
    else:
        form = gazForm(instance=g)
    return render(request, 'myhome_1/gazoline_edit.html', {'form': form})


@login_required
def gaz_template_month(request):
    start_date = date(int(request.GET['year_1'][0:4]),1,1)
    end_date = date(int(request.GET['year_1'][0:4]),12,31)
    query = gazoline.objects.all()
    qsstats = QuerySetStats(query, date_field='created_date', aggregate=Sum('price_after_disc'))
    values = qsstats.time_series(start_date, end_date, interval='months')
    qsstats = QuerySetStats(query, date_field='created_date', aggregate=Sum('liters'))
    liters = qsstats.time_series(start_date, end_date, interval='months')
    query_1 = query.filter(created_date__year=start_date.year)

    return render_to_response( 'template_gaz_google.html', {'query':query_1,'values':values, 'liters':liters})


@login_required
def gaz_search(request):
    return render_to_response('gaz_search.html')


@login_required
def gchart(request):
    return render_to_response('gchart_1.html')


@login_required
def gaz_search_result(request):

    start_date = date(int(request.GET['year_1']),1,1)
    end_date = date(int(request.GET['year_2']),12,31)
    query = gazoline.objects.all().filter(created_date__range=(start_date, end_date))
    query_Avg = query.aggregate(Avg('price_liter'))["price_liter__avg"]
    query_Count = query.aggregate(Count('created_date'))["created_date__count"]
    query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]
    query_Liters = query.aggregate(Sum('liters'))["liters__sum"]
    query_Min = query.aggregate(Min('millage'))["millage__min"]
    query_Max = query.aggregate(Max('millage'))["millage__max"]
    distance = query_Max - query_Min
    qsstats = QuerySetStats(query, date_field='created_date')
    values_dat_m = qsstats.time_series(start_date, end_date, interval='months', aggregate=Sum('price_after_disc'))
    values_a = [t[1] for t in values_dat_m]
    captions_a = [t[0] for t in values_dat_m]

    return render(request, 'search_result_gaz.html', {'values': values_dat_m,
                                                     'query_Avg': query_Avg,
                                                     'query_Count': query_Count,
                                                     'query_Sum': query_Sum,
                                                      'query_Liters': query_Liters,
                                                     'values_dat': values_dat_m,
                                                     'values_a': values_a,
                                                     'captions_a': captions_a,
                                                      'distance': distance })

class GazDelete(DeleteView):
    model = gazoline
   # template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('gaz_list')



class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]


    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]



    def get_data(self):
        """Return 3 datasets to plot."""
        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


 #   line_chart = TemplateView.as_view(template_name='line_chart.html')
#    line_chart_json = LineChartJSONView.as_view()


@login_required
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myhome_1_gazoline.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'created_date','fuel_type', 'liters','millage','price_after_disc','price_liter','station'])

    gaz = gazoline.objects.all().values_list( 'id', 'created_date','fuel_type', 'liters','millage','price_after_disc','price_liter','station')
    for gaz in gaz:
        writer.writerow(gaz)

    return response

@login_required
def export_orbitrack_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myhome_1_orbitrack.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'distance', 'time', 'speed', 'created'])

    orbi = orbi_tmp.objects.all().values_list( 'id', 'distance', 'time', 'speed', 'created')
    for orbi in orbi:
        writer.writerow(orbi)

    return response


def get_success_url(self):
    return request.META.get('HTTP_REFERER')


def get_stock(request):
    start_date = date(2016, 3, 12)
    end_date = date(2016, 3, 16)
    stock_info = stock.main()
    return render_to_response( 'stock.html', { 'stock_info': stock_info})


def sec(request):
    secunds =  (strftime("%H:%M:%S", gmtime()))
    return HttpResponse(secunds)



class orbi_tmpListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = orbi_tmp
    fields = '__all__'
    
    
@login_required
@api_view(['GET', 'POST', 'DELETE'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def arduino(request):

    if request.method == 'GET':
        mqtts = mqtt.objects.all()
        
      
        mqtts_serializer = mqttSerializer(mqtts, many=True)
        return JsonResponse(mqtts_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        mqtt_data = JSONParser().parse(request)
        mqtts_serializer = mqttSerializer(data=mqtt_data)
        if mqtts_serializer.is_valid():
            mqtts_serializer.save(created_date=timezone.now())
            return JsonResponse(mqtts_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(mqtts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = mqtt.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


        
@api_view(['GET', 'POST', 'DELETE'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
@login_required
def electro(request):

    if request.method == 'GET':
        electricitys = electricity.objects.all().filter(param = ('100'))
        
      
        electricity_serializer = ElectricitySerializer(electricitys, many=True)
        return JsonResponse(electricity_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        electricity_data = JSONParser().parse(request)
        electricity_serializer = ElectricitySerializer(data=electricity_data)
        if electricity_serializer.is_valid():
            electricity_serializer.save(created_date=timezone.now())
            return JsonResponse(electricity_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(electricity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = electricitys.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were del successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@login_required
def electroshow(request):
    return render_to_response('indicator_electro.html')
    
    
    
class ElectroListjson(generics.ListAPIView):
    queryset=electricity.objects.all()
    serializer_class = ElectricitySerializer

    
@login_required    
def electroshow_all(request):
    return render_to_response('indicator_electro_all.html')
    
    
class electricityListView(LoginRequiredMixin,generic.ListView):
    model = electricity
    end_date = datetime.now()
    end_date = end_date#.replace(tzinfo=pytz.timezone("Europe/Kiev"))
    start_date = end_date - timedelta(days=1)
    queryset = electricity.objects.all().order_by('-id')[:500]#filter(param = "100", created_date__range=(start_date, end_date)) 
    fields = '__all__'

@login_required   
def electricity_template_day(request):
    query=electricity.objects.all()
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    qsstats = QuerySetStats(query, date_field='created_date', aggregate=Max('power'))
    values = qsstats.time_series(start_date, end_date, interval='months')
    query_1 = query.filter(created_date__year=start_date.year)
    return render_to_response( 'template_electricity_google.html', {'query':query_1,'values':values})

@login_required
def export_electro_all_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export_electro_all.csv"'

    writer = csv.writer(response)
    writer.writerow(['param', 'created_date', 'current', 'energy', 'voltage', 'frequency', 'pf', 'power'])

    electro = electricity.objects.all().values_list('param', 'created_date', 'current', 'energy', 'voltage', 'frequency', 'pf', 'power')
    for e in electro:
        writer.writerow(e)
    return response
   
@login_required   
def electricity_all_graph(request):

    end_date = datetime.now()+ timedelta(days=0.2)
    #end_date = end_date.replace(tzinfo=pytz.timezone("Europe/Kiev")) + timedelta(days=0.1)
    start_date = end_date - timedelta(days=1.2)
    queryset_power = electricity.objects.all().filter(param = "100", created_date__range=(start_date, end_date))
    #queryset_hum = mqtt.objects.all().filter(topic = "home/poliv/water").order_by('-created_date')
    queryset_power = electricity.objects.all().filter(param = "100", created_date__range=(start_date, end_date))
    lst = np.asarray(queryset_power.values_list('created_date'))
   
    return render(request, "line_chart_electro.html", {"my_data_power": queryset_power})



class electrometrListView(generic.ListView):
    model = electrometr
    end_date = timezone.now()
    #end_date = end_date.replace(tzinfo=pytz.timezone("Europe/Kiev"))
    start_date = end_date - timedelta(days=1)
    queryset = electrometr.objects.all()#.order_by('-id')[:100]#filter(param = "100", created_date__range=(start_date, end_date))
    
    fields = '__all__'
    


def close_to_time(year, month, day, hr, min, sec):

    K = datetime(year, month, day, hr, min, sec)
    K = K.replace(tzinfo=pytz.timezone("UTC"))
    end_date = K+ timedelta(minutes=10)
    start_date = K - timedelta(minutes=10)
    queryset_power = electricity.objects.all().filter(param = "100", created_date__range=(start_date, end_date))
    lst = np.asarray(queryset_power.values_list('created_date'))
    idx = (np.abs(lst - K)).argmin()
    close_to = lst[idx]
    return close_to

@login_required   
def electro_zones_old(request):
    month = datetime.today().month
    year = datetime.today().year
    queryset = electrozones.objects.all().filter(created_date__month = month,created_date__year = year).order_by('created_date')
    query_Sum_night = queryset.aggregate(Sum('energy_night'))["energy_night__sum"]
    query_Sum_day = queryset.aggregate(Sum('energy_day'))["energy_day__sum"]
    query_Sum = query_Sum_night+query_Sum_day

    price_Sum_night = float(query_Sum_night) * NIGHT_ELECTRO_PRICE
    price_Sum_day = float(query_Sum_day) * DAY_ELECTRO_PRICE
    price_Sum = price_Sum_night + price_Sum_day

    queryset_meter = electrozones.objects.all()
    meter_Sum_night = float(queryset_meter.aggregate(Sum('energy_night'))["energy_night__sum"]) + NIGHT_ELECTRO_METER_0
    meter_Sum_day = float(queryset_meter.aggregate(Sum('energy_day'))["energy_day__sum"]) + DAY_ELECTRO_METER_0
    meter_Sum = meter_Sum_day + meter_Sum_night

    return render_to_response('electro_zones.html', { 'queryset':queryset, 'energy_sum_night': query_Sum_night, 
    'energy_sum_day': query_Sum_day, 'energy_sum': query_Sum ,
    'price_sum_day': price_Sum_day, 'price_sum': price_Sum ,
    'price_sum_night': price_Sum_night, 'day_electro_meter': meter_Sum_day, 'night_electro_meter': meter_Sum_night,
    'electro_meter': meter_Sum
    })
    
 
def electro_zones(request):

    if 'e-month' in request.GET:
        month = int(request.GET['e-month'][5:7])    
        year = int(request.GET['e-month'][:4])
      
    else:
        month = datetime.today().month
        year = datetime.today().year
    try:
        queryset = electrozones.objects.all().filter(created_date__month = month,created_date__year = year).order_by('created_date')
        query_Sum_night = queryset.aggregate(Sum('energy_night'))["energy_night__sum"]
        query_Sum_day = queryset.aggregate(Sum('energy_day'))["energy_day__sum"]
        query_Sum = query_Sum_night+query_Sum_day

        price_Sum_night = float(query_Sum_night) * NIGHT_ELECTRO_PRICE
        price_Sum_day = float(query_Sum_day) * DAY_ELECTRO_PRICE
        price_Sum = price_Sum_night + price_Sum_day

        queryset_meter = electrozones.objects.all().filter(created_date__month__lte = month,created_date__year__lte = year)
        meter_Sum_night = float(queryset_meter.aggregate(Sum('energy_night'))["energy_night__sum"]) + NIGHT_ELECTRO_METER_0
        meter_Sum_day = float(queryset_meter.aggregate(Sum('energy_day'))["energy_day__sum"]) + DAY_ELECTRO_METER_0
        meter_Sum = meter_Sum_day + meter_Sum_night

        return render_to_response('electro_zones.html', { 'queryset':queryset, 'energy_sum_night': query_Sum_night, 
        'energy_sum_day': query_Sum_day, 'energy_sum': query_Sum ,
        'price_sum_day': price_Sum_day, 'price_sum': price_Sum ,
        'price_sum_night': price_Sum_night, 'day_electro_meter': meter_Sum_day, 'night_electro_meter': meter_Sum_night,
        'electro_meter': meter_Sum
        })
    except:
        return render_to_response('electro_zones.html')



from django.http import HttpResponse
logger = logging.getLogger(__name__)
def index(request):
    logger.error("Test!!")
    return HttpResponse("Hello logging world.")




@login_required
def temperature(request):
    
    with open('/home/pi/iot/myhome/myhome/humidity.csv', 'r') as f:
        opened_file = f.readlines()
        var = opened_file[-1].split(',')
        print(var)
        
    return render(request, "temperature.html", {'temperature':var[2],'humidity':var[3] , 'time':var[1]} )