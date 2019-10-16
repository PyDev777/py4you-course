from django.shortcuts import render
from django.utils.html import format_html
from .models import Essay


def index_view(request):
    context = {}
    return render(request, 'home.html', context)


def catalog_view(request):
    context = {}
    return render(request, 'catalog.html', context)


def essay_view(request):

    essay = Essay.objects.filter(id=104).values()[0]

    essay['description'] = format_html(essay['description'])
    # essay['category'], essay['tag'] = essay.cat.name, essay.tag.name

    context = {'essay': essay}
    # print('context:', context)

    return render(request, 'essay.html', context)
