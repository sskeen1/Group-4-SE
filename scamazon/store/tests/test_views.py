from django.test import TestCase
from django.urls import reverse

from store.models import Book, CustomUser


class BrowseBookViewTest(TestCase):

    def setUp(self):
        # Create 5 books for tests
        number_of_books = 5

        for book_id in range(number_of_books):
            Book.objects.create(
                title=f'Book {book_id}',
                author=f'Author {book_id}',
                isbn={book_id},
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
