from typing import Any
from django.test import TestCase
from django.urls import reverse

from store.models import Book, Listing, Cart, CustomUser
from store.forms import SignupForm


'''
List of all views/features:

@login_required
def book(request, isbn):

@login_required
def add_cart(request,id):

@login_required
def remove_cart(request,id):

@login_required
def pull_cart(request):

@login_required
def checkout(request):

@login_required
def search(request)

@login_required
def decrease_cart_quantity(request, id):

@login_required
def increase_cart_quantity(request, id):
'''

class SignupViewTest(TestCase):
    ''' Further testing of this feature can be found in the form testing file'''
    def setUp(self):
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_form_type(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SignupForm)


class RouterViewTest(TestCase):
    def setUp(self):
        test_buyer = CustomUser.objects.create_user(username='testbuyer1', password='group4se', type="Buyer")
        test_seller = CustomUser.objects.create_user(username='testseller1', password='group4se', type="Seller")
        test_badUser = CustomUser.objects.create_user(username='testbaduser1', password='group4se', type="Weird")
        test_buyer.save()
        test_seller.save()
        test_badUser.save()

    def test_view_url_redirects_for_buyer(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)

    def test_view_url_redirects_for_seller(self):
        login = self.client.login(username='testseller1', password='group4se')
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)

    def test_routing_to_buyer_dashboard(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('')
        self.assertEqual(response.url, '/buyer/')
    
    def test_routing_to_seller_dashboard(self):
        login = self.client.login(username='testseller1', password='group4se')
        response = self.client.get('')
        self.assertEqual(response.url, '/seller/')

    def test_routing_to_no_dashboard(self):
        login = self.client.login(username='testbaduser1', password='group4se')
        response = self.client.get('')
        self.assertEqual(response.url, '/accounts/signup/')


class BrowseBookViewTest(TestCase):

    def setUp(self):
        # Create 5 books for tests
        number_of_books = 5

        for book_id in range(number_of_books):
            Book.objects.create(
                title=f'Book {book_id}',
                author=f'Author {book_id}',
                isbn= book_id + 1,
                pages=200,
                rating=4,
                description=f'Here is example book {book_id}'
            )

        test_user1 = CustomUser.objects.create_user(username='testbuyer1', password='group4se', type="Buyer")
        test_user1.save()

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-books/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse_books.html')

    def test_book_display_is_correct_length(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['book_list']), 5)
    
    def test_book_one_is_correct(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['book_list'][0]['title'], "Book 0")

    def test_book_five_is_correct(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['book_list'][4]['author'], "Author 4")


class BuyerDashboardViewTest(TestCase):
    def setUp(self):
        self.test_user = CustomUser.objects.create_user(username='testbuyer1', password='group4se', type="Buyer")
        # Creating some example books for testing
        self.book1 = Book.objects.create(title='Book 1', author='Author 1', isbn=1234567890123, pages=200, rating=4)
        self.book2 = Book.objects.create(title='Book 2', author='Author 2', isbn=1234567890124, pages=250, rating=5)
        self.book3 = Book.objects.create(title='Book 3', author='Author 1', isbn=1234567890125, pages=180, rating=3)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/buyer/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/buyer/')
        self.assertTemplateUsed(response, 'buyer_dashboard.html')

    def test_correct_book_nums_displayed(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/buyer/')
        self.assertEqual(response.context['num_books'], 3)

    def test_correct_user_type_displayed(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/buyer/')
        self.assertEqual(response.context['user_type'], 'Buyer')


class BrowseAuthorViewTest(TestCase):

    def setUp(self):
        # Create 5 books for tests
        number_of_books = 5

        for book_id in range(number_of_books):
            Book.objects.create(
                title=f'Book {book_id}',
                author=f'Author {book_id}',
                isbn= book_id + 1,
                pages=200,
                rating=4,
                description=f'Here is example book {book_id}'
            )

        test_user1 = CustomUser.objects.create_user(username='testbuyer1', password='group4se', type="Buyer")
        test_user1.save()

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-authors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse_authors.html')

    def test_author_display_is_correct_length(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-authors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['authors']), 5)
    
    def test_author_one_is_correct(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-authors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['authors'][0]['author'], "Author 0")

    def test_author_five_is_correct(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/browse-authors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['authors'][4]['author'], "Author 4")


class AuthorViewTest(TestCase):
    def setUp(self):
        # Create 5 books for tests
        number_of_books = 5

        for book_id in range(number_of_books):
            Book.objects.create(
                title=f'Book {book_id}',
                author=f'Author {book_id}',
                isbn= book_id + 1,
                pages=200,
                rating=4,
                description=f'Here is example book {book_id}'
            )

        Book.objects.create(
            title=f'Book 200',
            author=f'Author 4',
            isbn= 200,
            pages=200,
            rating=4,
            description=f'Here is example book {number_of_books}'
        )

        test_user1 = CustomUser.objects.create_user(username='testbuyer1', password='group4se', type="Buyer")
        test_user1.save()
    
    def test_view_url_redirects(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/author/Author 0/')
        self.assertEqual(response.status_code, 200)

    def test_view_directs_to_correct_template(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/author/Author 0/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse_books.html')

    def test_view_contains_correct_book(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/author/Author 0/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['book_list'][0].title, 'Book 0')
    
    def test_view_contains_multiple_books_for_same_author(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/author/Author 4/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['book_list']), 2)

    def test_view_directs_to_null_template_for_wrong_url(self):
        login = self.client.login(username='testbuyer1', password='group4se')
        response = self.client.get('/author/bad author/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'null_author.html')


'''
Features for next sprint so don't need to be tested now:


@login_required
def seller_dashboard(request):

@login_required
def seller_listing(request, id):

@login_required
def add_listing(request, isbn=''):

@login_required
def add_book(request):

@login_required
def remove_listing(request,id):
'''