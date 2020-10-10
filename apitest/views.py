from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect #加入引用,
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from apitest.models import Apitest,Apistep,Apis
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pymysql


def test(request):
    return HttpResponse("hello world") #返回Httpresponse


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username,password = password)
        if user is not None and user.is_active:
            auth.login(request,user)
            request.session['user'] = username
            response = HttpResponseRedirect('/home/')
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error'})
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return render(request,'login.html')

#接口管理
@login_required
def apitest_manage(request):
    # 读取所有流程接口数据
    apitest_list = Apitest.objects.all()
    # 浏览器登录session 
    username = request.session.get('user','')
    # 定义流程接口数据的变量并返回到前端
    return render(request, "apitest_manage.html", {"user": username, "apitests": apitest_list})

#接口步骤管理
@login_required
def apistep_manage(request):
    # 浏览器登录session
    username = request.session.get('user', '')
    apistep_list = Apistep.objects.all()
    # 定义流程接口数据的变量并返回到前端
    return render(request, "apistep_manage.html", {"user": username, "apisteps": apistep_list})

@login_required
def apis_manage(request):
    username = request.session.get('user','')
    apis_list = Apis.objects.all()
    return render(request, "apis_manage.html", {'user': username, "apis": apis_list})

@login_required
def test_report(request):
    username = request.session.get('user','')
    apis_list = Apis.objects.all()
    apis_count = Apis.objects.all().count()
    db = pymysql.connect(user='root', db='autotest', passwd='123456', host='127.0.0.1')
    cursor = db.cursor()
    sql1 = 'Select count(id) From apitest_apis where apitest_apis.apistatus = 1'
    aa = cursor.execute(sql1)
    apis_pass_count = [row[0] for row in cursor.fetchmany(aa)][0]
    sql2 = 'Select count(id) From apitest_apis Where apitest_apis.apistatus=0'
    bb = cursor.execute(sql2)
    apis_fail_count = [row[0] for row in cursor.fetchmany(bb)][0]
    db.close()
    return render(request, "report.html", {"user":username, "apis":apis_list, "apiscounts": apis_count,
                                           "apis_pass_counts": apis_pass_count, "apis_fail_counts": apis_fail_count,
                                           })#把值赋给apiscounts变量
@login_required
def apisearch(request):
    username = request.session.get('user', '')
    search_apitestname = request.GET.get("apitestname", "")
    apitest_list = Apitest.objects.filter(apitestname__icontains=search_apitestname)
    return render(request, 'apitest_manage.html', {"user": username, "apitests": apitest_list})

@login_required
def apistepsearch(request):
    username = request.session.get('user', '')
    search_apitestname = request.GET.get("apitestname", "")
    apitestname_list = Apitest.objects.filter(apitestname__icontains=search_apitestname)
    return render(request, 'apistep_manage.html', {"user": username, "apisteps": apitestname_list})


def left(request):
    return render(request, "left.html")
"""
@login_required
def apitest_manage(request):
    apitest_list = Apitest.objects.all()
    username = request.session.get('user', '')
    paginator = Paginator(apitest_list, 8)
    page = request.Get.get('page', 1)
    currentPage=int(page)
    try:
        apitest_list = paginator.page(page)
    except PageNotAnInteger:
        apitest_list = paginator.page(1)
    except EmptyPage:
        apitest_list = paginator.page(paginator.num_pages)

    return render(request, " apitest_manage.html", {"user":username}, "apitest:apitest_list")
"""

# Create your views here.
