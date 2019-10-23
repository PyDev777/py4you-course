import sys
from requests_html import HTMLSession
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
# from django.conf import settings
from threading import Lock

from catalog.models import *


locker = Lock()


def crawler(url):

    print(f'crawler: url={url}')

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
    # print(f'crawler: Essay={essay}')

    try:
        with locker:
            essay = Essay.objects.create(**essay)
    except Exception as e:
        print(type(e), e)
        return
    # print(f'crawler: Essay is created.')

    cat = response.html.xpath('//div[@class="entry-info"]/div[@class="entry-tax"]/a[@rel="category"]')
    cat = cat[0].text if cat else '-'
    cat = {'name': cat, 'slug': slugify(cat), 'description': ''}
    with locker:
        cat, created = Category.objects.get_or_create(**cat)
        essay.cat.add(cat)
    # print(f'crawler: cat added to Essay.')

    tag = response.html.xpath('//footer[@class="entry-meta"]/div[@class="entry-tax"]/a[@rel="tag"]')
    tag = tag[0].text if tag else '-'
    with locker:
        tag, created = Tag.objects.get_or_create(name=tag)
        essay.tag.add(tag)
    # print(f'crawler: tag added to Essay.')

    print(f'crawler: DONE.')


def urls_generator(start, end, task):
    print(f'urls_generator: start={start}, end={end}')

    # https://freeessays.page/post-sitemap1.xml
    # https://freeessays.page/post-sitemap2.xml
    # https://freeessays.page/post-sitemap3.xml

    with HTMLSession() as session:
        response = session.get('https://freeessays.page/post-sitemap1.xml')  # 1000 essays!

    essay_urls = response.html.xpath('//url/loc')
    if essay_urls:

        urls = [essay_url.text for essay_url in essay_urls if essay_url]  # [0:1000]
        print(f'urls_generator: len(urls) = {len(urls)}')
        end_max = len(urls)

        if end > end_max:
            end = end_max

        if start > end:
            start = end

        for i in range(start, end):
            url = urls[i]
            # print(f'urls_generator: url={url}')
            with locker:
                task.status = f'urls No: {i}'
                task.save()
            yield url


def run_crawler(start, end, task):

    print(f'run_crawler: start={start}, end={end}')

    with locker:
        task.status = 'start parsing'
        task.save()
    # print(f'run_crawler: task.save - start parsing')
    url_gen = urls_generator(start, end, task)

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(crawler, url_gen)
    task.status = 'finished'
    task.end_time = datetime.now()
    task.save()
    # print(f'run_crawler: task.save - finished')
    print(f'run_crawler: DONE.')


class Command(BaseCommand):
    help = 'Essays Scraper'

    def handle(self, *args, **options):
        from task.models import Task

        task = Task.objects.create(name='run_scraper')
        run_crawler(0, 20, task)
