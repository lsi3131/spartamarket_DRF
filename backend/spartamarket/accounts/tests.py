import time

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import *
import json


class AccountAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()
        # 테스트를 위한 데이터 설정 등

    def test_when_invalid_data(self):
        url = reverse('accounts:signup')
        data = {
            'nothing': 'n',
            'to': 'x'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_when_signup_finish_then_login(self):
        url = reverse('accounts:signup')
        data = {
            'username': 'user',
            'password': 'user1234'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(User.objects.filter(username='user').exists())

    def test_signup_duplicate(self):
        url = reverse('accounts:signup')
        data1 = {
            'username': 'user',
            'password': 'user1234'
        }

        data2 = {
            'username': 'user',
            'password': 'user1234'
        }

        response = self.client.post(url, data=json.dumps(data1), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        response = self.client.post(url, data=json.dumps(data2), content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_login(self):
        url = reverse('accounts:login')
        data1 = {
            'username': 'user',
            'password': 'pass'
        }
        response = self.client.post(url, data=json.dumps(data1), content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        User.objects.create_user(username='user', password='pass')
        response = self.client.post(url, data=json.dumps(data1), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put_user_profile(self):
        User.objects.create_user(username='user', password='user')
        url = reverse('accounts:profile', args=['user'])
        email = 'test@test.con'
        put_data = {
            "email": f"{email}",
            "nickname": "silee",
            "birthday": "1991-06-11"
        }
        response = self.client.put(url, data=json.dumps(put_data), content_type='application/json')
        self.assertEqual(email, response.data['email'])
        self.assertEqual('silee', response.data['nickname'])
        self.assertEqual('1991-06-11', response.data['birthday'])

        # 동일한 데이터 다시 put 진행 시 실패
        response = self.client.put(url, data=json.dumps(put_data), content_type='application/json')
        self.assertEqual(f'email(={email}) already exists', response.data['message'])

    def test_put_password(self):
        User.objects.create_user(username='user', password='pass')
        url = reverse('accounts:password', args=['user'])
        put_data = {
            "new_password": "",
        }
        response = self.client.put(url, data=json.dumps(put_data), content_type='application/json')
        self.assertEqual('password is empty', response.data['message'])

        put_data['new_password'] = 'new_password'
        response = self.client.put(url, data=json.dumps(put_data), content_type='application/json')
        self.assertEqual('password changed successfully', response.data['message'])

    def test_delete_user(self):
        user = User.objects.create_user(username='user', password='pass')
        url = reverse('accounts:delete', args=[user.username])

        delete_data = {
            'password': 'invalid_pass'
        }
        # 로그인 안되었을 때 삭제 실패
        response = self.client.delete(url, data=json.dumps(delete_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 로그인 진행
        self.client.force_authenticate(user)

        # 비밀번호가 일치하지 않을 경우 삭제 실패
        response = self.client.delete(url, data=json.dumps(delete_data), content_type='application/json')
        self.assertEqual(f'password is not match', response.data['message'])

        # 비밀번호가 일치할 경우 삭제
        delete_data['password'] = 'pass'
        response = self.client.delete(url, data=json.dumps(delete_data), content_type='application/json')
        self.assertEqual(f'"user" is deleted.', response.data['message'])

    def test_add_following_multi(self):
        user = User.objects.create_user(username='user', password='password')
        follower1 = User.objects.create_user(username='user1', password='password')
        url = reverse('accounts:following', args=[user.username])
        data = {
            'follower': follower1.username
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(f'{follower1.username} is added.', response.data['message'])

        follower2 = User.objects.create_user(username='user2', password='password')
        data['follower'] = follower2.username
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(f'{follower2.username} is added.', response.data['message'])

    def test_delete_following_multi(self):
        user = User.objects.create_user(username='user', password='password')
        follower1 = User.objects.create_user(username='user1', password='password')
        user.following.add(follower1)

        url = reverse('accounts:following', args=[user.username])
        data = {
            'follower': follower1.username
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(f'{follower1.username} is deleted.', response.data['message'])

        self.assertEqual(0, user.following.count())
