from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from catalog.models import Essay, Category, Tag


class EssayAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)


# Register your models here.
admin.site.register(Category)
admin.site.register(Essay, EssayAdmin)
admin.site.register(Tag)
