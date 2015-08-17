# coding: utf-8
from django.contrib.auth.forms import AuthenticationForm as AuthenticationFormBase


class AuthenticationForm(AuthenticationFormBase):
    def get_user(self):
        raise BaseException(123)
