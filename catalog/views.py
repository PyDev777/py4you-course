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

    q_params = {}
    cat_name = 0

    qi = request.GET.get('search_input', '')
    if qi:
        q_params.update(name__contains=qi)

    cat = request.GET.get('category', '')
    cat = int(cat) if cat.isdigit() else 0
    if cat:
        q_params.update(cat__id=cat)
        cat_name = get_object_or_404(Category, id=cat)

    tag = request.GET.get('tag', '')
    tag = int(tag) if tag.isdigit() else 0
    if tag:
        q_params.update(tag__id=tag)
        cat_name = get_object_or_404(Tag, id=tag)

    # print(f'q_params = {q_params}')

    essays = Essay.objects.filter(**q_params).values() if q_params else []
    # print(f'essays = {essays}')

    for essay in essays:
        essay['descr'] = strip_tags(essay['description'])[:250] + '...'

    # print(f'essays={essays}')

    context = {'essays': essays, 'cat_name': cat_name}

    return render(request, 'essays.html', context)


def robots_view(request):
    return render(request, 'robots.txt', {}, content_type="text/plain")
