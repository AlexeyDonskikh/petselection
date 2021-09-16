from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
from pets.models import Pet


from django.views.generic import (
    ListView,
)


# def index(request):
#     """
#     Display most recent `recipes.Recipe`, fitered with tags, 6 per page.
#     """
#     # tags = request.GET.getlist('tag', Tag)
#
#     # pets = Pet.objects.filter(
#     #     tags__title__in=tags
#     # ).select_related(
#     #     'author'
#     # ).prefetch_related(
#     #     'tags'
#     # ).distinct()
#
#     pets = Pet.objects.select_related('master')
#
#     paginator = Paginator(pets, settings.PAGINATION_PAGE_SIZE)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#
#     return render(
#         request,
#         'pets/index.html',
#         {
#             'page': page,
#             'paginator': paginator,
#         }
#     )


class PetListView(ListView):
    model = Pet
    template_name = 'pets/index.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE
    context_object_name = 'pets'
