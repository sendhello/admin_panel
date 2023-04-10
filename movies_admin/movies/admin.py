from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description')

    def short_description(self, obj):
        short_text = obj.description[:70] if obj.description else ''
        return f'{short_text}...'

    short_description.short_description = _('short_description')

    search_fields = ('name',)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork

    autocomplete_fields = ('genre',)


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork

    autocomplete_fields = ('person',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_year', 'rating', 'created', 'modified')

    fields = ('title', 'creation_date', 'description', 'rating', 'type')

    def creation_year(self, obj):
        if obj.creation_date is None:
            return None

        year = obj.creation_date.year
        return f"{year} г."

    creation_year.empty_value_display = '????'
    creation_year.short_description = _('short_creation_year')

    # Фильтрация в списке
    list_filter = ('type', 'creation_date',)

    # Поиск по полям
    search_fields = ('title', 'description', 'id')
