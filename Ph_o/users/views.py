from django.shortcuts import render
from django.shortcuts import render, redirect
from photos import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model, authenticate, login, logout
from core.management.commands.my_email import send_email
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse
from users.forms import CustomAuthForm
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from datetime import datetime

class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/login.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if not username:
            context = {'error': 'Введите юзернейм'}
        if not password:
            context = {'error': 'Введите пароль'}

        user = authenticate(username=username, password=password)
        context = {'error': user}
        if user is None and username and password:
            try:
                user = models.RunUser.objects.get(email=email)

                context = {'error': 'Неправильный пароль'}
                # context = {'error': password}
                return render(request, 'registration/login.html', context)

            except:
                context = {'error': 'Пользователь с таким юзернеймом не найден'}
                return render(request, 'registration/login.html', context)
        if user:
            user.last_login = datetime.now()
            user.save()
            login(request, user)

            return redirect('home')
        context = {'error': 'Пользователь с таким юзернеймом не найден'}
        return render(request, 'registration/login.html', context)


class CreateUser(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/create_user.html', {})

    def post(self, request, *args, **kwargs):

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if str(password1) != str(password2):
            context = {'error': 'Пароли не совпадают'}
            return render(request, 'registration/create_user.html', context)
        else:
            create_new_user = models.RunUser.objects.create_user(username, email, password1)
            user = authenticate(username=username, password=password1)
            login(request, user)
            return redirect('login')

class PasswordRecovery(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/password_recovery.html', {})

    def post(self, request, *args, **kwargs):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = models.RunUser.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    html = render_to_string(email_template_name, c)
                    # try:
                    msg = send_email(data={
                        'subject': 'Изменение пароля',
                        'text': 'Добрый день, Ваш новый пароль: ',
                        'email': user.email,
                        'html': html
                    })
                        # send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    # except:
                    #     return HttpResponse('Invalid header found.')
                    return redirect("password_reset_complete")

        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="registration/password_reset.html",
                      context={"password_reset_form": password_reset_form})


class ChangePassword(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        return redirect('login')


class LoginRedirect(TemplateView):

    def get(self, request, *args, **kwargs):
        return userRedirect(request.user)
