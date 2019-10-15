from threading import Thread
from requests_html import HTMLSession
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime

from catalog.models import *


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    names = response.html.xpath('//url/loc')

    for name in names:
        print('name:', name.text)

    # for name in names:
    #
    #     category = {
    #         'name': name,
    #         'slug': slugify(name),
    #         'description': name
    #     }
    #
    #     print('category:', category)

        # Category.objects.create(**essay)


class Command(BaseCommand):
    help = 'Category Scraper'

    def handle(self, *args, **options):
        url = 'https://freeessays.page/category-sitemap.xml/'
        Thread(target=crawler, args=(url, )).start()
        print('Done!')


# https://freeessays.page/analytical-essays/
# https://freeessays.page/argumentative-essays/
# https://freeessays.page/assignments/
# https://freeessays.page/book-reports/
# https://freeessays.page/free-papers/business/
# https://freeessays.page/case-study/
# https://freeessays.page/cause-and-effect-essays/
# https://freeessays.page/classification-essay/
# https://freeessays.page/compare-and-contrast/
# https://freeessays.page/coursework/
# https://freeessays.page/critical-essays/
# https://freeessays.page/definition-essays/
# https://freeessays.page/descriptive-essays/
# https://freeessays.page/free-papers/drugs/
# https://freeessays.page/free-papers/economics/
# https://freeessays.page/free-papers/book-reviews/
# https://freeessays.page/free-papers/
# https://freeessays.page/free-papers/history/
# https://freeessays.page/writing-guide/
# https://freeessays.page/informative-essays/
# https://freeessays.page/lab-reports/
# https://freeessays.page/free-papers/love-and-relationships/
# https://freeessays.page/free-papers/management/
# https://freeessays.page/narrative-essay/
# https://freeessays.page/personal-narrative/
# https://freeessays.page/personal-statement/
# https://freeessays.page/persuasive-essays/
# https://freeessays.page/premium-essays/
# https://freeessays.page/problem-solution-essays/
# https://freeessays.page/profile-essays/
# https://freeessays.page/quantitative-research/
# https://freeessays.page/reflective-essays/
# https://freeessays.page/research-essays/
# https://freeessays.page/research-papers/
# https://freeessays.page/rhetorical-essays/
# https://freeessays.page/satire-essays/
# https://freeessays.page/free-papers/social-issues-and-civics/
# https://freeessays.page/synthesis-essays/
