from django.test import TestCase
from store.models import CustomUser, Book, Image, Listing, Cart

class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(
            title="The Hunger Games", 
            author = "Coleen Hoover",
            isbn = 439023483,
            pages = 384,
            rating = 4.3,
            description = "Dystopian novel where kids kill each other"
        )
        Book.objects.create(
            title="Tress of the Emerald Sea (paperback)", 
            author = "Brandon Sanderson",
            isbn = 9781399613385,
            pages = 384,
            rating = .2,
            description = "A girl lives on an ocean world"
        )
        Book.objects.create(
            title="Tress of the Emerald Sea (hardcover)", 
            author = "Brandon Sanderson",
            isbn = 9781250899651,
            pages = 302,
            rating = 4.0,
            description = "A girl lives on an ocean world"
        )

    def test_books_created(self):
        """Tests if books are created correctly"""

        # get the books
        hunger_games = Book.objects.get(isbn = 439023483)
        tress_paperback = Book.objects.get(isbn = 9781399613385)
        tress_hardcover = Book.objects.get(isbn = 9781250899651)


        self.assertEqual(str(hunger_games), 'The Hunger Games by Coleen Hoover')
        self.assertEqual(str(tress_paperback), 'Tress of the Emerald Sea (paperback) by Brandon Sanderson')
        self.assertEqual(str(tress_hardcover), 'Tress of the Emerald Sea (hardcover) by Brandon Sanderson')
    
    def test_books_uniqueness(self):
        """Tests if there are the right number of books"""

        # get the books
        books_count = Book.objects.all().count()

        self.assertEqual(books_count, 3)

    def test_book_title_max_length(self):
        """Tests if there are the book title length is correct"""

        book = Book.objects.get(isbn=439023483)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)