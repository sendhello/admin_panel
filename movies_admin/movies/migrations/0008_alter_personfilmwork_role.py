# Generated by Django 4.1.7 on 2023-04-15 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_alter_filmwork_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.TextField(
                choices=[
                    ('actor', 'actor'), ('writer', 'writer'), ('director', 'director')
                ],
                null=True,
                verbose_name='profession'
            ),
        ),
    ]
