from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUser(AbstractUser):
    type = models.CharField(max_length=10);

class Book(models.Model):
    title = models.CharField(max_length=200);
    author = models.CharField(max_length=200);
    isbn = models.CharField(max_length=13, primary_key=True);
    pages = models.IntegerField(default=0, validators = [MinValueValidator(0)]);
    rating = models.FloatField(default=0, validators = [MinValueValidator(0), MaxValueValidator(5.0)]);
    description = models.CharField(default = None, blank = True, null = True, max_length = 1500);


    def __str__(self):
        return self.title + " by " + self.author

    def is_highly_rated(self):
        return self.rating >= 4;


class Image(models.Model):
    image = models.ImageField(upload_to = '')


class Listing(models.Model):
    listingID = models.CharField(max_length = 13);
    isbn = models.ForeignKey(Book, null = True, on_delete=models.CASCADE);
    quantity = models.IntegerField(default = 1);
    userID = models.ForeignKey(CustomUser, null = True, on_delete=models.DO_NOTHING);
    price = models.FloatField(default = 0, validators = [MinValueValidator(0)]);
    image = models.ForeignKey(Image, null = True, on_delete=models.CASCADE);

class Cart(models.Model):
    listingID = models.ForeignKey(Listing, null = True, on_delete=models.CASCADE);
    quantity = models.IntegerField(default=1);
    userID = models.CharField(max_length=20);

class Order(models.Model):
    date = models.DateField();
    oldListingId = models.IntegerField(default=0);
    oldListingImage = models.ForeignKey(Image, null = True, on_delete=models.CASCADE);
    quantity = models.IntegerField(default=1);
    book = models.ForeignKey(Book, null = True, on_delete=models.CASCADE);
    price = models.FloatField(default = 0, validators = [MinValueValidator(0)]);
    buyer = models.ForeignKey(CustomUser, null = True, on_delete=models.DO_NOTHING, related_name='buyer');
    seller = models.ForeignKey(CustomUser, null = True, on_delete=models.DO_NOTHING, related_name='seller');
    delivered = models.BooleanField(default=False);
    address = models.CharField(max_length=200);
    payment = models.CharField(max_length=200);

    def get_payment_last_4_digits(self):
        return self.payment[-4:]
    
    def get_total_payment(self):
        return round(self.quantity * self.price, 2)