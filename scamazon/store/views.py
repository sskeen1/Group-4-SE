from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth.models import Group


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('router')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def router(request):
    num_books = Book.objects.all().count()

    context = {
        'num_books': num_books,
        'user_type': request.user.type,
    }

    if (request.user.type == "Buyer"):
        return redirect('buyer_dashboard')
    
    elif (request.user.type =="Seller"):
        return redirect('seller_dashboard')

    else:
        return redirect('signup')
    
@login_required
def buyer_dashboard(request):
    num_books = Book.objects.all().count()

    context = {
        'num_books': num_books,
        'user_type': request.user.type,
    }

    return render(request, 'buyer_dashboard.html', context=context)

@login_required
def seller_dashboard(request):
    num_books = Book.objects.all().count()

    context = {
        'num_books': num_books,
        'user_type': request.user.type,
    }

    return render(request, 'seller_dashboard.html', context=context)

@login_required
def browse_books(request):
    book_list = Book.objects.all()
    context = {
        "book_list" : book_list,
    }
    return render(request, 'browse_books.html', context = context)
    
