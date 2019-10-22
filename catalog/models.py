from django.db import models
from django.conf import settings
from django.utils.html import strip_tags


class Category(models.Model):

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Tag(models.Model):

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Essay(models.Model):

    class Meta:
        verbose_name = 'Essay'
        verbose_name_plural = 'Essays'

    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    published = models.DateField(db_index=True)
    img = models.ImageField(blank=True, default='', upload_to=settings.IMG_UPLOAD_TO)
    img_source = models.URLField(max_length=255, blank=True, default='')
    essay_source = models.URLField(max_length=255, blank=True, default='')
    parsing_date = models.DateTimeField(auto_now=True)
    cat = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)

    @property
    def descr(self):
        return strip_tags(self.description[:250]) + '...'

    def __str__(self):
        return self.name


class Review(models.Model):

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField()
    comment = models.TextField()
    rating = models.IntegerField()
    website = models.URLField()
    published = models.DateField(auto_now=True, db_index=True)
    moderated = models.BooleanField(default=False)

    essay = models.ForeignKey(Essay, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
