from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def pwd_validate(self):
        return self.password == self.password2


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Create your views here.
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
                    user = authenticate(username=form.username, password=form.password)
                    login(request, user)
                    return HttpResponseRedirect('/songlists/index')
                else:
                    error_msg = '两次输入密码不一致'
            else:
                error_msg = '您已经注册'
        else:
            error_msg = '请完整填写表单'
    return render(request, template_name='create_account/signup.html', context={'error_msg': error_msg})


def sign_in(request):
    error_msg = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print('valid')
            data = form.cleaned_data
            form.username = data['username']
            form.password = data['password']
            user = authenticate(username=form.username, password=form.password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/songlists/index')
            else:
                error_msg = '用户名或密码错误'
    return render(request, template_name='create_account/signin.html', context={'error_msg': error_msg})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/songlists/index')
