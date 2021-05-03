from django.urls import path, include, reverse_lazy
from django_registration.backends.one_step.views import RegistrationView
from accounts.forms import RegisterForm
from accounts.views import ProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegistrationView.as_view(form_class=RegisterForm, success_url=reverse_lazy('index')), name="django_registration_register"),
    path('', include('django_registration.backends.one_step.urls')),
    path('', include('django.contrib.auth.urls')),
]
