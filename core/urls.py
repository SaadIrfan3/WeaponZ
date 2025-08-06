from django.urls import path
from . import views

urlpatterns = [
    path('api/mainpage/',views.main_page,name = 'mainpage'),
    path('api/signup/',views.signup_page,name = 'signup'),
    path('api/login/',views.login_page,name = 'login'),
    path('api/shop/',views.shop_weapons,name = 'shop'),
    path('api/shopsell/',views.sell_weapons,name='sellweapons'),
    path('api/shopbuy/',views.buy_weapons,name='buyweapons')
]