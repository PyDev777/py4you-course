# Generated by Django 2.2.6 on 2019-10-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20191022_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='published',
            field=models.DateField(auto_now=True, db_index=True),
        ),
    ]
