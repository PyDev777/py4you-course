from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Essay(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    description = models.TextField()
    published = models.DateField()

    # img = models.ImageField()
    # img_source = models.URLField(max_length=255)
    # author = models.CharField(max_length=255)

    essay_source = models.URLField(max_length=255)
    parsing_date = models.DateTimeField(auto_created=True)

    cat = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
