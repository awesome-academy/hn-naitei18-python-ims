from django.test import TestCase

from myalbums.models import *

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name_category='Dung', thumbnail='avatar.jpg')

    def test_name_category_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name_category').verbose_name
        self.assertEquals(field_label, 'name category')

    def test_thumbnail_label(self):
        category=Category.objects.get(id=1)
        field_label = category._meta.get_field('thumbnail').verbose_name
        self.assertEquals(field_label, 'thumbnail')

    def test_name_category_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name_category').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_name_category(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name_category
        self.assertEquals(expected_object_name, str(category))

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(category.get_absolute_url(), '/category/1')