from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import ReviewForm
from .models import Book, Contributor, Review, Publisher
from accounts.forms import SearchForm
from .views import review_edit


class BookViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.publisher_data = {'name': 'publisher', 'email': 'test@o2.pl', 'website': 'www.website.com'}
        self.publisher = Publisher.objects.create(**self.publisher_data)

        self.book = Book.objects.create(title='Test Book', publication_date=datetime.now(), isbn='1234567890',
                                        publisher=self.publisher)

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    #
    def test_book_search_view(self):
        response = self.client.get(reverse('book_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search-results.html')

        # Test with search query
        response = self.client.get(reverse('book_search'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search-results.html')
        self.assertIn('books', response.context)
        self.assertIsInstance(response.context['form'], SearchForm)

    #
    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertIn('book_list', response.context)

    #
    def test_book_detail_view(self):
        response = self.client.get(reverse('book_detail', args=[str(self.book.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')
        self.assertIn('book', response.context)
        self.assertIn('book_rating', response.context)
        self.assertIn('reviews', response.context)

    #
    def test_book_detail_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('book_detail', args=[str(self.book.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')
        self.assertIn('book', response.context)
        self.assertIn('book_rating', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('viewed_books', self.client.session)


class AddBookViewTest(TestCase):
    # def setUp(self):
    #     # Tworzymy użytkownika (możesz dostosować to do swoich potrzeb)
    #     self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_add_book_view(self):
        # Logujemy się przed przystąpieniem do testu
        self.client.login(username='testuser', password='testpassword')

        # Dane testowe dla nowej książki
        new_book_data = {
            'title': 'Test Book',
            'contributors': 'Test Author',
            'publication_date': '2022-01-01',
            'isbn': '1234567890',
            'publisher': 'Test Publisher'


        }

        # Wysyłamy żądanie POST do widoku AddBookView z danymi nowej książki
        response = self.client.post(reverse('add_book'), data=new_book_data)
        self.assertTemplateUsed(response, 'add_book.html')

        # Sprawdzamy, czy odpowiedź przekierowuje nas na stronę z listą książek
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('book_list'))

        # Sprawdzamy, czy książka została dodana poprawnie do bazy danych
        self.assertTrue(Book.objects.filter(title='Test Book').exists())

        # Sprawdzamy, czy wiadomość sukcesu została dodana do kontekstu
        messages = [msg.message for msg in response.context['messages']]
        self.assertIn(f"Dodano książkę {new_book_data['title']}", messages)


class ReviewDeleteViewTest(TestCase):

    def setUp(self):
        # Tworzymy użytkownika
        self.user = User.objects.create_user(username='testuser', email='uzytkownik@o2.pl', password='testpassword')

        # Tworzymy książkę
        self.publisher_data = {'name': 'publisherTest', 'email': 'Publoisher@o2.pl', 'website': 'www.testwebsite.com'}
        self.publisher = Publisher.objects.create(**self.publisher_data)
        self.book = Book.objects.create(title='Test Book', publication_date=datetime.now(), isbn='1234567890',
                                        publisher=self.publisher)

        # Logujemy użytkownika
        self.client.login(username='testuser', password='testpassword')

        # Tworzymy recenzję przypisaną do użytkownika i książki
        self.review = Review.objects.create(
            creator=self.user,
            book=self.book,
            content='Test review content',
            rating=5
        )

    def test_review_delete_view_get(self):
        # Testujemy GET request do widoku usuwania recenzji
        response = self.client.get(reverse('review_delete', args=[self.book.id, self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_list.html')

    def test_review_delete_view_post(self):
        # Testujemy POST request do widoku usuwania recenzji
        response = self.client.post(reverse('review_delete', args=[self.book.id, self.review.id]))
        self.assertEqual(response.status_code, 302)  # Oczekujemy przekierowania po usunięciu recenzji
        self.assertEqual(Review.objects.count(), 0)  # Oczekujemy, że recenzja została usunięta

    def test_review_delete_view_post_wrong_user(self):
        # Testujemy POST request do widoku usuwania recenzji przez użytkownika, który nie jest autorem recenzji
        # Powinien otrzymać komunikat o błędzie
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.login(username='anotheruser', password='anotherpassword')

        response = self.client.post(reverse('review_delete', args=[self.book.id, self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'komunikat.html')
        self.assertEqual(Review.objects.count(), 1)  # Recenzja nie powinna zostać usunięta

    def test_review_delete_view_get_wrong_user(self):
        # Testujemy GET request do widoku usuwania recenzji przez użytkownika, który nie jest autorem recenzji
        # Powinien otrzymać komunikat o błędzie
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.login(username='anotheruser', password='anotherpassword')

        response = self.client.get(reverse('review_delete', args=[self.book.id, self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'komunikat.html')
        self.assertEqual(Review.objects.count(), 1)  # Recenzja nie powinna zostać usunięta


class ReviewEditViewTest(TestCase):

    def setUp(self):
        # Tworzymy użytkownika
        self.user = User.objects.create_user(username='testuser', email='uzytkownik@o2.pl', password='testpassword')

        # Tworzymy książkę
        self.publisher_data = {'name': 'publisherTest', 'email': 'Publoisher@o2.pl', 'website': 'www.testwebsite.com'}
        self.publisher = Publisher.objects.create(**self.publisher_data)
        self.book = Book.objects.create(title='Test Book', publication_date=datetime.now(), isbn='1234567890',
                                        publisher=self.publisher)

    def test_review_edit_get(self):
        # Test GET request to review_edit view
        url = reverse('review_edit', args=[self.book.id])
        request = self.factory.get(url)
        request.user = self.user
        response = review_edit(request, self.book.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instance-form.html')
        self.assertIsInstance(response.context['form'], ReviewForm)

    def test_review_edit_post(self):
        # Test POST request to review_edit view
        url = reverse('review_edit', args=[self.book.pk])
        data = {
            'content': 'Test content',
            'rating': 4
        }
        request = self.factory.post(url, data)
        request.user = self.user
        response = review_edit(request, self.book.pk)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post
        self.assertRedirects(response, reverse('book_detail', args=[self.book.pk]))

        # Verify that the review was created
        self.assertEqual(Review.objects.count(), 1)
        created_review = Review.objects.first()
        self.assertEqual(created_review.content, 'Test content')
        self.assertEqual(created_review.rating, 4)
        self.assertEqual(created_review.creator, self.user)

    def test_review_edit_post_invalid_form(self):
        # Test POST request with invalid form data
        url = reverse('review_edit', args=[self.book.pk])
        data = {
            'content': '',  # Invalid data, should trigger form validation error
            'rating': 4
        }
        request = self.factory.post(url, data)
        request.user = self.user
        response = review_edit(request, self.book.pk)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page after invalid post
        self.assertTemplateUsed(response, 'instance-form.html')
        self.assertIsInstance(response.context['form'], ReviewForm)
        self.assertIn('form', response.context)
        self.assertIn('instance', response.context)
        self.assertIn('model_type', response.context)
        self.assertIn('related_instance', response.context)
        self.assertIn('related_model_type', response.context)