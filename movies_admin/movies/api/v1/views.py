from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from ...models import FilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        return self.model.objects.values(
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
        ).annotate(
            actors=ArrayAgg('people__full_name', filter=Q(personfilmwork__role__exact='actor'), distinct=True)
        ).annotate(
            directors=ArrayAgg('people__full_name', filter=Q(personfilmwork__role__exact='director'), distinct=True)
        ).annotate(
            writers=ArrayAgg('people__full_name', filter=Q(personfilmwork__role__exact='writer'), distinct=True)
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True)
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        instance = self.get_object(queryset)
        return instance
