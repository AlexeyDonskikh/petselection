from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'auth/signUp.html'


def page_not_found(request, exception):
    """
    Handle HTTP 404 Not Found.
    """
    return render(request, 'error/404.html', status=404)


def server_error(request):
    """
    Handle HTTP 500 Server Error.
    """
    return render(request, 'error/500.html', status=500)


def page_bad_request(request, exception):
    """
    Handle HTTP 400 Bad Request.
    """
    return render(request, 'error/400.html', status=400)
