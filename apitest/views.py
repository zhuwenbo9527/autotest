from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect #加入引用,
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from apitest.models import Apitest,Apistep,Apis,Users
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import ListView
import pymysql


def test(request):
    return HttpResponse("hello world") #返回Httpresponse


def home(request):
    return render(request, 'home.html')

def login(request):
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username,password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/home/')
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error'})
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


#接口管理
@login_required
def apitest_manage(request):
    # 读取所有流程接口数据
    apitests_list = Apitest.objects.all()
    apitests_count = apitests_list.count()
    # 浏览器登录session 
    username = request.session.get('user', '')
    apitest_list, left_has_more, right_has_more, left_page_range, right_page_range, paginator = getpagemessage(request,
                                                                                                                apitests_list)

    return render(request, "apitest_manage.html",
                  {'user': username, "apitests": apitest_list, "left_has_more": left_has_more,
                   "right_has_more": right_has_more, "left_page_range": left_page_range,
                   "right_page_range": right_page_range, "paginator": paginator, "apitests_count":apitests_count})


#接口步骤管理
@login_required
def apistep_manage(request):
    # 浏览器登录session
    username = request.session.get('user', '')
    apisteps_list = Apistep.objects.all()
    apisteps_count = apisteps_list.count()
    apisteps_list, left_has_more, right_has_more, left_page_range, right_page_range, paginator = getpagemessage(request,
                                                                                                    apisteps_list)

    return render(request, "apistep_manage.html",
                  {'user': username, "apisteps": apisteps_list, "left_has_more": left_has_more,
                   "right_has_more": right_has_more, "left_page_range": left_page_range,
                   "right_page_range": right_page_range, "paginator": paginator,"apisteps_count":apisteps_count})


def getpagemessage(request, message_list):
    paginator = Paginator(message_list, 20)
    page = request.GET.get('page', 1)
    currentPage = int(page)
    try:
        message_list = paginator.page(page)
    except PageNotAnInteger:
        message_list = paginator.page(1)
    except EmptyPage:
        message_list = paginator.page(paginator.num_pages)
    total = paginator.num_pages  # 总共的页码
    around = 2
    if currentPage <= around + 3:
        left_has_more = False
        left_page_range = range(1, currentPage)
    else:
        left_has_more = True
        left_page_range = range(currentPage - around, currentPage)
    if currentPage >= total - around - 2:
        right_has_more = False
        right_page_range = range(currentPage + 1, total + 1)
    else:
        right_has_more = True
        right_page_range = range(currentPage + 1, currentPage + around + 1)
    return message_list, left_has_more, right_has_more, left_page_range, right_page_range,paginator

@login_required
def apis_manage(request, apis_list=None, message=None):
    if apis_list :
        apis_list = apis_list
    else:
        apis_list = Apis.objects.filter(isdelete=0)
    username = request.session.get('user', '')
    apis_account = apis_list.count()
    apis_list, left_has_more, right_has_more, left_page_range, right_page_range, paginator = getpagemessage(request, apis_list)
    return render(request, "apis_manage.html", {'user': username, "apis": apis_list, "left_has_more": left_has_more, "right_has_more": right_has_more, "left_page_range": left_page_range,"right_page_range": right_page_range, "paginator":paginator, "apis_account": apis_account, "message":message })

@login_required
def users_manage(request):
    username = request.session.get('user', '')
    users_list = Users.objects.all()
    return render(request, "users_manage.html", {'user': username, "users": users_list})


@login_required
def apissearch(request):
    username = request.session.get('user', '')
    search_feature = request.GET.get("feature", "")
    apis_list = Apis.objects.filter(feature__contains=search_feature, isdelete=0)
    return apis_manage(request, apis_list=apis_list)

@login_required
def apitestsearch(request):
    username = request.session.get('user', '')
    search_apitestfeature = request.GET.get("apitestfeature", "")
    apitest_list = Apitest.objects.filter(apitestfeature__contains=search_apitestfeature)
    return render(request, 'apitest_manage.html', {"user": username, "apitests": apitest_list})

@login_required
def apistepsearch(request):
    username = request.session.get('user', '')
    search_title = request.GET.get("title", "")
    apistep_list = Apistep.objects.filter(title__contains=search_title)
    return render(request, "apistep_manage.html", {"user": username, "apistep_list": apistep_list})


@xframe_options_sameorigin
def left(request):
    return render(request, "left.html")
# Create your views here.



@xframe_options_sameorigin
def apis_add(request):
    return render(request, "apis_add.html")


def apis_add_submit(request):
    if request.POST:
        product_id = request.POST.get("Product")
        feature = request.POST.get("feature")
        story = request.POST.get("story")
        title = request.POST.get("title")
        link = request.POST.get("link")
        issue = request.POST.get("issue")
        url = request.POST.get("url")
        method = request.POST.get("method")
        headers = request.POST.get("headers")
        apiparamvalue = request.POST.get("apiparamvalue")
        enable = True if request.POST.get("enable") == "on" else False
        exceptresponse = request.POST.get("exceptresponse")
        tester = request.POST.get("tester")
        Apis.objects.create(Product_id=product_id, feature=feature, story=story, title=title, link=link, issue=issue, url=url,
                                   method=method, headers=headers, apiparamvalue=apiparamvalue, enable=enable, exceptresponse=exceptresponse, tester=tester)
    return apis_manage(request)

def apis_update_submit(request):
    if request.POST:
        id = request.POST.get("id")
        product_id = request.POST.get("Product")
        feature = request.POST.get("feature")
        story = request.POST.get("story")
        title = request.POST.get("title")
        link = request.POST.get("link")
        issue = request.POST.get("issue")
        url = request.POST.get("url")
        method = request.POST.get("method")
        headers = request.POST.get("headers")
        apiparamvalue = request.POST.get("apiparamvalue")
        enable = True if request.POST.get("enable") == "on" else False
        exceptresponse = request.POST.get("exceptresponse")
        tester = request.POST.get("tester")
        try:
            Apis.objects.filter(id=id).update(Product_id=product_id, feature=feature, story=story, title=title, link=link, issue=issue, url=url,
                                   method=method, headers=headers, apiparamvalue=apiparamvalue, enable=enable, exceptresponse=exceptresponse, tester=tester)
            return apis_manage(request, message="保存成功")
        except Except as e:
            return apis_manage(request, message="保存失败，"+str(e))


def apis_update(request):
    if request.GET:
        id = request.GET.get("id")
        api = Apis.objects.get(id=id)
    return render(request, "apis_update.html", {"api": api})

def apis_delete(request):
    if request.GET:
        id = request.GET.get("id")
        api = Apis.objects.get(id=id)
    return render(request, "apis_delete.html", {"api": api})

def apis_delete_submit(request):
    if request.POST:
        id = request.POST.get("id")
        Apis.objects.filter(id=id).update(isdelete = 1)
    return apis_manage(request, message="删除成功")