# Generated by Django 3.1.2 on 2020-10-07 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='issue_description',
            field=models.TextField(default='Sem descrição'),
            preserve_default=False,
        ),
    ]
