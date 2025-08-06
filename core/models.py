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
    price = models.DecimalField(max_digits=4,decimal_places=2)
    description = models.TextField(blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.ad_type.title()} - {self.weapon_name} by {self.user.username}"

