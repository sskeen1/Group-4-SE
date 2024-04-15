from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Listing, Cart, Order, Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm, ListingForm, BookForm, CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
import datetime


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

    #notify if a new listing has sold
    orders_list = Order.objects.filter(seller=request.user)
    undelivered_count = 0
    for order in orders_list:
        if not order.delivered:
            undelivered_count += 1

    context = {
        'num_books': num_books,
        'user_type': request.user.type,
        'listing_list': listings_list,
        'undelivered_count': undelivered_count
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
    except(ObjectDoesNotExist):
        return render(request, "null_book.html")
    
    context = {
        "book": book,
        "listing_list": listings_list,
            }

    return render(request, 'book.html', context = context)


@login_required
def add_cart(request, id):
    listing = get_object_or_404(Listing, id=request.POST.get('id'))
    cart = Cart.objects.filter(userID=request.user.username).values('listingID')
    cartlistings = Listing.objects.filter(id__in=cart)

    if listing in cartlistings:
        return redirect('cart')
    else:
        p = Cart.objects.create(listingID=listing, quantity=1, userID=request.user.username)
        return redirect('cart')

@login_required
def remove_cart(request, id):
    listing = get_object_or_404(Listing, id=request.POST.get('id'))
    cart = Cart.objects.filter(userID=request.user.username).values('listingID')
    cartlisting = Listing.objects.filter(id__in=cart)

    if listing in cartlisting:
        p = Cart.objects.filter(listingID=listing, userID=request.user.username).delete()
        return redirect('cart')
    else:
        return redirect('cart')

@login_required
def pull_cart(request):
        cart = Cart.objects.filter(userID=request.user.username)
        listings = Listing.objects.filter(id__in=cart).values('isbn')
        books = Book.objects.filter(isbn__in=listings)
    
        return render(request, "cart_display.html",
                      {'books': books,'listings': listings ,'username': request.user.username, 'cart': cart})


@login_required
def checkout(request):
    if 'checkout' in request.POST:
        form = CheckoutForm(request.POST)

        #data would need to be verified and used here once changes to models are implemented

        if form.is_valid():
            cart = Cart.objects.filter(userID=request.user.username)

            for item in cart:
                listing = item.listingID

                #create an order
                new_order = Order(
                    date = datetime.date.today(),
                    quantity = item.quantity,
                    book = listing.isbn,
                    price = listing.price,
                    buyer = request.user,
                    seller = listing.userID,
                    delivered = False,
                    address = form.cleaned_data['address'],
                    payment = form.cleaned_data['cardNum'],
                    oldListingId = listing.id,
                    oldListingImage = listing.image
                )
                new_order.save()

                #decrease listing amount by the cart items amount
                if item.quantity < listing.quantity:
                    listing.quantity -= item.quantity
                    listing.save()
                else:
                    listing.delete()

            Cart.objects.filter(userID=request.user.username).delete()

            return redirect('cart')
        else:
            return redirect('cart')
    else:
        form = CheckoutForm()
        return render(request, 'checkout.html', {'form': form})

    
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
        form = ListingForm(request.POST, request.FILES)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            
            #book already exists
            if (Book.objects.filter(isbn=form.cleaned_data['isbn'])):
                book = Book.objects.filter(isbn=form.cleaned_data['isbn'])[0]
                print(form.cleaned_data.get('image'))
                new_image = Image(
                    image=form.cleaned_data.get('image')
                )
                new_image.save()
                new_listing = Listing(
                    listingID = 0,
                    isbn = book,
                    quantity=form.cleaned_data['quantity'],
                    price=form.cleaned_data['price'],
                    userID=request.user,
                    image=new_image
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
        form = BookForm()

    context = {
        'form': form,
    }

    return render(request, 'add_listing.html', context)

@login_required
def remove_listing(request,id):
    listing = get_object_or_404(Listing, id=request.POST.get('listing_id'))
    if listing:
        listing.delete()
        return redirect('/seller/')
    else:
        return redirect('/seller/')
    
@login_required
def decrease_cart_quantity(request, id):
    listing = get_object_or_404(Listing, id=request.POST.get('id'))
    cart = Cart.objects.filter(userID=request.user.username).values('listingID')
    cartlisting = Listing.objects.filter(id__in=cart)

    if listing in cartlisting:
        p = Cart.objects.filter(listingID=listing, userID=request.user.username)
        for cartObject in p:
            if cartObject.quantity > 1:
                cartObject.quantity -= 1
                cartObject.save()
            else:
                cartObject.delete()
        return redirect('cart')
    else:
        return redirect('cart')
    
@login_required
def increase_cart_quantity(request, id):
    listing = get_object_or_404(Listing, id=request.POST.get('id'))
    cart = Cart.objects.filter(userID=request.user.username).values('listingID')
    cartlisting = Listing.objects.filter(id__in=cart)

    if listing in cartlisting:
        p = Cart.objects.filter(listingID=listing, userID=request.user.username)
        for cartObject in p:
            if listing.quantity >= cartObject.quantity + 1:
                cartObject.quantity += 1
                cartObject.save()
            else:
                pass
        return redirect('cart')
    else:
        return redirect('cart')
    
@login_required
def edit_listing(request, id):
    
    listing = get_object_or_404(Listing, id=id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ListingForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            listing.quantity=form.cleaned_data['quantity']
            listing.price=form.cleaned_data['price']
            listing.image=form.cleaned_data['image']
            listing.save()

            # redirect to a new URL:
            return redirect('/seller')

    # If this is a GET (or any other method) create the default form.
    else:
        form = ListingForm(initial={'isbn': listing.isbn.isbn, 'quantity': listing.quantity, 'price': listing.price, 'image': listing.image})

    context = {
        'form': form,
    }

    return render(request, 'add_listing.html', context)

@login_required
def buyer_orders(request):
    orders_list = Order.objects.filter(buyer=request.user).order_by('delivered')

    context = {
        'orders_list': orders_list
    }

    return render(request, 'buyer_orders.html', context=context)

@login_required
def return_order(request, id):
    order = get_object_or_404(Order, id=id)

    #check if the order is already delivered and if it don't let them return it
    if order.delivered:
        return redirect('buyer_orders')
    else:
        # if the listing still exits
        try:
            oldListing = Listing.objects.get(id=order.oldListingId)
            oldListing.quantity += order.quantity
            oldListing.save()
            order.delete()
        
        #if the listing doesn't still exist make a new one
        except Listing.DoesNotExist:
            returned_listing = Listing(
                id = order.oldListingId,
                listingID = 0,
                isbn = order.book,
                quantity = order.quantity,
                userID = order.seller,
                price = order.price,
                image = order.oldListingImage
            )
            returned_listing.save()
            order.delete()

        return redirect('buyer_orders')
    
@login_required
def seller_orders(request):
    orders_list = Order.objects.filter(seller=request.user).order_by('delivered')

    total_made = 0
    for order in orders_list:
        total_made += order.quantity * order.price

    context = {
        'orders_list': orders_list,
        'total_made': round(total_made, 2)
    }

    return render(request, 'seller_orders.html', context=context)

@login_required
def deliver_order(request, id):
    order = get_object_or_404(Order, id=id)

    #check if the order is already delivered and if it don't let them return it
    if order.delivered:
        return redirect('seller_orders')
    else:
        
        order.delivered = True
        order.save()

        return redirect('seller_orders')