from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.router, name="router"),
    path("accounts/signup/", views.signup, name="signup"),
    path("buyer/", views.buyer_dashboard, name="buyer_dashboard"),
    path("seller/", views.seller_dashboard, name="seller_dashboard"),
    path("browse-books/", views.browse_books, name='browse-books'),
    path("browse-authors/", views.browse_authors, name='browse_authors'),
    path("books/<str:isbn>/", views.book, name="book-view"),
    path("author/<str:author>/", views.author, name="author-view"),
    path("cart/", views.pull_cart, name="cart"),
    path("add_cart/<str:isbn>",views.add_cart, name="add_cart"),
    path("remove_cart/<str:isbn>", views.remove_cart, name="remove_cart"),
    path("search/", views.search, name="search"),
    path("seller/listings/<str:id>", views.seller_listing, name="seller_listing"),
    path("seller/add_listing/<str:isbn>", views.add_listing, name="add_listing"),
    path("seller/add_listing", views.add_listing, name="add_listing"),
    path("seller/add_book", views.add_book, name="add_book")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
