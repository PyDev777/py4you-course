import sys
from requests_html import HTMLSession
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings

from catalog.models import *


def crawler(url):

    # print(f'Crawler started with url: {url}')

    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath('//h1')[0].text
    # print(f'name: {name}')

    slug = slugify(name)
    # print(f'slug: {slug}')

    # Remove banner ad, save other html tags in description
    description = response.html.xpath('//div[@class="entry-content"]/*[not(self::div)]')
    description = ''.join([el.html for el in description]) if description else ''
    # print(f'description: {description}')

    published = response.html.xpath('//div[@class="entry-date"]/time')[0].text
    published = datetime.strptime(published, '%B %d, %Y')
    # print(f'published: {published}')

    image_name = ''
    img_source = response.html.xpath('//div[@class="entry-content"]/p/img/@src')

    if img_source:
        # print(f'img_source is True')

        img_source = img_source[0]
        # print(f'img_source: {img_source}')

        try:
            with HTMLSession() as session2:
                img_resp = session2.get(img_source)

            if img_resp:
                # print(f'img_resp is True')

                image_name = slug + '.' + img_source.split('.')[-1]
                image_fname = f'{settings.MEDIA_URL[1:]}{settings.IMG_UPLOAD_TO}/{image_name}'
                print(f'image_fname: {image_fname}')

                with open(image_fname, 'wb') as imgf:
                    imgf.write(img_resp.content)

            del img_resp
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno)
    else:
        img_source = ''

    essay = {
        'name': name,
        'slug': slug,
        'description': description,
        'published': published,
        'essay_source': url,
        'img': image_name,
        'img_source': img_source,
    }

    # print(f'Essay: {essay}')

    try:
        essay = Essay.objects.create(**essay)
    except Exception as e:
        print(type(e), e)
        return

    cat = response.html.xpath('//div[@class="entry-info"]/div[@class="entry-tax"]/a[@rel="category"]')
    cat = cat[0].text if cat else '-'
    cat = {'name': cat, 'slug': slugify(cat), 'description': ''}
    cat, created = Category.objects.get_or_create(**cat)
    essay.cat.add(cat)

    tag = response.html.xpath('//footer[@class="entry-meta"]/div[@class="entry-tax"]/a[@rel="tag"]')
    tag = tag[0].text if tag else '-'
    tag, created = Tag.objects.get_or_create(name=tag)
    essay.tag.add(tag)

    print(f'Essay saved: {name}')


def urls_list():

    # https://freeessays.page/post-sitemap1.xml
    # https://freeessays.page/post-sitemap2.xml
    # https://freeessays.page/post-sitemap3.xml

    with HTMLSession() as session:
        response = session.get('https://freeessays.page/post-sitemap1.xml')  # 1000 essays!

    essay_urls = response.html.xpath('//url/loc')
    if essay_urls:
        return [essay_url.text for essay_url in essay_urls if essay_url]  # [0:1000]
    else:
        print('Error: essay_urls is empty!')
        return []


class Command(BaseCommand):
    help = 'Essays Scraper'

    def handle(self, *args, **options):

        url_gen = urls_list()

        if url_gen:
            with ThreadPoolExecutor(max_workers=1) as executor:  # Only 1 worker!
                executor.map(crawler, url_gen)
            print('Done!')
        else:
            print('Error! Essays Urls not found!')
