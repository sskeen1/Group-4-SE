from django.test import TestCase
from store.models import CustomUser, Book, Image, Listing, Cart
from django.db import IntegrityError, DataError
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
        with self.assertRaises(ValueError):
            Book.objects.create() #all fields are empty
            
    def test_fields_invalid_values(self):
        #Test if input validation is properly handled
        with self.assertRaises(ValueError):
            Book.objects.create(
                title = "What If?: Serious Scientific Answers to Absurd Hypothetical Questions",
                author = "Randall Monroe",
                isbn = 9780544272996,
                pages = 320,
                rating = -8, #negative rating isn't possible
                description = "HIDDEN FEATURE: The inside of this book has words and pictures.")
            
        with self.assertRaises(ValueError):
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
        image_file_path = 'store/tests/test_image.jpg'
        
        # Open and read the image file
        with open(image_file_path, 'rb') as f:
            image_data = f.read()
        
        #Create SimpleUploadedFile from the image data
        image_file = SimpleUploadedFile("test_image.jpg", image_data, content_type = "image/jpeg")

        #Create image object
        image_object = Image.objects.create(image = image_file)

        #Test if image is stored properly
        self.assertTrue(image_object.image.name.startswith("uploads/test_image"))
        
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
        
        image_file_path = 'store/tests/test_image.jpg'
        
        with open(image_file_path, 'rb') as f:
            image_data = f.read()
        
        image_file = SimpleUploadedFile("test_image.jpg", image_data, content_type = "image/jpeg")

        self.image_object = Image.objects.create(image = image_file)
        
        Listing.objects.create(
            isbn = self.book.isbn,
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
        with self.assertRaises(ValueError):
            Listing.objects.create() #all fields are empty
            
    def test_listing_fields_invalid_values(self):
        #Test if input validation is properly handled
        with self.assertRaises(ValueError):
            Listing.objects.create(
                isbn = self.book.isbn,
                quantity = 6,
                userID = self.user,
                price = -723.99, #invalid price
                image = self.image_object)
    
        with self.assertRaises(ValueError):
            Listing.objects.create(
                isbn = self.book.isbn,
                quantity = -1, #invalid quantity
                userID = self.user,
                price = 54.32,
                image = self.image_object)
            
            
    
        
