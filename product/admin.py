from django.contrib import admin
from product.models import Product
from apitest.models import Apitest,Apis
from apptest.models import Appcase
from webtest.models import Webcase

class ApisAdmin(admin.TabularInline):
    list_display=['apiname', 'apiurl', 'apiparamvalue', 'apimethod', 'apiresult', 'apistatus', 'create_time', 'id', 'product']
    modle = Apis
    extra = 1

class ProductAdmin(admin.ModelAdmin):

    list_display = ['productname', 'productdesc', 'producter', 'create_time', 'id']
    inlines = [ApisAdmin]

admin.site.register(Product)

class AppcaseAdmin(admin.TabularInline):
    list_display = ['appcasename', 'apptestresult', 'create_time', 'id', 'preoduct']
    model = Appcase
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc', 'create_time', 'id']
    inlines = [AppcaseAdmin]

class WebcaseAdmin(admin.TabularInline):
    list_display=['webcasename', 'webtestresult', 'create_time', 'id', 'product']
    model = Webcase
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc', 'create_time', 'id']
    inlines = [WebcaseAdmin]

# Register your models here.
