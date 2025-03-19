from django.contrib import admin

from .models import CatalogUsers, Profile, ONEID
# Register your models here.

admin.site.register(CatalogUsers)
admin.site.register(Profile)
admin.site.register(ONEID)
