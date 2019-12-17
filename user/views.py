from django.contrib.auth.forms import User
from django.contrib import messages
from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

def register(request):
    form = RegisterForm(request.POST or None)

    context = {
        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password = password
        newUser.save()

        messages.success(request, "Kayıt başarılı.")
        return redirect("user:login")
    
    return render(request, "register.html", context)

def loginUser(request): 
    form = LoginForm(request.POST or None)

    context = {
        "form":form
    }    

    if form.is_valid(): 
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)

        if user:    
            messages.success(request, "Giriş başarılı.")
            login(request, user)
            return redirect("index")
        else:   
             messages.error(request, "Kullanıcı adı veya şifre hatalı.")


    return render(request, "login.html", context)

@login_required(login_url = "user:login")
def logoutUser(request):    
    logout(request)
    messages.success(request, "Çıkış yapıldı.")
    return redirect("index")
