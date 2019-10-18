from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html, strip_tags
from .models import *


def index_view(request):

    # cats = Category.objects.all().values('id', 'slug', 'name')
    # tags = Tag.objects.all().values('id', 'name')
    # context = {'cats': cats, 'tags': tags}

    return render(request, 'home.html', context={})


def essay_view(request, **kwargs):

    slug = kwargs.get('slug')
    cat_name = kwargs.get('cat_name')

    essay = get_object_or_404(Essay, slug=slug)
    essay.description = format_html(essay.description)

    context = {'essay': essay, 'cat_name': cat_name}

    return render(request, 'essay.html', context)


def essays_view(request):

    qi = request.GET.get('search_input', '')

    cat = request.GET.get('category', '')
    cat = int(cat) if cat else 0

    tag = request.GET.get('tag', '')
    tag = int(tag) if tag else 0

    # print(f'qi={qi}, cat={cat}, tag={tag}')

    essays = []
    cat_name = ''

    if qi:
        pass
        # essays = Essay.objects.filter(slug__contains=qi).values('id', 'slug', 'name', 'description', 'published')
    else:
        if cat:
            essays = Essay.objects.filter(cat__id=cat).values('id', 'slug', 'name', 'description', 'published')
            cat_name = get_object_or_404(Category, id=cat)
            # print(f'cat_name={cat_name}')
        else:
            if tag:
                essays = Essay.objects.filter(tag__id=tag).values('id', 'slug', 'name', 'description', 'published')
                cat_name = get_object_or_404(Tag, id=tag)
                # print(f'tag_name={cat_name}')
            else:
                pass
                # essays = Essay.objects.all().values('id', 'slug', 'name', 'description', 'published')

    for essay in essays:
        essay['descr'] = strip_tags(essay['description'])[:250] + '...'

    # print(f'essays={essays}')

    context = {'essays': essays, 'cat_name': cat_name}

    return render(request, 'essays.html', context)


def robots_view(request):
    return render(request, 'robots.txt', {}, content_type="text/plain")
