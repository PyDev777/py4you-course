# Generated by Django 2.2.6 on 2019-10-22 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20191020_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='published',
            field=models.DateField(db_index=True),
        ),
    ]
