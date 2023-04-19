# Generated by Django 4.1.7 on 2023-03-15 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_person_gender'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE "content"."genre_film_work"
                ADD CONSTRAINT "genre_film_work_film_work_id_genre_id_uniq"
                UNIQUE ("film_work_id", "genre_id");
                """,
            reverse_sql="""
                ALTER TABLE "content"."genre_film_work"
                DROP CONSTRAINT "genre_film_work_film_work_id_genre_id_uniq"
                """,
        )
    ]
