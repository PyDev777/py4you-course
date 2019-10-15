from requests_html import HTMLSession
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from catalog.models import *


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath('//h1')[0].text

    # Remove banner ad, save other html tags in description
    description = response.html.xpath('//div[@class="entry-content"]/*[not(self::div)]')
    description = ''.join([el.html for el in description]) if description else ''

    published = response.html.xpath('//div[@class="entry-date"]/time')[0].text
    published = datetime.strptime(published, '%B %d, %Y')

    # img_source = response.html.xpath('//div[@class="entry-content"]/p/img/@src')

    essay = {
        'name': name,
        'slug': slugify(name),
        'description': description,
        'published': published,
        'essay_source': url,
    }

    try:
        essay = Essay.objects.create(**essay)
    except Exception as e:
        print(type(e), e)
        return

    cat = response.html.xpath('//div[@class="entry-info"]/div[@class="entry-tax"]/a[@rel="category"]')
    cat = cat[0].text if cat else 'No Category'
    cat = {'name': cat, 'slug': slugify(cat), 'description': ''}
    cat, created = Category.objects.get_or_create(**cat)
    essay.cat.add(cat)

    tag = response.html.xpath('//footer[@class="entry-meta"]/div[@class="entry-tax"]/a[@rel="tag"]')
    tag = tag[0].text if tag else 'No Tag'
    tag, created = Tag.objects.get_or_create(name=tag)
    essay.tag.add(tag)

    print('Essay saved:', name)


def urls_list():

    # https://freeessays.page/post-sitemap1.xml
    # https://freeessays.page/post-sitemap2.xml
    # https://freeessays.page/post-sitemap3.xml

    with HTMLSession() as session:
        response = session.get('https://freeessays.page/post-sitemap1.xml')  # 1000 essays!

    essay_urls = response.html.xpath('//url/loc')
    if essay_urls:
        return [essay_url.text for essay_url in essay_urls if essay_url][800:900]  # Saved: [0:100], [900:1000]
    else:
        print('Error: essay_urls is empty!')
        return []


class Command(BaseCommand):
    help = 'Essays Scraper'

    def handle(self, *args, **options):

        url_gen = urls_list()
        if url_gen:
            with ThreadPoolExecutor(max_workers=2) as executor:  # Only 2 workers for server tolerance!
                executor.map(crawler, url_gen)
            print('Done!')
        else:
            print('Error! Essays Urls not found!')
