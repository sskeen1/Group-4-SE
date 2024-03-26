from django.test import TestCase
from django.urls import reverse

from store.models import Book

class BrowseBookViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/store/books/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)
