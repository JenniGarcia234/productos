from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):

   user = models.OneToOneField(User,on_delete=models.CASCADE)
   username = models.CharField(max_length=25,null=True)
   dob = models.DateField(blank=True,null=True)  # If no date is selected then Django saves blank field value.
   city = models.CharField(max_length=25)
   contactno = models.CharField(max_length=25)
   portfolio_site = models.URLField(blank=True)
   gender = models.CharField(max_length=150, null=True)
   grade = models.CharField(max_length=150, null=True)
   image = models.ImageField(null=True,upload_to='images/', default = 'images/None/no-img.jpg',blank=True)


class Product(models.Model):
    product_name = models.CharField(max_length=250)
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to="products/%Y/%m/%d")
    size=models.IntegerField(null=True)
    width=models.IntegerField(null=True)
    details = models.CharField(max_length=500)
    def __str__(self):
      return self.product_name
    

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.FloatField()
    size=models.IntegerField(null=True)
    width=models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    