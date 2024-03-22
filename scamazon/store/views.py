from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Listing, Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm, ListingForm, BookForm
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
    listings_list = Listing.objects.filter(userID=request.user.id)

    context = {
        'num_books': num_books,
        'user_type': request.user.type,
        'listing_list': listings_list
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
    cart = Cart.objects.filter(userID=request.user.username);
    if listing in cart:
        p = Cart.objects.filter(listingID=listing, quantity=1, userID=request.user.username).delete()
        return redirect('cart')
    else:
        return redirect('cart')

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

@login_required
def seller_listing(request, id):
    try: 
        listing = Listing.objects.get(id = id)
    except(ObjectDoesNotExist):
        return render(request, "null_book.html")
    
    context = {
        "listing": listing,
            }

    return render(request, 'seller_listing.html', context = context)

@login_required
def add_listing(request, isbn=''):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ListingForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            
            #book already exists
            if (Book.objects.filter(isbn=form.cleaned_data['isbn'])):
                book = Book.objects.filter(isbn=form.cleaned_data['isbn'])[0]
                new_listing = Listing(
                    listingID = 0,
                    isbn = book,
                    quantity=form.cleaned_data['quantity'],
                    price=form.cleaned_data['price'],
                    userID=request.user,
                    image=form.cleaned_data['image']
                )
                new_listing.save()
            else:
                return redirect('/seller/add_book')

            # redirect to a new URL:
            return redirect('/seller')

    # If this is a GET (or any other method) create the default form.
    else:
        form = ListingForm(initial={'isbn': isbn})

    context = {
        'form': form,
    }

    return render(request, 'add_listing.html', context)

@login_required
def add_book(request):
     # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = BookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            newBook = Book(
                isbn = form.cleaned_data['isbn'],
                title = form.cleaned_data['title'],
                author = form.cleaned_data['author'],
                pages = form.cleaned_data['pages'],
                rating = form.cleaned_data['rating'],
                description = form.cleaned_data['description'],
            )
            newBook.save()

            # redirect to a new URL:
            return redirect('/seller/add_listing/' + form.cleaned_data['isbn'])

    # If this is a GET (or any other method) create the default form.
    else:
        form = ListingForm()

    context = {
        'form': form,
    }

    return render(request, 'add_listing.html', context)