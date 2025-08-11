from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .models import WeaponsAd
# Create your views here.

@csrf_exempt
def main_page(request):
    return render(request,'core/mainpage.html')

@csrf_exempt
def signup_page(request):
    if request.method == 'POST':

        username = request.POST.get('username') or request.GET.get('username')
        email = request.POST.get('email') or request.GET.get('email')
        password = request.POST.get('password') or request.GET.get('password')

        if not username or not email or not password:
            return JsonResponse({'message': 'PLez enter all credentials'})
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
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
        user = authenticate(username=username,password=password)
        if user is not None: 
            login(request,user)
            request.session['coins'] = 1000
            return redirect('shop')
        else:
            return JsonResponse({'error': 'invalid credentials bro'})
        
    return render(request,'core/login.html')

@csrf_exempt
def sell_weapons(request):
    if request.method == 'POST':
        weapon_name= request.POST.get('weapon_name')
        price=request.POST.get('price')
        description=request.POST.get('description')
        image=request.FILES.get('image')

        if not request.user.is_authenticated:
            return JsonResponse({'message': 'plez login to post an ad'})
        WeaponsAd.objects.create(
            user=request.user,
            ad_type='sell',
            weapon_name=weapon_name,
            price=price,
            description=description,
            image=image,
        )
        return redirect('shop')
    return render(request,'core/sell.html')

@csrf_exempt
def buy_weapons(request):
    if request.method == 'POST':
        weapon_name = request.POST.get('weapon_name')
        price= request.POST.get('price')
        description=request.POST.get('description')
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'plez login first to buy uwu'})
        price = float(request.POST.get('price',0))
        coins = request.session.get('coins',0)

        if coins >=price:
            request.session['coins'] = coins - price

        WeaponsAd.objects.create(
            user=request.user,
            ad_type='buy',
            weapon_name = weapon_name,
            price= price,
            description = description
        )
        #return redirect('shop')
    ads = WeaponsAd.objects.filter(ad_type='sell').order_by('posted_at')
    return render(request, 'core/buy.html', {'ads': ads, 'coins': request.session.get('coins',0)})


@csrf_exempt
def shop_weapons(request):
    
    return render(request, 'core/shop.html',{'coins': request.session.get('coins',0)})




