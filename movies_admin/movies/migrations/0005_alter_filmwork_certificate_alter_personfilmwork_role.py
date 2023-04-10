# Generated by Django 4.1.7 on 2023-03-19 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_add_index_genre_film_work"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filmwork",
            name="certificate",
            field=models.CharField(
                blank=True, max_length=512, null=True, verbose_name="certificate"
            ),
        ),
        migrations.AlterField(
            model_name="personfilmwork",
            name="role",
            field=models.TextField(
                choices=[
                    ("actor", "actor"),
                    ("producer", "producer"),
                    ("director", "director"),
                ],
                null=True,
                verbose_name="profession",
            ),
        ),
    ]