from django.urls import path

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
]
