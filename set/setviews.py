from django.shortcuts import render
from set.models import Set
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def set_manage(request):

    username = request.session.get('user', '')
    set_list = Set.objects.all()
    # 定义流程接口数据的变量并返回到前端
    return render(request, "set_manage.html", {"user": username, "sets": set_list})

def set_user(request):

    user_list = User.objects.all()
    username = request.session.get('user', '')
    return render(request, "set_user.html", {'user':username, 'users': user_list})
# Create your views here.

@login_required
def setsearch(request):
    username = request.session.get('user', '')
    search_setname = request.GET.get("setname", "")
    set_list = Set.objects.filter(setname__icontains=search_setname)
    return render(request, 'set_manage.html', {"user": username, "sets": set_list})

