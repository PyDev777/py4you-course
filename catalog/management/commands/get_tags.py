from threading import Thread
from requests_html import HTMLSession
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalog.models import Tag


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    tag_urls = response.html.xpath('//url/loc')

    for tag_url in tag_urls:
        name = tag_url.text.split('/')[-2]

        tag = {'name': name}
        print('tag:', tag)

        Tag.objects.create(**tag)


class Command(BaseCommand):
    help = 'Tag Scraper'

    def handle(self, *args, **options):
        url = 'https://freeessays.page/post_tag-sitemap.xml/'
        Thread(target=crawler, args=(url, )).start()
        print('Done!')
