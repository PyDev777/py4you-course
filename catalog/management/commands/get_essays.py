from threading import Thread
from requests_html import HTMLSession
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime

from catalog.models import *

# https://freeessays.page/category-sitemap.xml
# https://freeessays.page/post_tag-sitemap.xml
# https://freeessays.page/post-sitemap1.xml


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath('//h1')[0].text

    description = response.html.xpath('//div[contains(@class,"entry-content")]')[0].text
    description = '\n'.join([f'<p>{p}</p>' for p in description.split('\n') if p])

    # published = response.html.xpath('//div[@class="entry-date"]/time/@datetime')[0]  # 2019-09-03T09:08:48+00:00
    published = response.html.xpath('//div[@class="entry-date"]/time')[0].text
    published = datetime.strptime(published, '%B %d, %Y')

    # img_source = response.html.xpath('//img[@id="coverImage"]/@src')[0]
    # parsing_date = ''

    cat = ''
    tag = ''

    essay = {
        'name': name,
        'slug': slugify(name),
        # 'img_source': img_source,
        'essay_source': url,
        'description': description,
        'published': published,
    }

    print(essay)

    # Essay.objects.create(**essay)


class Command(BaseCommand):
    help = 'Running books scraper'

    def handle(self, *args, **options):
        url = 'https://freeessays.page/why-marriage-is-still-important/'
        Thread(target=crawler, args=(url, )).start()
        print('Done!')
