from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from catalog.models import *


class EssayAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_filter = ['published', 'cat', 'tag']
    list_display = ['name', 'published']
    list_editable = []
    search_fields = ['name']


class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('comment',)
    list_filter = ['published', 'moderated']
    list_display = ['name', 'website', 'published', 'rating', 'moderated']
    list_editable = ['moderated']
    search_fields = ['name']


# Register your models here.
admin.site.register(Category)
admin.site.register(Essay, EssayAdmin)
admin.site.register(Tag)
admin.site.register(Review, ReviewAdmin)
