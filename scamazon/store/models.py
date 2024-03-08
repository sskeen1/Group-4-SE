from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200);
    author = models.CharField(max_length=200);
    isbn = models.CharField(max_length=13, primary_key=True);
    pages = models.IntegerField(default=0);
    rating = models.IntegerField(default=0);
    quantity = models.IntegerField(default=1);

    def __str__(self):
        return self.title + " by " + self.author

    def is_highly_rated(self):
        return self.rating >= 4;

class Cart(models.Model):
    listingID = models.CharField(max_length=20);
    quantity = models.IntegerField(default=1);
    userID = models.CharField(max_length=20);

class Listing(models.Model):
    listingID = models.CharField(max_length = 13, primary_key=True);
    book = models.ForeignKey(Book, null =True, )
    quantity = models.IntegerField(default = 1);
    userID = models.CharField(max_length=20);
    price = models.FloatField();


