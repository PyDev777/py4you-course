import sys
from threading import Thread
from requests_html import HTMLSession
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from catalog.models import *

# https://freeessays.page/post-sitemap1.xml
# https://freeessays.page/post-sitemap2.xml
# https://freeessays.page/post-sitemap3.xml


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath('//h1')[0].text
    print('name:', name)

    description = response.html.xpath('//div[contains(@class,"entry-content")]')[0].text
    description = '\n'.join([f'<p>{p}</p>' for p in description.split('\n') if p])

    published = response.html.xpath('//div[@class="entry-date"]/time')[0].text
    published = datetime.strptime(published, '%B %d, %Y')

    # img_source = response.html.xpath('//img[@id="coverImage"]/@src')[0]

    essay = {
        'parsing_date': datetime.now(),
        'name': name,
        'slug': slugify(name),
        'description': description,
        'published': published,
        'essay_source': url,
        # 'img_source': img_source,
    }

    print(essay)

    try:
        essay = Essay.objects.create(**essay)
    except Exception as e:
        print(type(e), e)
        return

    cat = response.html.xpath('//div[@class="entry-info"]/div[@class="entry-tax"]/a[@rel="category"]')
    cat = cat[0].text if cat else 'No Category'
    print('cat:', cat)

    cat = {'name': cat, 'slug': slugify(cat), 'description': ''}
    cat, created = Category.objects.get_or_create(**cat)
    essay.cat.add(cat)

    tag = response.html.xpath('//footer[@class="entry-meta"]/div[@class="entry-tax"]/a[@rel="tag"]')
    tag = tag[0].text if tag else 'No Tag'
    print('tag:', tag)

    tag, created = Tag.objects.get_or_create(name=tag)
    essay.tag.add(tag)


def urls_list():

    with HTMLSession() as session:
        response = session.get('https://freeessays.page/post-sitemap1.xml')  # 1000 essays!

    essay_urls = response.html.xpath('//url/loc')
    if essay_urls:
        return [essay_url.text for essay_url in essay_urls if essay_url][:2]  # Only 2 first essays!
    else:
        print('Error: essay_urls is empty!')
        return []


class Command(BaseCommand):
    help = 'Essays Scraper'

    def handle(self, *args, **options):

        url_gen = urls_list()
        if url_gen:
            with ThreadPoolExecutor(max_workers=2) as executor:  # Only 2 workers!
                executor.map(crawler, url_gen)
            print('Done!')
        else:
            print('Error!')
