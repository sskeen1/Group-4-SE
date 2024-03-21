from django.contrib import admin

from .models import Book, Cart, Listing, CustomUser, Image

admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Listing)
admin.site.register(CustomUser)
admin.site.register(Image)
