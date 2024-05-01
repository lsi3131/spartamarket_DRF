import json

from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


def create_items(items: list):
    for item in items:
        Item.objects.create(title=item['title'], content=item['content'])


class ItemsListAPIViewTestCase(TestCase):
    def login_as_user(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)

    def login_as_admin(self):
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.client.force_authenticate(user=self.user)

    def request_get_item_list_and_get_response(self, category, keyword, sort, page):
        url = reverse('items:item_list') + f'?category={category}&keyword={keyword}&sort={sort}&page={page}'
        response = self.client.get(url)
        data = response.json()
        results = data['results']
        return response.status_code, results

    def setUp(self):
        self.client = APIClient()
        self.user = None
        # 테스트를 위한 데이터 설정 등

    def test_login(self):
        pass

    def test_get_items_with_pagination(self):
        for i in range(1, 100):
            create_items([
                {'title': f'test{i}', 'content': f'content{i}'},
            ])

        category = 'title'
        keyword = ''
        sort = 'oldest'
        status_code, results = self.request_get_item_list_and_get_response(category, keyword, sort, page=1)
        self.assertEqual(status_code, status.HTTP_200_OK)
        i = 1 + (20 * 0)
        for result in results:
            self.assertEqual(f'content{i}', result['content'])
            i += 1

        status_code, results = self.request_get_item_list_and_get_response(category, keyword, sort, page=2)
        self.assertEqual(status_code, status.HTTP_200_OK)
        i = 1 + (20 * 1)
        for result in results:
            self.assertEqual(f'content{i}', result['content'])
            i += 1

        status_code, results = self.request_get_item_list_and_get_response(category, keyword, sort, page=3)
        self.assertEqual(status_code, status.HTTP_200_OK)
        i = 1 + (20 * 2)
        for result in results:
            self.assertEqual(f'content{i}', result['content'])
            i += 1

    def test_get_items_with_search(self):
        create_items([
            {'title': f'title0', 'content': f'nothing'},
            {'title': f'title1', 'content': f'nothing'},
            {'title': f'title2', 'content': f'nothing'},
        ])

        create_items([
            {'title': f'nothing', 'content': f'content0'},
            {'title': f'nothing', 'content': f'content1'},
        ])

        _, results = self.request_get_item_list_and_get_response(category='title', keyword='title', sort='oldest',
                                                                 page=1)
        self.assertEqual(f'title0', results[0]['title'])
        self.assertEqual(f'title1', results[1]['title'])
        self.assertEqual(f'title2', results[2]['title'])

        _, results = self.request_get_item_list_and_get_response(category='content', keyword='content', sort='oldest',
                                                                 page=1)
        self.assertEqual(f'content0', results[0]['content'])
        self.assertEqual(f'content1', results[1]['content'])

    def test_add_items(self):
        self.login_as_user()
        url = reverse('items:item_list')
        data = {
            'title': 'title1',
            'content': 'content1',
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        results = Item.objects.all()
        self.assertEqual(('title1', 'content1'), (results[0].title, results[0].content))

    def test_put_item(self):
        self.login_as_user()
        item = Item.objects.create(title='title1', content='content1', user=self.user)

        url = reverse('items:item_list', args=[item.id])
        data = {
            'title': 'title2',
            'content': 'content2',
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        db_item = Item.objects.first()
        self.assertEqual(('title2', 'content2'), (db_item.title, db_item.content))

    def test_delete_item(self):
        self.login_as_user()
        item = Item.objects.create(title='title1', content='content1', user=self.user)
        url = reverse('items:item_list', args=[item.id])
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        db_item = Item.objects.first()
        self.assertEqual(None, db_item)

    def test_add_category_only_admin_possible(self):
        url = reverse('items:category')
        data = {
            'name': 'category',
        }
        # 일반 유저 category 생성 불가
        self.login_as_user()
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        # admin 유저 category 생성 가능
        self.login_as_admin()
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        db_item = Category.objects.first()
        self.assertEqual('category', db_item.name)

    def test_add_category_and_set_item(self):
        self.login_as_user()
        # post 진행
        cate1 = Category.objects.create(name='cate1')
        data = {
            'title': 'title1',
            'content': 'content1',
            'category': cate1.id
        }
        url = reverse('items:item_list')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        item = Item.objects.first()
        self.assertEqual(cate1.id, item.category.id)
        self.assertEqual(cate1.name, item.category.name)

        # put 진행
        cate2 = Category.objects.create(name='cate2')
        url = reverse('items:item_list', args=[item.id])
        data['category'] = cate2.id
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        item = Item.objects.first()
        self.assertEqual(cate2.id, item.category.id)
        self.assertEqual(cate2.name, item.category.name)
