from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from reviews.models import Book, Review


# Create your tests here.


class RegistrationTestClass(TestCase):
    def setUp(self):
        pass

    def test_create_user(self):
        url = reverse('register_view')
        response = self.client.post(url, {'username': 'test', 'email': 'text@o2.pl', 'password': 'Passtest', 're_password': 'Passtest'})
        u = User.objects.get(username='test')
        self.assertIsNotNone(u)

#
#    def test_login_view(self):
#         response = self.client.get(reverse('login'))
#         self.assertEqual(response.status_code, 200)
#
#         response = self.client.post(reverse('login'), self.user_data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('home'))

class LoginLogoutRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {'username': 'test', 'email': 'text@o2.pl', 'password': 'Passtest'}
        self.user = User.objects.create_user(**self.user_data)

    def test_login_view(self):
        response = self.client.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('login_view'), self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect status after successful login
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout_view'))
        self.assertEqual(response.status_code, 302)  # Redirect status after logout
        self.assertRedirects(response, reverse('home'))

    def test_registration_view(self):
        response = self.client.get(reverse('register_view'))
        self.assertEqual(response.status_code, 200)

        new_user_data = {'username': 'test', 'email': 'text@o2.pl', 'password': 'Passtest', 're_password': 'Passtest'}
        response = self.client.post(reverse('register_view'), new_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        print(response.content)  # poprawnie
        print(response.url)  # Wypisz URL przekierowania, jeśli istnieje
#
#
# class HomeProfileReadingHistoryViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user_data = {'username': 'testuser', 'password': 'testpassword'}
#         self.user = User.objects.create_user(**self.user_data)
#
#         self.book = Book.objects.create(title='Test Book')
#         self.review = Review.objects.create(creator=self.user, book=self.book)
#
#     def test_home_view(self):
#         response = self.client.get(reverse('home'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_profile_view(self):
#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.get(reverse('profile'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Test Book')  # Check if the book is present in the profile
#
#     def test_reading_history_view(self):
#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.get(reverse('reading_history'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.get('Content-Type'), 'application/vnd.ms-excel')

