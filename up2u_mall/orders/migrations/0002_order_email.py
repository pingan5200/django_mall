# Generated by Django 2.1.5 on 2019-01-23 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='de8ug@foxmail.com', max_length=254),
            preserve_default=False,
        ),
    ]
