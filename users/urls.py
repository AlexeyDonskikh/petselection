from django.contrib.auth import views as auth_views
from django.urls import path, include

from users import views

auth_urls = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='auth/authForm.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='auth/logout.html'),
        name='logout'
    ),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='auth/changePassword.html'
        ),
        name='password_change'
    ),
    path(
        'password-change-done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='auth/changePasswordDone.html'
        ),
        name='password_change_done'
    ),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/resetPassword.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset-done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='auth/resetPasswordDone.html'
        ),
        name='password_reset_done'
    ),
    path(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='auth/resetPasswordConfirm.html'
        ),
        name='password_reset_confirm'
    ),
]


urlpatterns = [
    path('auth/', include(auth_urls)),
    path('<slug:slug>/', views.ProfileView.as_view(), name='profile_view'),
]
