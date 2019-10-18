from .models import Category, Tag


def menu(request):
    cats = Category.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    return {'cats': cats, 'tags': tags}
