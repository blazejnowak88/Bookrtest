from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from reviews.models import Book, Review, Publisher
from datetime import datetime

# Create your tests here.


class AuthTest(TestCase):


    def test_create_user(self):
        url = reverse('register_view')
        response = self.client.post(url, {'username': 'test', 'email': 'text@o2.pl', 'password': 'Passtest', 're_password': 'Passtest'})
        u = User.objects.get(username='test')
        self.assertIsNotNone(u)


    def test_login_view(self):
        url = reverse('register_view')
        self.client.post(url, {'username': 'test', 'email': 'text@o2.pl', 'password': 'Passtest',
                                          're_password': 'Passtest'})
        response = self.client.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('login_view'), {'username': 'test', 'password': 'Passtest',})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        url = reverse('register_view')
        self.client.post(url, {'username': 'test', 'email': 'text@o2.pl', 'password': 'Passtest',
                                          're_password': 'Passtest'})
        response = self.client.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('login_view'), {'username': 'test', 'password': 'Passtest',})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        response = self.client.get(reverse('logout_view'))
        self.assertEqual(response.status_code, 302)  # Redirect status after logout
        self.assertRedirects(response, reverse('home'))


#
#
class HomeProfileReadingHistoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {'username': 'testuser', 'password': 'testpassword'}
        self.user = User.objects.create_user(**self.user_data)
        self.publisher_data = {'name': 'publisher', 'email': 'test@o2.pl', 'website': 'www.website.com'}
        self.publisher = Publisher.objects.create(**self.publisher_data)

        self.book = Book.objects.create(title='Test Book', publication_date=datetime.now(), isbn='1234567890', publisher = self.publisher)
        self.review = Review.objects.create(creator=self.user, book=self.book, content='Test', rating=4)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')  # Check if the book is present in the profile

    def test_reading_history_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile', ))

        self.assertContains(response, self.book.title)

    def test_review_create(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('review_create', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('review_create', args=[self.book.id]), dict(creator = self.user.id, content='Test', rating=4))
        print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_detail', args=[self.book.id]))


        # self.assertEqual(response.get('Content-Type'), 'application/vnd.ms-excel')

