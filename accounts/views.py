from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
import uuid
from django.conf import settings

from django.contrib.auth import authenticate, login
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            messages.error(request, "USer not found")
            return redirect('/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.error(request, "User email is not verified. Please check your mail")
            return redirect("/login")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "username or password is not correct")
            return redirect('/login')

        user_login(request, user)
        return redirect('/home')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, "Username is taken")
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request, "email is taken")
                return redirect('/register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/token-send')

        except Exception as e:
            print(e)

    return render(request, 'register.html')


def logout(request):
    user_logout(request)
    return redirect('/login')


@login_required(login_url='/')
def login_success(request):
    return render(request, 'login_success.html')


def success(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token_send.html')


def verify(request, auth_token):
    try:
        profile = Profile.objects.filter(auth_token=auth_token).first()
        if profile:
            if profile.is_verified:
                messages.success(request, "Your account has be already verified")
                return redirect('/login')
            profile.is_verified = True
            profile.save()
            messages.success(request, "Your account is verified")
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)


def send_mail_after_registration(email, token):
    subject = "Your account needs to be veriffied"
    messages = f"hi please click the link to verify your account http://127.0.0.1:8000/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_email = [email]
    send_mail(subject, messages, email_from, recipient_email)


def error_page(request):
    return render(request, 'error.html')


def home(request):
    return render(request, "home.html")
