from django.contrib.auth.views import LoginView
from django.contrib import admin

class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'  # Use the default admin login template