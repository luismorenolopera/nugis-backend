from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class SignUpTests(APITestCase):
    def test_signup_creates_regular_user_and_token(self):
        res = self.client.post('/users/user', {
            'username': 'neo', 'first_name': 'Thomas', 'last_name': 'Anderson',
            'password': 'Wake-up-2077',
        })
        self.assertEqual(res.status_code, 201)
        self.assertNotIn('password', res.data)
        user = User.objects.get(username='neo')
        self.assertTrue(user.check_password('Wake-up-2077'))
        login = self.client.post('/api-token-auth/', {
            'username': 'neo', 'password': 'Wake-up-2077'})
        self.assertIn('token', login.data)

    def test_signup_cannot_grant_superuser(self):
        res = self.client.post('/users/user', {
            'username': 'mallory', 'password': 'Wake-up-2077',
            'is_superuser': True, 'is_staff': True,
        }, format='json')
        self.assertEqual(res.status_code, 201)
        user = User.objects.get(username='mallory')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_weak_password_rejected(self):
        res = self.client.post('/users/user', {
            'username': 'weak', 'password': '12345678'})
        self.assertEqual(res.status_code, 400)


class UserDetailTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', password='Wake-up-2077')
        self.bob = User.objects.create_user('bob', password='Wake-up-2077')
        self.client.force_authenticate(self.alice)

    def test_cannot_read_or_edit_other_users(self):
        url = '/users/user/{}'.format(self.bob.pk)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.patch(url, {'first_name': 'x'}).status_code, 404)

    def test_me_and_password_change_is_hashed(self):
        res = self.client.patch('/users/me', {'password': 'New-pass-2077'})
        self.assertEqual(res.status_code, 200)
        self.alice.refresh_from_db()
        self.assertTrue(self.alice.check_password('New-pass-2077'))
        self.assertEqual(self.client.get('/users/me').data['username'], 'alice')
