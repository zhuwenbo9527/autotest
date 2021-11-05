from django.contrib import admin
from apitest.models import Apitest, Apistep, Apis, Users

# Register your models here.
class ApistepAdmin(admin.TabularInline):
    list_display = ['id', 'waittime', 'title', 'url', 'apimethod', 'apiparamvalue', 'exceptresponse', 'actualresponse', 'result', 'apistatus', 'create_time']
    model = Apistep
    extra = 1

class ApitestAdmin(admin.ModelAdmin):
    list_display = ['id',  'apitestfeature', 'apiteststory', 'apitester', 'apitestresult', 'create_time']
    inlines = [ApistepAdmin]

class ApisAdmin(admin.ModelAdmin):
    list_displya = ['id', 'feature', 'story', 'title', 'link', 'issue', 'url', 'mehtod', 'headers', 'apiparamvalue', 'apimethod', 'enable',  'exceptresponse', 'actualresponse', 'result', 'tester', 'create_time']

class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'environment'  'name', 'merchantcode', 'username', 'password', 'token', 'creator', 'create_time']


admin.site.register(Apitest, ApitestAdmin)
admin.site.register(Apis)
admin.site.register(Users)
