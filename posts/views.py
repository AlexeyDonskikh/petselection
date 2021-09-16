from django.conf import settings
from posts.models import Post


from django.views.generic import (
    ListView,
)


class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE
    context_object_name = 'posts'
