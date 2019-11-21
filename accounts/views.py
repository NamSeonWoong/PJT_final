from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import UserCustomCreationForm
from .models import User

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == "POST":
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserCustomCreationForm()
    context={
        'form':form
    }
    return render(request,'accounts/forms.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context={
        'form':form
    }
    return render(request,'accounts/forms.html',context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')

def index(request):
    user_model = get_user_model()
    user_list = user_model.objects.all()
    context = {
        'user_list':user_list
    }
    return render(request, 'accounts/index.html', context)
def detail(request, id):
    user_model = get_user_model()
    user_info = get_object_or_404(user_model, id=id)

    context= {
        'user_info':user_info
    }
    return render(request,'accounts/detail.html', context)

def follow(request, id):
    you = get_object_or_404(User, id=id)
    me = request.user
    if not you==me:
        if me in you.followers.all():
            you.followers.remove(me)
        else:
            you.followers.add(me)
            # me.followings.add(you)

    return redirect('accounts:detail', id)