from django.contrib import admin

from .models import Book, Cart, Listing

admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Listing)
