from django.shortcuts import render
from django.utils.html import format_html, strip_tags
from .models import *


def index_view(request):

    cats = Category.objects.all().values('id', 'name')
    tags = Tag.objects.all().values('id', 'name')
    context = {'cats': cats, 'tags': tags}
    return render(request, 'home.html', context)


def essay_view(request, **kwargs):

    essay_id = kwargs.get('id')

    essay = Essay.objects.filter(id=essay_id).values()[0]
    essay['description'] = format_html(essay['description'])
    context = {'essay': essay}

    return render(request, 'essay.html', context)


def essays_view(request):

    # search_input = request.GET.get('search_input', '')
    cat = request.GET.get('category', '')
    # tag = request.GET.get('tag', 'No Tag')

    essays = Essay.objects.filter(cat__id=cat).values('id', 'name', 'description', 'published')

    for el in essays:
        el['descr'] = strip_tags(el['description'])[:250] + '...'
        el['description'] = format_html(el['description'])

    context = {'essays': essays, 'cat': cat}

    return render(request, 'essays.html', context)
