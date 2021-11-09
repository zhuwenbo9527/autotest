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
def apis_manage(request):
    username = request.session.get('user', '')
    apis_list = Apis.objects.all()
    apis_account = apis_list.count()
    apis_list, left_has_more, right_has_more, left_page_range, right_page_range, paginator = getpagemessage(request, apis_list)

    return render(request, "apis_manage.html", {'user': username, "apis": apis_list, "left_has_more": left_has_more, "right_has_more": right_has_more, "left_page_range": left_page_range,"right_page_range": right_page_range, "paginator":paginator, "apis_account":apis_account })

@login_required
def users_manage(request):
    username = request.session.get('user', '')
    users_list = Users.objects.all()
    return render(request, "users_manage.html", {'user': username, "users": users_list})


@login_required
def apissearch(request):
    username = request.session.get('user', '')
    search_feature = request.GET.get("feature", "")
    apis_list = Apis.objects.filter(feature__contains=search_feature)
    return render(request, 'apis_manage.html', {"user": username, "apis": apis_list})

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

class ApisView(ListView):
    model = Apis
    template_name = 'apis_manage.html'
    context_object_name = 'apis_manage'
    paginate_by = 10
    ordering = '-id'
    page_kwarg = 'page'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        context.update(self.get_pagination_data(paginator, page_obj))
        return context

    @staticmethod
    def get_pagination_data(paginator, page_obj, around=2):
        """这个分页算法的核心部分，其实仔细看看也不难"""
        current = page_obj.number  # 当前页码
        total = paginator.num_pages  # 总共的页码
        if current <= around + 3:
            left_has_more = False
            left_page_range = range(1, current)
        else:
            left_has_more = True
            left_page_range = range(current - around, current)
        if current >= total - around - 2:
            right_has_more = False
            right_page_range = range(current + 1, total + 1)
        else:
            right_has_more = True
            right_page_range = range(current + 1, current + around + 1)
        return {
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'left_page_range': left_page_range,
            'right_page_range': right_page_range
        }

