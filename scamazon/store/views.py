from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Listing, Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm, CheckoutForm
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist


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
    book_list = Book.objects.all().order_by('title').values()
    context = {
        "book_list" : book_list,
    }
    return render(request, 'browse_books.html', context = context)

def browse_authors(request):
    authors = []
    temp_authors = Book.objects.order_by('author').values("author")
    for value in temp_authors:
        if value not in authors:
            authors.append(value)
    context = {
        'authors': authors,
    }
    return render(request, 'browse_authors.html', context = context)

@login_required
def book(request, isbn):
    try:
        book = Book.objects.get(isbn = isbn)
        listings_list = Listing.objects.filter(isbn = isbn).order_by('price')
        print(listings_list)
    except(ObjectDoesNotExist):
        return render(request, "null_book.html")
    
    context = {
        "book": book,
        "listing_list": listings_list,
            }

    return render(request, 'book.html', context = context)


@login_required
def add_cart(request,isbn):
    listing = get_object_or_404(Listing, isbn=request.POST.get('book_id'))
    cart = Cart.objects.filter(userID=request.user.username).values('listingID')
    cartlistings = Listing.objects.filter(id__in=cart)

    if listing in cartlistings:
        return redirect('cart')
    else:
        p = Cart.objects.create(listingID=listing, quantity=1, userID=request.user.username)
        return redirect('cart')

@login_required
def remove_cart(request,isbn):
    listing = get_object_or_404(Listing, isbn=request.POST.get('book_id'))
    cart = Cart.objects.filter(userID=request.user.username).values('listingID');
    cartlistings = Listing.objects.filter(id__in=cart)

    if listing in cartlistings:
        p = Cart.objects.filter(listingID=listing, quantity=1, userID=request.user.username).delete()
        return redirect('cart')
    else:
        return redirect('cart')

@login_required
def checkout(request):
    if 'checkout' in request.POST:
        form = CheckoutForm(request.POST)

        #data would need to be verified and used here once changes to models are implemented
        #print(form)

        cart = Cart.objects.filter(userID=request.user.username).values('listingID')
        cartlistings = Listing.objects.filter(id__in=cart).delete()
        Cart.objects.filter(userID=request.user.username).delete()

        return redirect('cart')
    else:
        form = CheckoutForm()
        return render(request, 'checkout.html', {'form': form})

@login_required
def pull_cart(request):
        cart = Cart.objects.filter(userID=request.user.username).values_list('listingID');
        listings = Listing.objects.filter(id__in=cart).values('isbn');
        books = Book.objects.filter(isbn__in=listings);
    
        return render(request, "cart_display.html",
                      {'books': books,'listings': listings ,'username': request.user.username})

    
@login_required
def author(request, author):
    books = Book.objects.filter(author = author)
    if(len(books) == 0):
        return render(request, "null_author.html")

    context = {
        'book_list' : books,
    }

    return render(request, 'browse_books.html', context = context)

@login_required
def search(request):
    if request.method=="POST":
        search = request.POST["search"]

        if len(search) == 0:
            return render(request, "null_search.html", {"search": search})

        results = Book.objects.filter(title__contains=search)
        results = results | Book.objects.filter(author__contains=search)
        results = results | Book.objects.filter(isbn=search)
        results.order_by("title", "author", "rating")

        if len(results) == 0:
            return render(request, "null_search.html", {"search": search})

        context = {
                "book_list": results,
                }
        return render(request, "browse_books.html", context = context)

    else:
        return render(request, "null_search.html")

   
