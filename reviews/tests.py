
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Contributor, Review
from accounts.forms import SearchForm


class BookViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(title='Test Book', publication_date='2022-01-01')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
#
#     def test_book_search_view(self):
#         response = self.client.get(reverse('book_search'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'search-results.html')
#
#         # Test with search query
#         response = self.client.get(reverse('book_search'), {'search': 'Test'})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'search-results.html')
#         self.assertIn('books', response.context)
#         self.assertIsInstance(response.context['form'], SearchForm)
#
#     def test_book_list_view(self):
#         response = self.client.get(reverse('book_list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'book_list.html')
#         self.assertIn('book_list', response.context)
#
    # def test_book_detail_view(self):
    #     response = self.client.get(reverse('book_detail', args=[str(self.book.id)]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'book_detail.html')
    #     self.assertIn('book', response.context)
    #     self.assertIn('book_rating', response.context)
    #     self.assertIn('reviews', response.context)
#
#     def test_book_detail_view_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.get(reverse('book_detail', args=[str(self.book.id)]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'book_detail.html')
#         self.assertIn('book', response.context)
#         self.assertIn('book_rating', response.context)
#         self.assertIn('reviews', response.context)
#         self.assertIn('viewed_books', self.client.session)