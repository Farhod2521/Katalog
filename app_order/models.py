from django.db import models
from django.contrib.auth import get_user_model
from app_company.models import Companies

from users.models import ONEID, CatalogUsers


ORDER_STATUS = (
    ('new_order', 'new_order'),
    ('accepted', 'accepted'),
    ('on_way', 'on_way'),    
    ('customer_accepted', 'customer_accepted'),
    ('sent', 'sent'),
    ('canceled', 'canceled'),
    ('customer_canceled', 'customer_canceled'),


)

PRODUCT_FILTER=  (
    ('material', 'material'),
    ('mmechano', 'mmechano'),
    ('smallmechano', 'smallmechano'),
    ('techno', 'techno'),
    ('work', 'work'),
)

class Order(models.Model):
    customer =  models.ForeignKey(CatalogUsers, on_delete=models.CASCADE)
    company =  models.CharField(max_length=9)
    company_name  =  models.CharField(max_length=300, null=True, blank=True)
    product_code =  models.CharField(max_length=200)
    product_name =  models.CharField(max_length=200)
    product_category = models.CharField(choices=PRODUCT_FILTER, max_length=20)
    ad_id =  models.IntegerField()
    price =  models.CharField(max_length=200)
    quantity = models.IntegerField()
    phone =  models.CharField(max_length=14)
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS, default="new_order")
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "app_orders"
        ordering = ['product_name', 'product_code']



from django.core.validators import MinValueValidator, MaxValueValidator
class RatingCommentCustomer(models.Model):
    customer =  models.ForeignKey(CatalogUsers, on_delete=models.CASCADE)
    company_stir =  models.CharField(max_length=9)
    product_category = models.CharField(choices=PRODUCT_FILTER, max_length=20)
    ad_id =  models.IntegerField()
    rating =  models.PositiveIntegerField(        
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    rating_company =  models.PositiveIntegerField(        
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    comment =  models.TextField(blank=True, null=True)
    create_date =  models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rating_comment"




    






        





    

# Create your models here.
