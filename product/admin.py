from django.contrib import admin
from product.models import Product
from apitest.models import Apitest,Apis

class ApisAdmin(admin.TabularInline):
    list_display=['apiname', 'apiurl', 'apiparamvalue', 'apimethod', 'apiresult', 'apistatus', 'create_time', 'id', 'product']
    modle = Apis
    extra = 1

class ProductAdmin(admin.ModelAdmin):

    list_display = ['productname', 'productdesc', 'producter', 'create_time', 'id']
    inlines = [ApisAdmin]

admin.site.register(Product)

# Register your models here.
