from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from users.forms import CreationForm
from users.models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'auth/signUp.html'


class ProfileView(DetailView):
    model = User
    template_name = 'users/profile_view.html'
    context_object_name = 'user'
