from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class WeaponsAd(models.Model):
    SELL = 'sell'
    BUY = 'buy'

    AD_Types = [
        (SELL,'Sell'),
        (BUY,'Buy')
    ]

    ad_type = models.CharField(max_length=4,choices=AD_Types)
    weapon_name = models.CharField(max_length=50)
    price = models.FloatField(default=1, null=True, blank=True)
    description = models.TextField(blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='WeaponZ/',blank=True,null=True,default='WeaponZ/1.jpg')
    
    def __str__(self):
        return f"{self.ad_type} - {self.weapon_name} by {self.user.username}"


class DiscountCode(models.Model):
    code = models.CharField(max_length=100,)
    discount_percent = models.FloatField(default=0)
    expiry_date = models.DateTimeField()
    is_valid = models.BooleanField(default=True)


    def __str_(self):
        return f"{self.code} - {self.discount_percent}% - {self.expiry_date}"
