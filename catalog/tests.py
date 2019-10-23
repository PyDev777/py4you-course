from django.test import TestCase, RequestFactory
from .management.commands.get_essays import crawler, urls_generator
from datetime import datetime
from .models import *

from task.models import Task
from .views import EssayDetailView


class BookTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_urls_generator(self):
        task = Task.objects.create(task='asd')
        gen = urls_generator(0, 10, task)
        result = list(gen)
        self.assertEqual(len(result), 10)

    def test_crawler(self):
        count = Essay.objects.all().count()
        self.assertEqual(count, 0)
        url = 'https://freeessays.page/why-marriage-is-still-important/'
        crawler(url)
        count = Essay.objects.all().count()
        self.assertEqual(count, 1)

    def test_essay_view(self):
        date_now = datetime.now()
        essay = {
            'name': 'name',
            'slug': 'slug',
            'description': 'description1',
            'published': date_now,
        }
        Essay.objects.create(**essay)
        count = Essay.objects.all().count()
        self.assertEqual(count, 1)

        request = self.factory.get('/essay/slug')
        response = EssayDetailView.as_view()(request, slug='slug')
        self.assertTemplateUsed('essay.html')
        self.assertEqual(response.status_code, 200)

        r_context_data = response.context_data
        self.assertIn('reviews', r_context_data)
        self.assertIn('essay', r_context_data)
        self.assertIn('object', r_context_data)
