from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.forms import CustomAuthForm
from users import views
from django.contrib.auth.views import LoginView as login_views, LogoutView as logout_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('login/', login_views.as_view(template_name='registration/login.html', authentication_form=CustomAuthForm), name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', logout_views.as_view(next_page='home'), name='logout'),
    path('password_recovery/', views.PasswordRecovery.as_view(), name='password_recovery'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('login-redirect/', views.LoginRedirect.as_view(), name='login-redirect'),
    path('create-user/', views.CreateUser.as_view(), name='create-user'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]

