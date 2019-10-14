from django.shortcuts import render

# Create your views here.


def index_view(request):
    context = {}
    return render(request, 'home.html', context)


def catalog_view(request):
    context = {}
    return render(request, 'catalog.html', context)


def essay_view(request):
    context = {}
    return render(request, 'essay.html', context)
