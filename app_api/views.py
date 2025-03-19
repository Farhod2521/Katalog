
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import logging
import json
import requests
from datetime import date
from django.db import connection
from django.http import HttpResponse, HttpResponseNotFound

currency_names =  {
    'USD': 12625.150,
    'RUB': 143.1545
}

from .filters import SelectedThingsFilterBackend, SearchedThingsFilterBackend
from .models import CustomLanguages,Material_Soliq_Price ,SelectedThings, ResourcesList4Search,TexnikJTSA ,Bojxona, BojxonaCategory, Iqtisod_Moliya,Document_Category, Document
from .serializers import (
    CustomLanguagesSerializer, SelectedThingsSerializer, TexnikJTSASerializer,BojxonaSerializer, SelectedThingsALLSerializer,
      BojxonaCategorySerializer,SearchedResourcesSerializer, 
Iqtisod_Moliya_Serializer, ConstructionDataSerializer, 
DocumentCategorySerializer, DocumentSerializer, Material_Soliq_PriceSerializer
      )


from config.pagination import LimitlessPagination, CustomPagination

from app_materials.models import MatVolumes, MatCategories, MatGroups, Materials, MaterialAds
from app_materials.serializers import MatVolumesSerializer, MatCategoriesSerializer, MatGroupsSerializer

from app_technos.models import TechnoVolumes, TechnoCategories, TechnoGroups, Techno, TechnoAds
from app_technos.serializers import TechnoVolumesSerializer, TechnoCategoriesSerializer, TechnoGroupsSerializer

from app_machines_and_mechanisms.models import MMechanoCategories, MMechanoGroups, MMechano, MMechanoAds
from app_machines_and_mechanisms.serializers import MMechanoCategoriesSerializer, MMechanoGroupsSerializer

from app_small_mechanisms.models import SmallMechanoCategories, SmallMechanoGroups, SmallMechano, SmallMechanoAds
from app_small_mechanisms.serializers import SmallMechanoCategoriesSerializer, SmallMechanoGroupsSerializer

from app_works.models import WorkCategories, WorkGroups, Work, WorkAds
from app_works.serializers import WorkCategoriesSerializer, WorkGroupsSerializer

from app_company.models import Companies


resource_types = {'material': 'material_ads', 'techno': 'techno_ads', 'work': 'work_ads', 'mmechano': 'mmechano_ads', 'smallmechano': 'smallmechano_ads'}



from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta
from rest_framework.views import APIView




class Material_Soliq_PriceListView(ListAPIView):
    serializer_class = Material_Soliq_PriceSerializer
    pagination_class = CustomPagination
    queryset   =  Material_Soliq_Price.objects.all()


class DocumentCategoryCreateView(CreateAPIView):
    queryset = Document_Category.objects.all()
    serializer_class = DocumentCategorySerializer

# CreateView for Document
class DocumentCreateView(CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentListView(ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer










class ConstructionDataView(APIView):


    def post(self, request, *args, **kwargs):
        inn = request.data.get("inn")
        certificate_number = request.data.get("certificate_number")

        # Bu yerda olingan ma'lumotlarni qayta ishlash mumkin
        # Misol uchun, tasdiqlash yoki ma'lumotlar bazasiga yozish

        if not inn or not certificate_number:
            return Response({"error": "INN va certificate_number kerak."}, status=status.HTTP_400_BAD_REQUEST)

        # Ma'lumotlarni tashqi URL ga yuborish
        external_url = "http://10.190.7.22:55550/api/construction/view"
        data = {
            "inn": inn,
            "certificate_number": certificate_number
        }
        try:
            external_response = requests.post(external_url, data=data)  # json -> data
            if external_response.status_code != 200:
                return Response({"error": "Tashqi so'rovda xatolik yuz berdi: Status kod - {}".format(external_response.status_code)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            external_response_data = external_response.json()
        except ValueError:
            return Response({"error": "Tashqi serverdan noto'g'ri formatdagi javob olindi."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Tashqi so'rovda xatolik yuz berdi: {}".format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Ma'lumotlarni qayta ishlash natijasi
        result = {
            "message": "Ma'lumot muvaffaqiyatli qabul qilindi.",
            "external_response": external_response_data
        }

        return Response(result, status=status.HTTP_200_OK)






class BojxonaListApiView2(ListAPIView):
    queryset = Bojxona.objects.all().order_by('-id')[:100] # Ma'lumotlarni tartiblash
    serializer_class = BojxonaSerializer







from rest_framework import status
from requests.auth import HTTPBasicAuth
class EHRequestView(APIView):
    def post(self, request):
        url = "https://iskm.egov.uz:9444/oauth2/token"
        data = {
            "grant_type": "password",
            "username": "qv-kommunal-institut",
            "password": "lL55OnHg22Qs5Xl9YQ6T",
        }
        auth = HTTPBasicAuth('C2VbEEXIMop5Prz1ob2qlLLcG2Ea', 'rGljitk1xXL6kFipKzckWGrPXQQa')

        try:
            response = requests.post(url, data=data, auth=auth)
            response_data = response.json()

            if response.status_code == 200:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EH_DataAPIView(APIView):
    def post(self, request, *args, **kwargs):
        url = "https://apimgw.egov.uz:8243/service/stat/ktyadr/v1"
        token = "eyJ4NXQiOiJNell4TW1Ga09HWXdNV0kwWldObU5EY3hOR1l3WW1NNFpUQTNNV0kyTkRBelpHUXpOR00wWkdSbE5qSmtPREZrWkRSaU9URmtNV0ZoTXpVMlpHVmxOZyIsImtpZCI6Ik16WXhNbUZrT0dZd01XSTBaV05tTkRjeE5HWXdZbU00WlRBM01XSTJOREF6WkdRek5HTTBaR1JsTmpKa09ERmtaRFJpT1RGa01XRmhNelUyWkdWbE5nX1JTMjU2IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJxdi1rb21tdW5hbC1pbnN0aXR1dCIsImF1dCI6IkFQUExJQ0FUSU9OX1VTRVIiLCJhdWQiOiJDMlZiRUVYSU1vcDVQcnoxb2IycWxMTGNHMkVhIiwibmJmIjoxNzI4MzgxMzU5LCJhenAiOiJDMlZiRUVYSU1vcDVQcnoxb2IycWxMTGNHMkVhIiwic2NvcGUiOiJkZWZhdWx0IiwiaXNzIjoiaHR0cHM6XC9cL2RlLmVnb3YudXo6OTQ0M1wvb2F1dGgyXC90b2tlbiIsImV4cCI6MTcyODM4NDk1OSwiaWF0IjoxNzI4MzgxMzU5LCJqdGkiOiI3OTBlMzkxZC05MDgzLTQ2Y2EtYjVjNi1iOTgyNzNmYzg3ZWYifQ.aLbCuyYcfBSVGAhdrFnxPjTokFI8uJzOjwtOaf3ZMcab3HhwinzAhKadAuM6qY89zuD31ODo3F0amC0sRcxja-qTt80cVpLzuuZKHaUeU_w5odD-Dnz1jMh0hCAUnXNFSWXjiRYCOlPaB0p_NsINDuP-OJ7b--Gapd3L7FQL58JuCFiiGr4Q5tSBcTg7a8nEDgggli1Do-zLlvOKRKlqK89mfsIIV5TSxEFfYCSsWou-OC1LATCjeRBFxdutaSCluVsuugB3-D729Nvy6uuuV_m_uurB9PmnHfFYZtVnRSCjKAWgnc373_Ek22JU367iCxVkaI4Cmj-0IqqXudwdLQ"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        inn = request.data.get("inn")
        if not inn:
            return Response({"error": "INN is required"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "inn": inn,
            "transaction_id": "123456",
            "sender_pinfl": "12345678901234",
            "purpose": "test",
            "consent": "true"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)







class BirjaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
       # token = request.META['HTTP_TOKEN']

       # if not token:
        #    raise AuthenticationFailed('Invalid token, login again, please')


        today = datetime.today().weekday()
        if today == 00:
            old_monday = datetime.today() - timedelta(days=7)
            old_friday = old_monday + timedelta(days=4)
        else:
            old_monday = datetime(2024, 12, 23)
            old_friday = datetime(2024, 12, 27)

        before_monday  = old_monday - timedelta(days=7)
        before_friday = before_monday + timedelta(days=4)
        url_change = f"http://10.190.4.38:4040/api/Construction/GetProductsByDate/1/5000/%20/{before_monday.strftime('%Y-%m-%d')}/{before_friday.strftime('%Y-%m-%d')}/%20/%20"
        url = f"http://10.190.4.38:4040/api/Construction/GetProductsByDate/1/5000/%20/{old_monday.strftime('%Y-%m-%d')}/{old_friday.strftime('%Y-%m-%d')}/%20/%20"
        
        response = requests.get(url)
        response1 = requests.get(url_change)


	          # JSON javoblarni olish
        data = response.json()
        data1 = response1.json()
        for item1 in data:
            for item2 in data1:
                if item1['name'] == item2['name']:
                    item1["changeSum"] = item1['price'] - item2['price']
                    item1["changePresent"] = "12%"
                else:
                    item1["changeSum"] = 0
                    item1["changePresent"] = 0

        return Response(data)







class VolumesListView(ListAPIView):
    pagination_class = LimitlessPagination
    
    def get_serializer_class(self):
        table_name = self.request.GET['key']
        
        if table_name == 'materials':
            serializer_class = MatVolumesSerializer
        elif table_name == 'technos':
            serializer_class = TechnoVolumesSerializer
        else:
            serializer_class = MatVolumesSerializer
        
        return serializer_class
    
    def get_queryset(self):
        table_name = self.request.GET['key']
        
        if table_name == 'materials':
            queryset = MatVolumes.objects.all().order_by('id')
        elif table_name == 'technos':
            queryset = TechnoVolumes.objects.all().order_by('id')
        else:
            queryset = MatVolumes.objects.none()
        return queryset


class CategoriesListView(ListAPIView):
    pagination_class = LimitlessPagination
    
    def get_serializer_class(self):
        table_name = self.request.GET['key']
        
        if table_name == 'materials':
            serializer_class = MatCategoriesSerializer
        elif table_name == 'technos':
            serializer_class = TechnoCategoriesSerializer
        elif table_name == 'machine-mechano':
            serializer_class = MMechanoCategoriesSerializer
        elif table_name == 'small-mechano':
            serializer_class = SmallMechanoCategoriesSerializer
        elif table_name == 'works':
            serializer_class = WorkCategoriesSerializer
        else:
            serializer_class = MatCategoriesSerializer
        
        return serializer_class
    
    def get_queryset(self):
        table_name = self.request.GET['key']
        
        if table_name == 'materials':
            fk = self.request.GET['parent']
            queryset = MatCategories.objects.filter(category_volume=fk).order_by('id')
        elif table_name == 'technos':
            fk = self.request.GET['parent']
            queryset = TechnoCategories.objects.filter(category_volume=fk).order_by('id')
        elif table_name == 'machine-mechano':
            queryset = MMechanoCategories.objects.all().order_by('id')
        elif table_name == 'small-mechano':
            queryset = SmallMechanoCategories.objects.all().order_by('id')
        elif table_name == 'works':
            queryset = WorkCategories.objects.all().order_by('id')
        else:
            queryset = MatCategories.objects.none()
        return queryset


class GroupsListView(ListAPIView):
    pagination_class = LimitlessPagination
    
    def get_serializer_class(self):
        table_name = self.request.GET['key']
        
        if table_name == 'materials':
            serializer_class = MatGroupsSerializer
        elif table_name == 'technos':
            serializer_class = TechnoGroupsSerializer
        elif table_name == 'machine-mechano':
            serializer_class = MMechanoGroupsSerializer
        elif table_name == 'small-mechano':
            serializer_class = SmallMechanoGroupsSerializer
        elif table_name == 'works':
            serializer_class = WorkGroupsSerializer
        else:
            serializer_class = MatGroupsSerializer
        
        return serializer_class
    
    def get_queryset(self):
        table_name = self.request.GET['key']
        
        if table_name == 'materials':
            fk = self.request.GET['parent']
            queryset = MatGroups.objects.filter(group_category=fk).order_by('id')
        elif table_name == 'technos':
            fk = self.request.GET['parent']
            queryset = TechnoGroups.objects.filter(group_category=fk).order_by('id')
        elif table_name == 'machine-mechano':
            fk = self.request.GET['parent']
            queryset = MMechanoGroups.objects.filter(group_category=fk).order_by('id')
        elif table_name == 'small-mechano':
            fk = self.request.GET['parent']
            queryset = SmallMechanoGroups.objects.filter(group_category=fk).order_by('id')
        elif table_name == 'works':
            fk = self.request.GET['parent']
            queryset = WorkGroups.objects.filter(group_category=fk).order_by('id')
        else:
            queryset = MatGroups.objects.none()
        return queryset


class CustomLanguagesListView(ListAPIView):
    pagination_class = LimitlessPagination
    queryset = CustomLanguages.objects.all()
    serializer_class = CustomLanguagesSerializer


@api_view(['GET', 'POST'])
def GetMenuTranslations(request):
    if request.method == 'GET':
        if 'lang' in request.GET:
            lang = request.GET['lang']
        else:
            lang = 'uz'
        if lang != 'en' and lang != 'uz' and lang != 'ru':
            lang = 'uz'
            
        sql = "SELECT key_name AS name, " + lang + " AS key_value FROM lang_translations;"
        obj = {}
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
            words = cursor.fetchall()
            for w in words:
                obj[w[0]] = w[1]
            # print(obj)
#        print(json.dumps(obj["materials"]))
        return HttpResponse(json.dumps(obj), content_type="application/json")
    elif request.method == 'POST':
        fields = dict(request.data)
        insert_SQL = ""
        for i in fields.keys():
            insert_SQL = insert_SQL + "INSERT INTO lang_translations(key_name, uz, en, ru) VALUES('{}', '{}', '{}', '{}');".format(i, i, i, i)
        try:
            with connection.cursor() as cursor:
                cursor.execute(insert_SQL)
            return HttpResponse(json.dumps({"result": "success"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"result": "error", "description": str(e)}), content_type="application/json")


@api_view(['GET'])
def GetAveragePrices(request):
    if 'resource' not in request.GET:
        return HttpResponse(json.dumps({"Error": "Invalid query params, see API documentation"}), content_type="application/json")
    else:
        csr_code = request.GET['resource']
        sql = "SELECT resource_code, resource_average_price, resource_current_average_price FROM csr_resources WHERE resource_code='{}';".format(csr_code)
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchone()
            
            if results is not None:
                return HttpResponse(json.dumps({"resource_code": results[0], "resource_average_price": results[1], "resource_current_average_price": results[2]}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"Error": "Invalid resource code"}), content_type="application/json")


class SelectedThingsSelectView(LoginRequiredMixin, CreateAPIView):
    queryset = SelectedThings.objects.all()
    serializer_class = SelectedThingsSerializer


@api_view(['GET'])
def SelectedThingsDeSelect(request, pk):
    if request.user.is_authenticated:
        sql_query = "SELECT id, user_id FROM selected_things WHERE id={};".format(pk)
        
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchone()
            
            if result is not None:
                if result[1] == request.user.id:
                    sql_deselect = "UPDATE selected_things SET deselected=1, deselected_time=CURRENT_TIMESTAMP WHERE id={} AND user_id={};".format(pk, request.user.id)
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(sql_deselect)
                            return HttpResponse(json.dumps({'result': 'deselected'}), content_type="application/json")
                    except:
                        return HttpResponse(json.dumps({'result': 'error', 'description': 'Internal server error'}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'result': 'error', 'description': 'This item isn\'t your!'}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"Result": "Error", 'description': 'Selections doesn\'t have which your query paramaters'}), content_type="application/json")
        return HttpResponse(json.dumps({'result': 'OK'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'result': 'error', 'description': 'You must be logged'}), content_type="application/json")


class SelectedThingsListView(LoginRequiredMixin, ListAPIView):
    serializer_class = SelectedThingsALLSerializer
    pagination_class = CustomPagination
    filter_backends = (SelectedThingsFilterBackend,)
    
    def get_queryset(self):
        queryset = SelectedThings.objects.filter(deselected=False)
        return queryset


class SearchedResourcesListView(ListAPIView):
    queryset = ResourcesList4Search.objects.all()
    serializer_class = SearchedResourcesSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchedThingsFilterBackend,)


@api_view(['GET'])
def getCurrencyCources(request):
    try:
        sana = date.today()
        API_CURRENCY = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/all/" + str(sana)
        COURSES = json.loads((requests.get(API_CURRENCY)).text)
        current_courses = {}
        for i in COURSES:
            if i['Ccy'] == "USD":
                current_courses['USD'] = i['Rate']
            elif i['Ccy'] == "RUB":
                current_courses['RUB'] = i['Rate']
            if len(current_courses) == 2:
                break
        currency_names = current_courses
        return Response(data=current_courses)
    except:
        return Response(data=currency_names)


# Hisobotlarni olish uchun
@api_view(['GET'])
def getStatistics(request):
    if request.method == 'GET':
        try:
            stat = {}
            stat["Materiallar va buyumlar"] = Materials.objects.all().count() - 24610
            stat["Materiallar va buyumlar e'lonlari"] = MaterialAds.objects.all().count()
            stat["E'lonlar orqali qamrab olingan material va buyumlar (unique)"] = MaterialAds.objects.values('material_name_id').distinct().count()
            
            stat["------------------------------ ------------------------------"] = "-"
            
            stat["Mashina va mexanizmlar"] = MMechano.objects.all().count()
            stat["Mashina va mexanizmlar e'lonlari"] = MMechanoAds.objects.all().count()
            stat["E'lonlar orqali qamrab olingan mashina va mexanizmlar (unique)"] = MMechanoAds.objects.values('mmechano_name_id').distinct().count()
            
            stat["------------------------ ------------------------------------"] = "-"
            
            stat["Qurilish ishlari"] = Work.objects.all().count()
            stat["Qurilish ishlari e'lonlari"] = WorkAds.objects.all().count()
            stat["E'lonlar orqali qamrab olingan qurilish ishlari (unique)"] = WorkAds.objects.values('work_name_id').distinct().count()
            
            stat["------------------------------------------ ------------------"] = "-"
            
            stat["Kichik mexanizatsiyalar"] = SmallMechano.objects.all().count()
            stat["Kichik mexanizatsiyalar e'lonlari"] = SmallMechanoAds.objects.all().count()
            stat["E'lonlar orqali qamrab olingan kichik mexanizatsiyalar (unique)"] = SmallMechanoAds.objects.values('smallmechano_name_id').distinct().count()
            
            stat["------------ ------------------------------------------------"] = "-"
            
            stat["Uskuna va qurilmalar"] = Techno.objects.all().count()
            stat["Uskuna va qurilmalar e'lonlari"] = TechnoAds.objects.all().count()
            stat["E'lonlar orqali qamrab olingan uskuna va qurilmalar (unique)"] = TechnoAds.objects.values('techno_name_id').distinct().count()
            
            stat["---------------------------------------------------------- --"] = "-"
            
            stat["Tizimga e'lonlari joylangan kompaniyalar soni"] = MaterialAds.objects.order_by().values('company_stir').distinct().count()
            
            return Response(data=stat)
        except:
            return Response(data={"Error": "Ma'lumotlarni olishda xatolik yuz berdi, keyinroq urinib ko'ring"})
    else:
        return HttpResponseNotFound()




class SoliqAPIView(APIView):
    def get(self, request, pk=None):
        url1 = f"https://mspd-api.soliq.uz/minstroy/construction/get-factura-list-by-catalog-code?catalogCode=00407001001000000&fromDate=01.06.2024&toDate=3.06.2024"
        response1 = requests.get(url1)

        if response1.status_code == 200:
            data1 = response1.json()
            return Response(data1)
        else:
            error_message = "Serverdan yaroqsiz javob qaytardi"
            return Response({'error': error_message}, status=response1.status_code)

    def post(self, request, mxik=None):
        # Retrieve mxik, fromDate, and toDate from the request data
        mxik = request.data.get("mxik")
        from_date = request.data.get("fromDate")
        to_date = request.data.get("toDate")

        # Validate the presence of mxik, fromDate, and toDate
        if not mxik:
            return Response({'error': 'mxik is required'}, status=400)
        if not from_date or not to_date:
            return Response({'error': 'Both fromDate and toDate are required'}, status=400)

        # Construct the URL dynamically with mxik, fromDate, and toDate
        url1 = f"https://mspd-api.soliq.uz/minstroy/construction/get-factura-list-by-catalog-code?catalogCode={mxik}&fromDate={from_date}&toDate={to_date}"
        response1 = requests.get(url1)

        # Handle the API response
        if response1.status_code == 200:
            data1 = response1.json()
            return Response(data1)
        else:
            error_message = "Serverdan yaroqsiz javob qaytardi"
            return Response({'error': error_message}, status=response1.status_code)













import requests
@api_view(["POST"])
def getCertificate(request):
    url = "http://10.190.7.22:55550/api/construction/view"
    inn =  request.data.get("inn")
    certificate_number =  request.data.get("certificate_number")
    if inn and certificate_number:
        data = {
        "inn": inn,
        "certificate_number": certificate_number
        }
        response = requests.post(url, data=data)
        return Response(response.text)
    return Response(data={
        "result":"Inn bilan Sertifikat raqamni yubor !!!",
        "message": "Xatolik"
    })









from rest_framework.authentication import TokenAuthentication
from django.utils import timezone


class BojxonaBulkCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Extract the relevant data from the request
            gtd_info = request.data.get('gtdInformation', {})
            data = gtd_info.get('declarationData', {})
            
            if not data:
                return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

            # Extract 'tovar' data and 'g15'
            tovars_data = data.pop('tovar', [])
            bj_id = data.get('id')  # Dynamically set bj_id from request data
            get15 = data.get('g15')  # Get 'get15' from the declarationData
            if not bj_id:
                return Response({"error": "'id' is required in the declarationData"}, status=status.HTTP_400_BAD_REQUEST)
            category, created = BojxonaCategory.objects.get_or_create(
                bj_id=bj_id,
                defaults={
                    'get15': get15,  # Set get15 in the BojxonaCategory model
                    'error': None  # Default value, update as needed
                }
            )
            for tovar_data in tovars_data:
                tovar_data['bj_category'] = category.id
                tovar_data['g31name'] = tovar_data.get('g31name')  # Ensure g31name is included
                serializer = BojxonaSerializer(data=tovar_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            response_data = {
                "id": category.id,
                "bj_id": bj_id,
                "error": "",
                "receive_time_org": timezone.now()  # Use timezone for datetime
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



    



class BojxonaListApiView(APIView):
    def get(self, request, *args, **kwargs):
        # Query the Bojxona data grouped by category
        bojxona_categories = BojxonaCategory.objects.all()
        response_data = []

        # Loop through each category
        for category in bojxona_categories:
            # Initialize the category-specific data structure
            category_data = {
                "gtdInformation": {
                    "declarationData": {
                        "date": category.date.strftime('%Y-%m-%d'),
                        "g15": category.get15 or "",
                        "tovar": [],
                        "id": category.bj_id
                    },
                    "Information_Date": timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }

            # Get all Bojxona objects related to the current category
            bojxona_objects = Bojxona.objects.filter(bj_category=category).order_by('-id')[:100]

            # Add Bojxona data to the tovar list
            for bojxona in bojxona_objects:
                tovar_data = {
                    "unit": bojxona.unit,
                    "codeName": bojxona.codeName,
                    "additionalUnit": bojxona.additionalUnit,
                    "codeTiftn": bojxona.codeTiftn,
                    "value": bojxona.value,
                    "g31name": bojxona.g31name,
                    "netMass": bojxona.netMass
                }
                category_data["gtdInformation"]["declarationData"]["tovar"].append(tovar_data)

            # Append the category data to the response
            response_data.append(category_data)

        # Return the response with the grouped data
        return Response(response_data, status=200)







class TexnikJTSAListApiView(ListAPIView):
    serializer_class = TexnikJTSASerializer
    queryset =  TexnikJTSA.objects.all()
    pagination_class = CustomPagination



class IQTISODMOLIYAVAZRILIKListApiView(ListAPIView):
    serializer_class = Iqtisod_Moliya_Serializer
    queryset =  Iqtisod_Moliya.objects.all()
    pagination_class = CustomPagination



class CreateMultiplePosts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        data_length = len(request.data)
        
        if data_length == 0:
            return Response({'error': 'At least 1 post is required.'}, status=status.HTTP_400_BAD_REQUEST)
        elif data_length > 50:
            return Response({'error': 'A maximum of 50 posts are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = Iqtisod_Moliya_Serializer(data=request.data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'{data_length} posts created successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


