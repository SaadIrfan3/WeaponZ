from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/mainpage/',views.main_page,name = 'mainpage'),
    path('api/signup/',views.signup_page,name = 'signup'),
    path('api/login/',views.login_page,name = 'login'),
    path('api/shop/',views.shop_weapons,name = 'shop'),
    path('api/shopsell/',views.sell_weapons,name='sellweapons'),
    path('api/shopbuy/',views.buy_weapons,name='buyweapons'),
    path('api/discountpage/',views.discount_page,name='discountpage'),
    path('api/createpayment/',views.create_payment,name='createpayment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)