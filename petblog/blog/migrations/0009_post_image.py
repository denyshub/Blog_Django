# Generated by Django 5.1 on 2024-08-14 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_uploadfile_alter_category_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/%Y/%m/%d', verbose_name='Фото'),
        ),
    ]