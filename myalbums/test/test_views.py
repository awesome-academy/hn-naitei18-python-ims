from django.test import TestCase
from django.urls import reverse

from myalbums.models import *


class CategoryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name_category='Dung', thumbnail='avatar.jpg')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myalbums/category_list.html')