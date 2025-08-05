from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

# Create your views here.

@csrf_exempt
def main_page(request):
    return render(request,'core/mainpage.html')

@csrf_exempt
def signup_page(request):
    if request.method == 'POST':

        username = request.POST.get('username') or request.GET.get('username')
        email = request.POST.get('email') or request.GET.get('email')
        password = request.Post.get('password') or request.Get.get('password')

        if not username or not email or not password:
            return JsonResponse({'message': 'PLez enter all credentials'})
        if User.objects.filter.get(username=username).exists() or User.objects.filter.get(email=email):
            return JsonResponse({'message': 'username or email already exists'})
        User.objects.create_user(
        username=username,
        email=email,
        password=password)

        return redirect('login')
    return render(request,'core/signup.html')

@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username') or request.GET.get('username')
        email = request.POST.get('email') or request.GET.get('email')
        password = request.POST.get('password') or request.POST.get('password')

        if not username or not email or not password:
            return JsonResponse({'message': 'Please enter the correct credentials to login'})
        user = authenticate(username=username,email=email,password=password)
        if user is not None:
            login(request,user)
            return (request,'core/shop.html')
        else:
            return JsonResponse({'error': 'invalid credentials bro'})
    return render(request,'core/login.html')

@csrf_exempt
def shop_weapons(request):
    return render(request,'core/shop.html')

