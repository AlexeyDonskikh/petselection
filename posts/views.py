from django.conf import settings
from django.views.generic import DetailView, ListView, CreateView

from posts.forms import CommentForm
from posts.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    extra_context = {
        'comments_form': CommentForm(),
    }


    class PostCreateView(CreateView):

