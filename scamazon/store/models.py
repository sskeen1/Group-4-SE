from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    type = models.CharField(max_length=10);

class Book(models.Model):
    title = models.CharField(max_length=200);
    author = models.CharField(max_length=200);
    isbn = models.CharField(max_length=13);
    pages = models.IntegerField(default=0);
    rating = models.IntegerField(default=0);
    price = models.FloatField();

    def __str__(self):
        return self.title + " by " + self.author

    def is_highly_rated(self):
        return self.rating >= 4;