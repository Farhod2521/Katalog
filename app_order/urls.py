from django.urls import path

from .views import(
     OrderCreateAPIView, 
     OrderListAPIView, OrderCustomerListAPIView,
    RatingCommentCustomerCreateAPIView, 
    order_company_status, ratingcommentlistApi, RatingCompany, OrderCompanyExcel
)
urlpatterns  = [
    path('order_status/<int:pk>/', order_company_status, name="order_company_status"),
    path('rating_comment/create/customer/', RatingCommentCustomerCreateAPIView.as_view()),
    path('rating_comment/list/customer/', ratingcommentlistApi),
    path('list/company/', OrderListAPIView.as_view()),
    path('list/customer/', OrderCustomerListAPIView.as_view()),
    path('new/add/', OrderCreateAPIView.as_view()),
    path('rating/company/<str:stir>/', RatingCompany.as_view()),
    path('excel/', OrderCompanyExcel.as_view()),

]
