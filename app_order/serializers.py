from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Order, RatingCommentCustomer




class OrderSerializer(ModelSerializer):
    class Meta:
        model =  Order
        fields = ['id', 'customer','company_name','product_category','ad_id', 'company', 'product_code', 'product_name','phone', 'price', 'order_status','quantity', 'create_at', 'update_at' ]
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class OrderListSerializer(ModelSerializer):
    first_name = SerializerMethodField()
    last_name = SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer','company_name','product_category','ad_id', 'first_name', 'last_name', 'company', 'product_code', 'product_name', 'phone', 'price', 'order_status', 'quantity', 'create_at', 'update_at']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_first_name(self, obj):
        return obj.customer.first_name

    def get_last_name(self, obj):
        return obj.customer.last_name
    

class RatingCommentCustomerByCreateSerialzer(ModelSerializer):
    class  Meta:
        model =  RatingCommentCustomer
        fields =  "__all__"
        extra_kwargs = {
            'id': {'read_only': True}
        }
    def create(self, validated_data):
        return RatingCommentCustomer.objects.create(**validated_data)



class RatingCommentCustomerByListSerializer(ModelSerializer):
    first_name  =  SerializerMethodField()
    last_name  =  SerializerMethodField()

    class Meta:
        model =  RatingCommentCustomer
        fields = ["first_name", "last_name","customer",  "product_category", "ad_id", "rating", "rating_company" , "comment", "create_date", "company_stir" ]  
  

    def get_first_name(self, obj):
        return obj.customer.first_name
    
    def get_last_name(self, obj):
        return obj.customer.last_name
