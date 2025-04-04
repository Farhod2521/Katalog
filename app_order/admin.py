from django.contrib import admin
from .models import Order, RatingCommentCustomer


class CompanyFilter(admin.SimpleListFilter):
    title = "Company"
    parameter_name = "company"

    def lookups(self, request, model_admin):
        companies = Order.objects.values_list("company", flat=True).distinct()
        return [(company, company) for company in companies]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(company=self.value())
        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "company","company_name","product_name", "price", "quantity", "order_status", "create_at")
    list_filter = (CompanyFilter, "order_status")


admin.site.register(RatingCommentCustomer)
# Register your models here.
