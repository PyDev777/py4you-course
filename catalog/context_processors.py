from .models import Category, Tag
from cache_memoize import cache_memoize


@cache_memoize(60*5)
def menu(request):
    cats = Category.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    return {'cats': cats, 'tags': tags}
