from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


# Create your views here.
class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def pwd_validate(self):
        return self.password == self.password2


def sign_up(request):
    error_msg = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.username = data['username']
            form.email = data['email']
            form.password = data['password']
            form.password2 = data['password2']
            if not User.objects.all().filter(username=form.username):
                if form.pwd_validate():
                    user = User.objects.create_user(form.username, password=form.password, email=form.email)
                    user.save()
                    request.session['username'] = form.username
                    request.session['password'] = form.password
                    return HttpResponseRedirect('/songlists/')
                else:
                    error_msg = '两次输入密码不一致'
            else:
                error_msg = '该用户已注册'
        else:
            error_msg = '请完整填写表单'
    return render(request, template_name='create_account/signup.html',
                  context={'error_msg': error_msg})


def log_in(request):
    pass


def log_out(request):
    pass
