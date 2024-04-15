from django.test import TestCase
from store.models import CustomUser, Book, Image, Listing, Cart, Order
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(
            title = "The Hunger Games", 
            author = "Coleen Hoover",
            isbn = 439023483,
            pages = 384,
            rating = 4.3,
            description = "Dystopian novel where kids kill each other")
        
        Book.objects.create(
            title = "Tress of the Emerald Sea (paperback)", 
            author = "Brandon Sanderson",
            isbn = 9781399613385,
            pages = 384,
            rating = .2,
            description = "A girl lives on an ocean world")
        
        Book.objects.create(
            title = "Tress of the Emerald Sea (hardcover)", 
            author = "Brandon Sanderson",
            isbn = 9781250899651,
            pages = 302,
            rating = 4.0,
            description = "A girl lives on an ocean world")
        
        Book.objects.create(
            title = "Gadsby",
            author = "Ernest Wright",
            isbn = 9781466216730,
            pages = 260,
            rating = 4.2,
            description = "A story of over 50,000 words without using the letter 'E'")
        
    def test_books_created(self):
        #Tests if the books are created correctly
        hunger_games = Book.objects.get(isbn = 439023483)
        tress_paperback = Book.objects.get(isbn = 9781399613385)
        tress_hardcover = Book.objects.get(isbn = 9781250899651)
        gadsby = Book.objects.get(isbn = 9781466216730)

        self.assertEqual(str(hunger_games), 'The Hunger Games by Coleen Hoover')
        self.assertEqual(str(tress_paperback), 'Tress of the Emerald Sea (paperback) by Brandon Sanderson')
        self.assertEqual(str(tress_hardcover), 'Tress of the Emerald Sea (hardcover) by Brandon Sanderson')
        self.assertEqual(str(gadsby), 'Gadsby by Ernest Wright')
    
    def test_books_uniqueness(self):
        books_count = Book.objects.all().count() #gets the books
        #Tests if there are the right number of books
        self.assertEqual(books_count, 4)

    def test_book_title_max_length(self):
        #Tests if there are the book title length is correct
        book = Book.objects.get(isbn = 439023483)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)
        
    def test_books_rating(self):
        book1 = Book.objects.get(isbn = 9781466216730) # >4
        book2 = Book.objects.get(isbn = 9781250899651) # =4
        book3 = Book.objects.get(isbn = 9781399613385) # <4
        
        #Test if is_highly_rated() functions properly
        self.assertTrue(book1.is_highly_rated())
        self.assertTrue(book2.is_highly_rated())
        self.assertFalse(book3.is_highly_rated())
        
class BookValidationTestCase(TestCase):
    def setUp(self):
        Book.objects.create(
            title = "The Hunger Games", 
            author = "Coleen Hoover",
            isbn = 439023483,
            pages = 384,
            rating = 4.3,
            description = "Dystopian novel where kids kill each other")
        
    def test_repeat_primary_key(self):
        #Tests if unique primary keys are enforced 
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title = "Clifford, the Big Red Dog",
                author = "Norman Bridwell",
                isbn = 439023483, #primary key already in db
                pages = 32,
                rating = 3.9,
                description = "I don't know, look it up")
    
    def test_required_fields_populated(self):
        #Test if required fields must be populated    
        with self.assertRaises(IntegrityError):
            Book.objects.create() #all fields are empty
            
    def test_fields_invalid_values(self):
        #Test if input validation is properly handled
        with self.assertRaises(ValidationError):
            Book.objects.create(
                title = "What If?: Serious Scientific Answers to Absurd Hypothetical Questions",
                author = "Randall Monroe",
                isbn = 9780544272996,
                pages = 320,
                rating = -8, #negative rating isn't possible
                description = "HIDDEN FEATURE: The inside of this book has words and pictures.")
            
        with self.assertRaises(ValidationError):
            Book.objects.create(
                title = "The Hunger Games", 
                author = "Coleen Hoover",
                isbn = "Hello >:D", #invalid primary key
                pages = 384,
                rating = 4.3,
                description = "Dystopian novel where kids kill each other")

class CustomUserTestCase(TestCase):
    def test_custom_field_validation(self):
        #Test if type field is set correctly
        user = CustomUser.objects.create_user(
            username = 'testuser',
            email = 'test@example.com',
            password = 'password',
            type = 'Buyer')
        self.assertEqual(user.type, 'Buyer')

    def test_default_type_value(self):
        #Test default value of the 'type' field
        user = CustomUser.objects.create_user(
            username = 'testuser',
            email = 'test@example.com',
            password = 'password')
        self.assertEqual(user.type, '')
        
    def test_type_invalid_range(self):
        #Test validation of max field length for type
        with self.assertRaises(DataError):
            user = CustomUser.objects.create_user(
                username = 'testuser',
                email = 'test@example.com',
                password = 'password',
                type = 'BuyerButLikeWayTooLong' #invalid type name
                )
            
class ImageTestCase(TestCase):
    def test_image_upload(self):
        #Provide the path test image file
        image_file_path = 'scamazon/store/tests/test_image.jpg'
        
        # Open and read the image file
        with open(image_file_path, 'rb') as f:
            image_data = f.read()
        
        #Create SimpleUploadedFile from the image data
        image_file = SimpleUploadedFile("test_image.jpg", image_data, content_type = "image/jpeg")

        #Create image object
        image_object = Image.objects.create(image = image_file)

        #Test if image is stored properly
        self.assertTrue(image_object.image.name.startswith("test_image"))
        
class ListingTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title = "Gadsby",
            author = "Ernest Wright",
            isbn = 9781466216730,
            pages = 260,
            rating = 4.2,
            description = "A story of over 50,000 words without using the letter 'E'")
        
        self.user = CustomUser.objects.create_user(
            username = 'testuser',
            email = 'test@example.com',
            password = 'password',
            type = 'Buyer')
        
        image_file_path = 'scamazon/store/tests/test_image.jpg'
        
        with open(image_file_path, 'rb') as f:
            image_data = f.read()
        
        image_file = SimpleUploadedFile("test_image.jpg", image_data, content_type = "image/jpeg")

        self.image_object = Image.objects.create(image = image_file)
        
        Listing.objects.create(
            isbn = self.book,
            quantity = 2,
            userID = self.user,
            price = 13.67,
            image = self.image_object)
        
    def test_listing_created(self):
        listing_count = Listing.objects.all().count() #gets all listings
        
        #Tests that the listing was made
        self.assertEqual(listing_count, 1)
        
    def test_listing_fields_filled(self):
        listing = Listing.objects.get(isbn = self.book.isbn)
        
        #Tests if data in fields is correct
        self.assertEqual(listing.quantity, 2)
        self.assertEqual(listing.price, 13.67)
        
    def test_listing_required_fields_populated(self):
        #Test default behavior of model    
        with self.assertRaises(IntegrityError):
            Listing.objects.create() #all fields are empty
            
    def test_listing_fields_invalid_values(self):
        #Test if input validation is properly handled
        with self.assertRaises(ValidationError):
            Listing.objects.create(
                isbn = self.book,
                quantity = 6,
                userID = self.user,
                price = -723.99, #invalid price
                image = self.image_object)
    
        with self.assertRaises(ValidationError):
            Listing.objects.create(
                isbn = self.book,
                quantity = -1, #invalid quantity
                userID = self.user,
                price = 54.32,
                image = self.image_object)
            
class CartTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title = "Gadsby",
            author = "Ernest Wright",
            isbn = 9781466216730,
            pages = 260,
            rating = 4.2,
            description = "A story of over 50,000 words without using the letter 'E'")
        
        self.buyer = CustomUser.objects.create_user(
            username = 'testbuy',
            email = 'test@example.com',
            password = 'password',
            type = 'Buyer')
        
        self.seller = CustomUser.objects.create_user(
            username = 'testsell',
            email = 'test@example.com',
            password = 'password',
            type = 'Seller')
        
        image_file_path = 'scamazon/store/tests/test_image.jpg'
        
        with open(image_file_path, 'rb') as f:
            image_data = f.read()
        
        image_file = SimpleUploadedFile("test_image.jpg", image_data, content_type = "image/jpeg")

        self.image_object = Image.objects.create(image = image_file)
        
        self.listing1 = Listing.objects.create(
            isbn = self.book,
            quantity = 30,
            userID = self.seller,
            price = 13.67,
            image = self.image_object)
        
        self.listing2 = Listing.objects.create(
            isbn = self.book,
            quantity = 3,
            userID = self.seller,
            price = 4.24,
            image = self.image_object)
        
        Cart.objects.create(
            listingID = self.listing1,
            quantity = 3,
            userID = self.buyer)
    
    def test_cart_created(self):
        cart_count = Cart.objects.all().count() #gets all cart objects
        
        #Tests that the object was made
        self.assertEqual(cart_count, 1)
        
    def test_cart_fields_filled(self):
        cart = Cart.objects.get(listingID = self.listing1)
        
        #Tests if data in fields is correct
        self.assertEqual(cart.quantity, 3)
        
    def test_cart_default_case(self):
        Cart.objects.create(
            listingID = self.listing2,
            userID = self.buyer)
        
        #Tests default case of quantity field
        cart = Cart.objects.get(listingID = self.listing2)
        self.assertEqual(cart.quantity, 1)
        
    def test_cart_required_fields_populated(self):
        #Test default behavior of model    
        with self.assertRaises(IntegrityError):
            Cart.objects.create() #all fields are empty
        
    def test_cart_invalid_field(self):
        #Tests if input validation is handled properly
        with self.assertRaises(ValidationError):
            Cart.objects.create(
                listingID = self.listing1,
                quantity = -6, #invalid quantity
                userID = self.buyer)

class OrderTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title = "Gadsby",
            author = "Ernest Wright",
            isbn = 9781466216730,
            pages = 260,
            rating = 4.2,
            description = "A story of over 50,000 words without using the letter 'E'")
        
        self.buyer = CustomUser.objects.create_user(
            username = 'testbuy',
            email = 'test@example.com',
            password = 'password',
            type = 'Buyer')
        
        self.seller = CustomUser.objects.create_user(
            username = 'testsell',
            email = 'test@example.com',
            password = 'password',
            type = 'Seller')
        
        image_file_path = 'scamazon/store/tests/test_image.jpg'
        
        with open(image_file_path, 'rb') as f:
            image_data = f.read()
        
        image_file = SimpleUploadedFile("test_image.jpg", image_data, content_type = "image/jpeg")

        self.image_object = Image.objects.create(image = image_file)
        
        self.listing = Listing.objects.create(
            isbn = self.book,
            quantity = 54,
            userID = self.seller,
            price = 2.34,
            image = self.image_object)
        
        self.order = Order.objects.create(
            date = '2024-4-16',
            oldListingId = 8927091,
            oldListingImage = self.image_object,
            quantity = 2,
            book = self.book,
            price = self.listing.price,
            buyer = self.buyer,
            seller = self.seller,
            delivered = False,
            address = '123 Totally Real St',
            payment = '8291473089473064')
        
    def test_order_created(self):
        order_count = Order.objects.all().count() #gets all order objects
        
        #Tests if the order was made
        self.assertEqual(order_count, 1)
    
    def test_order_values(self):
        #Tests if field data is correct
        self.assertEqual(self.order.date, '2024-4-16')
        self.assertEqual(self.order.quantity, 2)
        self.assertEqual(self.order.price, self.listing.price)
        self.assertEqual(self.order.address, '123 Totally Real St')
        
    def test_order_get_payment_digits(self):
        #Tests if get_payment_last_4_digits() functions properly
        self.assertEqual(self.order.get_payment_last_4_digits(), '3064')
    
    def test_order_get_total_payment(self):
        #Tests if get_total_payment() functions properly
        self.assertEqual(self.order.get_total_payment(), 4.68)
        
    def test_order_required_fields_populated(self):
        #Test default behavior of model    
        with self.assertRaises(IntegrityError):
            Order.objects.create() #all fields are empty
            
    def test_order_fields_invalid(self):
        #Tests if input validation is handled properly
        with self.assertRaises(ValidationError):
            Order.objects.create(
            date = '2024-4-16',
            oldListingId = 8927091,
            oldListingImage = self.image_object,
            quantity = 2,
            book = self.book,
            price = 14.99,
            buyer = self.buyer,
            seller = self.seller,
            delivered = False,
            address = '123 Totally Real St',
            payment = '3' #invalid payment credentials
            )
            
        with self.assertRaises(ValidationError):
            Order.objects.create(
            date = '2024-4-16',
            oldListingId = 8927091,
            oldListingImage = self.image_object,
            quantity = -97, #invalid quantity
            book = self.book,
            price = 14.99,
            buyer = self.buyer,
            seller = self.seller,
            delivered = False,
            address = '123 Totally Real St',
            payment = '8291473089473064')
            
        with self.assertRaises(ValidationError):
            Order.objects.create(
            date = '2024-4-16',
            oldListingId = 8927091,
            oldListingImage = self.image_object,
            quantity = 1,
            book = self.book,
            price = -3, #invalid price
            buyer = self.buyer,
            seller = self.seller,
            delivered = False,
            address = '123 Totally Real St',
            payment = '8291473089473064')