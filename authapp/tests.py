from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse


class Authtest(APITestCase):
    def setUp(self):
        self.regis_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('login')
        self.test_url = reverse('text')

        
        self.user_data = {
            'number':'number',
            'password':'user'
        }
        
        self.client.post(self.regis_url, self.user_data)
        response = self.client.post(self.login_url, self.user_data)
        self.refresh_token = response.data['refresh']
        self.access_token = response.data['access']
        
        
    def test_regis(self):
        data = {
            'number':'user1',
            'password':'userq1'
        }
        
        response=self.client.post(self.regis_url, data)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['data'],'users')
        self.assertEqual(response.data['msg'], 'siz royxatdan otdingiz')
    def test_login(self):
        response=self.client.post(self.login_url, self.user_data)
        
        self.assertEqual(response.data['access'],self.access_token)
        self.assertEqual(response.data['refresh'],self.refresh_token)
        self.assertEqual(response.status_code,200)
    
    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer"+self.access_token)
        response = self.client.post(self.logout_url, {'refresh': self.refresh_token})


        self.assertEqual(response.data['msg'],"tizimdan chiqildi")
        self.assertEqual(response.status_code,200)
    
    def test_something(self):
        response = self.client.get(self.test_url)
        
        self.assertEqual(response.status_code,401)
        self.assertIsNot(response.data['msg','something'])







