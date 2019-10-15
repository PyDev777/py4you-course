from django.db import models
from django.conf import settings


class Category(models.Model):

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Tag(models.Model):

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Essay(models.Model):

    class Meta:
        verbose_name = 'Essay'
        verbose_name_plural = 'Essays'

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    published = models.DateField()
    img = models.ImageField(blank=True, default='', upload_to=settings.IMG_UPLOAD_TO)
    img_source = models.URLField(max_length=255, blank=True, default='')
    essay_source = models.URLField(max_length=255, blank=True, default='')
    parsing_date = models.DateTimeField(auto_now=True)
    cat = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
