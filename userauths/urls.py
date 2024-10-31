from django.urls import path
from userauths import views

app_name = 'userauths'

urlpatterns = [
    path('log-in/', views.login_view, name='log-in'),
    path('log-out/', views.logout_view, name='log-out'),
    path('register/', views.register_view, name='register'),
    path('profile/update/', views.profile_update, name='profile-update'),
    path('forget-password/', views.forgot_password, name='forgot_password'),
    path('get-reset-password-email/', views.get_reset_password_email, name='get_reset_password_email'),
    path('reset/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]