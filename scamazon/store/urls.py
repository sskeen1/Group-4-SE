from django.urls import path

from . import views

urlpatterns = [
    path("", views.router, name="router"),
    path("accounts/signup/", views.signup, name="signup"),
    path("buyer/", views.buyer_dashboard, name="buyer_dashboard"),
    path("seller/", views.seller_dashboard, name="seller_dashboard"),
]