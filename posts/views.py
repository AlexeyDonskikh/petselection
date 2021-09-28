from django.conf import settings
from django.views.generic import CreateView, DetailView, ListView

from posts.forms import CommentForm, PostForm
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
    model = Post
    form_class = PostForm
    template_name = 'posts/post_add.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)
