# coding: utf-8
from class_based_auth_views.views import LoginView as LoginViewBase


class LoginView(LoginViewBase):
    template_name = 'acc/login.html'
