from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from authors.models import AppUser

# Create your tests here.
class AuthorTests(TestCase):
  def createAuthor(self):
    return get_user_model().objects.create_user(email='test@email.com', password='test1234') 

  def test_register_author(self):
    User = get_user_model()
    all_users = User.objects.all()
    self.assertEqual(len(all_users), 0)
    data = {
      'email': 'test@email.com',
      'username': 'test',
      'password': 'test1234'
    }
    response = self.client.post(reverse("register"), data)
    self.assertEqual(response.status_code, 201)
    User = get_user_model()
    all_users = User.objects.all()
    self.assertEqual(len(all_users), 1)

  def test_login_author(self):
    User = self.createAuthor()
    response = self.client.post(reverse("login"), {'email': User.email, 'password': 'test1234'})
    print("Response: ", dir(response))
    self.assertEqual(response.status_code, 200)

  def test_view_all_authors(self):
    response = self.client.get(reverse("user"))
    get_user_model().objects.create_user(email='test@email.com', password='test1234') 
    get_user_model().objects.create_user(email='test1@email.com', password='test1234') 
    print("Response: ", response)


from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass123'
        )

    def test_user_view_unauthenticated(self):
        response = self.client.get(reverse('user'))
        self.assertNotEqual(response.status_code, 200)
        # Check for redirect or forbidden response

    def test_user_view_authenticated(self):
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('user'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_user_details_view_unauthenticated(self):
        user_id = self.user.pk
        response = self.client.get(reverse('user-detail', kwargs={'pk': user_id}))
        self.assertNotEqual(response.status_code, 200)
        # Check for redirect or forbidden response

    def test_user_details_view_authenticated(self):
        self.client.login(email='test@example.com', password='testpass123')
        user_id = self.user.pk
        response = self.client.get(reverse('user-detail', kwargs={'pk': user_id}))
        self.assertEqual(response.status_code, 200)
        self.client.logout()