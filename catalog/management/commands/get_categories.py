from threading import Thread
from requests_html import HTMLSession
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalog.models import Category


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    cat_urls = response.html.xpath('//url/loc')

    for cat_url in cat_urls:
        name = '/'.join(cat_url.text.split('/')[3:-1])

        category = {
            'name': name,
            'slug': slugify(name),
            'description': name
        }
        print('category:', category)

        Category.objects.create(**category)


class Command(BaseCommand):
    help = 'Category Scraper'

    def handle(self, *args, **options):
        url = 'https://freeessays.page/category-sitemap.xml/'
        Thread(target=crawler, args=(url, )).start()
        print('Done!')
