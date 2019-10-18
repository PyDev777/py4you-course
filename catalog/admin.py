from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from catalog.models import Essay, Category, Tag


class EssayAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_filter = ['published', 'cat', 'tag']
    list_display = ['name', 'published']
    list_editable = []
    search_fields = ['name']


# Register your models here.
admin.site.register(Category)
admin.site.register(Essay, EssayAdmin)
admin.site.register(Tag)
