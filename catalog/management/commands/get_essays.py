from threading import Thread
from requests_html import HTMLSession
from django.core.management.base import BaseCommand

from catalog.models import *


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath('//h1')[0].text
    print('description: ', name)
    description = response.html.xpath('//div[@class="entry-content"]')
    print('description: ', description)
    # description = response.html.xpath('//div[@id="description"]/span[2]')[0].text
    # img_source = response.html.xpath('//img[@id="coverImage"]/@src')[0]

    slug = ''
    published = ''
    essay_source = ''
    parsing_date = ''
    cat = ''
    char = ''



    essay = {
        'name': name,
        # 'img_source': img_source,
        'essay_source': url,
        'description': description
    }

    print(essay)

    # Essay.objects.create(**essay)


class Command(BaseCommand):
    help = 'Running books scraper'

    def handle(self, *args, **options):
        url = 'https://freeessays.page/argumentative-essay-statement-in-opposition-to-distant-learning/'
        Thread(target=crawler, args=(url, )).start()
        print('Done!')
