from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from .models import Order, RatingCommentCustomer
from  .serializers import(
     OrderSerializer, OrderListSerializer,
       RatingCommentCustomerByCreateSerialzer,
         RatingCommentCustomerByListSerializer
        
)

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404



class RatingCommentCustomerCreateAPIView(CreateAPIView):
    serializer_class =  RatingCommentCustomerByCreateSerialzer
    queryset =  RatingCommentCustomer.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer  =  RatingCommentCustomerByCreateSerialzer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

@api_view(['POST'])
def ratingcommentlistApi(request):
    product_category = request.data.get("product_category")
    ad_id = request.data.get("ad_id")
    
    if product_category and ad_id:
        try:
            queryset = RatingCommentCustomer.objects.filter(product_category=product_category, ad_id=ad_id)
            if queryset.exists():
                serializer = RatingCommentCustomerByListSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"result": "not found"}, status=status.HTTP_404_NOT_FOUND)
        except RatingCommentCustomer.DoesNotExist:
            return Response({"result": "not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"result": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"result": "E'lon id va category yuboring !!!"}, status=status.HTTP_400_BAD_REQUEST)

    


class OrderCreateAPIView(CreateAPIView):
    serializer_class =  OrderSerializer
    queryset =  Order.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer  =  OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    def get_queryset(self):
        token = self.request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_stir = payload['company_stir']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')

        queryset = Order.objects.filter(company=user_stir).order_by("-create_at")
        # serializer = self.get_serializer(queryset, many=True)
        return queryset
    


@api_view(['POST'])    
def order_company_status(request, pk):
    token = request.META.get('HTTP_TOKEN')
    if not token:
        raise AuthenticationFailed('Invalid token, login again, please')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token expired, login again, please')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token, login again, please')
    order = get_object_or_404(Order, id=pk)
    order_status = request.data.get("order_status")

    if order_status == "accepted":
        order.order_status = "accepted"
        order.save()
        return Response(data={"result": "Qabul qilindi !!!"})
    elif order_status == "sent":
        order.order_status = "sent"
        order.save()
        return Response(data={"result": "Yuborildi !!!"})
    elif order_status == "canceled":
        order.order_status = "canceled"
        order.save()
        return Response(data={"result": "Bekor qilindi !!!"})
    elif order_status == "customer_canceled":
        order.order_status = "customer_canceled"
        order.save()
        return Response(data={"result": "Bekor qilindi !!!"})
    elif order_status == "on_way":
        order.order_status = "on_way"
        order.save()
        return Response(data={"result": "Yuborilmoqda !!!"})
    elif order_status == "customer_accepted":
        order.order_status = "customer_accepted"
        order.save()
        return Response(data={"result": "Mijoz qabul qildi  !!!"})
    else:
        return Response(data={"result": "Topilmadi "})
    

    

class OrderCustomerListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    queryset =  Order.objects.all()
    def get_queryset(self):
        token = self.request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            pin = payload['id']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')

        queryset = Order.objects.filter(customer_id=id).order_by("-create_at")
        return queryset    






from django.db.models import Avg
class RatingCompany(APIView):
    serializer_class = RatingCommentCustomerByListSerializer

    def get(self, request, *args, **kwargs):
        keyword = self.kwargs["stir"]
        if keyword:
            ratings = RatingCommentCustomer.objects.filter(company_stir=keyword)
            average_rating = ratings.aggregate(Avg("rating"))["rating__avg"]
            serialized_ratings = self.serializer_class(ratings, many=True).data
            result = {
                "average_rating": average_rating if ratings.exists() else "Tovor sotilmagan",
                
            }
            return Response(result)
        else:
            return Response(data={"result": "not found"}, status=404)



from django.http import HttpResponse
from openpyxl import Workbook
class OrderCompanyExcel(ListAPIView):
    def get_queryset(self):
        token = self.request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_stir = payload['company_stir']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')

        queryset = Order.objects.filter(company=user_stir).order_by("-create_at")

        return self.generate_excel(queryset)

    def generate_excel(self, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = "Orders"
        headers = [
             "Mijoz", "Mahsulot kod", "Mahsulot nomi", 
          "Narx", "Soni", "Telfon raqam",  "Sana",
        ]
        ws.append(headers)
        for order in queryset:
            ws.append([
                order.customer.first_name if order.customer else "N/A",  # Assuming customer is a user model with a username
                order.product_code,
                order.product_name,
                order.price,
                order.quantity,
                order.phone,
                order.create_at.strftime('%Y-%m-%d %H:%M:%S')  # Formatting datetime for readability
           
            ])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=orders.xlsx'
        wb.save(response)
        return response
