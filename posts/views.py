from django.conf import settings
from django.views.generic import DetailView, ListView, CreateView

from posts.forms import CommentForm, PostForm, PostFormset
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

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['post_meta_formset'] = PostFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        post_meta_formset = PostFormset(self.request.POST)
        if form.is_valid() and post_meta_formset.is_valid():
            return self.form_valid(form, post_meta_formset)
        else:
            return self.form_invalid(form, post_meta_formset)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

