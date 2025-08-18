from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .models import WeaponsAd
from .models import DiscountCode
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware, is_naive
import stripe
from django.conf import settings



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
            request.session['coins'] = 3000
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
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'Please login first to buy uwu'})
        if not request.user.is_superuser:
            return JsonResponse({'message': 'Only admin can create discount codes!'})

        weapon_name = request.POST.get('weapon_name')
        description = request.POST.get('description')
        discount_code = request.POST.get('discount_code', '').strip()

        # Price handling
        try:
            base_price = float(request.POST.get('price', 0))
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            return JsonResponse({'message': 'Invalid price value.'})

        coins = request.session.get('coins', 0)
        price = base_price * quantity
        # Check discount code
        if discount_code:
            try:
                discount_obj = DiscountCode.objects.get(code=discount_code, is_valid=True)

                # Expiry check (inclusive, so code works until exact expiry time)
                if discount_obj.expiry_date >= timezone.now():
                    discount_percent = getattr(discount_obj, 'discount_percent', 0)
                    if discount_percent > 0:
                        price = price - (price * discount_percent / 100)
                else:
                    return JsonResponse({'message': 'Discount code expired!'})
            
            except DiscountCode.DoesNotExist:
                return JsonResponse({'message': 'Invalid discount code!'})

        # Check if user has enough coins
        if coins < price:
            return JsonResponse({'message': 'Not enough coins!'})

        # Deduct coins and update session
        request.session['coins'] = coins - price

        # Record the purchase
        WeaponsAd.objects.create(
            user=request.user,
            ad_type='buy',
            weapon_name=weapon_name,
            price=price,
            description=f"{description} (x{quantity})"
        )

        return JsonResponse({   
            'message': f'Successfully bought {weapon_name} for {price} coins.',
            'remaining_coins': request.session['coins']
        })

    # GET request → show available ads
    ads = WeaponsAd.objects.filter(ad_type='sell').order_by('posted_at')
    return render(request, 'core/buy.html', {
        'ads': ads,
        'coins': request.session.get('coins', 0)
    })



@csrf_exempt
def shop_weapons(request):
    
    return render(request, 'core/shop.html',{'coins': request.session.get('coins',0)})

@csrf_exempt
def discount_page(request):
 
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_percent = float(request.POST.get('discount_percent', 0))
        expiry_date_str = request.POST.get('expiry_date')

        try:
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            return JsonResponse({'message': 'Invalid expiry date format!'})

        # Make datetime timezone-aware
        if is_naive(expiry_date):
            expiry_date = make_aware(expiry_date)

        DiscountCode.objects.create(
            code=code,
            discount_percent=discount_percent,
            expiry_date=expiry_date,
            is_valid=True
        )
       
    discount_codes = DiscountCode.objects.all().order_by('expiry_date')
    return render(request, 'core/discountpage.html',{'discount_coupen': discount_codes})


stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment(request):
    if request.method == "POST" or "GET":
        try:
            intent = stripe.PaymentIntent.create(
                amount=1000,
                currency="usd",
                automatic_payment_methods={"enabled": True},
            )
            return JsonResponse({"clientSecret": intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)




