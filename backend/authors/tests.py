from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from authors.serializers import UserLoginSerializer

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
    response = self.client.post(reverse("authors:register"), data)
    self.assertEqual(response.status_code, 201)
    User = get_user_model()
    all_users = User.objects.all()
    self.assertEqual(len(all_users), 1)