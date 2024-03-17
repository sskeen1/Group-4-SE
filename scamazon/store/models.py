from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUser(AbstractUser):
    type = models.CharField(max_length=10);

class Book(models.Model):
    title = models.CharField(max_length=200);
    author = models.CharField(max_length=200);
    isbn = models.CharField(max_length=13);
    pages = models.IntegerField(default=0, validators = [MinValueValidator(0)]);
    rating = models.FloatField(default=0, validators = [MinValueValidator(0), MaxValueValidator(5.0)]);
    price = models.FloatField(default = 0, validators = [MinValueValidator(0)]);
    description = models.CharField(default = None, blank = True, null = True, max_length = 1500);

    def __str__(self):
        return self.title + " by " + self.author

    def is_highly_rated(self):
        return self.rating >= 4;
