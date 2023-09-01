from django.test import TestCase

from accounts.models import User


# Create your tests here.
class TestRegistration(TestCase):
    def test_registration(self):
        response = self.client.post('/accounts/signup', {
            'email': 'testuser@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        })

        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].email, 'testuser@gmail.com')

    def test_user_has_100_credits_upon_registration(self):
        response = self.client.post('/accounts/signup', {
            'email': 'testuser@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        })
        users = User.objects.all()
        self.assertEqual(users[0].credits, 100)


class TestLogin(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser@gmail.com',
            'email': 'testuser@gmail.com',
            'password': 'testpassword'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/accounts/login', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_with_wrong_credentials(self):
        response = self.client.post('/accounts/login',
            {'email': 'fflfle',
            'password': 'testpassword'}, follow=True)




class TestLogoutTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser@gmail.com',
            'email': 'testuser@gmail.com',
            'password': 'testpassword'
        }

    def test_logout(self):
        response = self.client.post('/accounts/logout', self.credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


class TestUserCanSubscribe(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser@gmail.com',
            'email': 'testuser@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.credentials)


class TestUserCanDeleteHisAccount:
    def setUp(self):
        self.credentials = {
            'username': 'testuser@gmail.com',
            'email': 'testuser@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.credentials)

    def test_user_can_delete_his_account(self):
        response = self.client.post('/accounts/delete-account', self.credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        users = User.objects.all()
        self.assertEqual(users.count(), 0)


class TestUserCanUseAPIAndUploadImage(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser@gmail.com',
            'email': 'testuser@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.credentials)

    def test_user_can_generate_api_key(self):
        self.client.login(
            username=self.credentials['username'],
            password=self.credentials['password']
        )
        response = self.client.post('/accounts/generate-api-key', follow=True)
        self.assertEqual(response.status_code, 200)


class TestContactForm(TestCase):
    def test_contact_form(self):
        response = self.client.post('/contact', {
            'first_name': 'testuser',
            'name': 'testname',
            'email': 'testuser@gmail.com',
            'message': 'testmessage'
        })
        print(response.content)
        self.assertEqual(response.status_code, 200)
