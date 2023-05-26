from django.urls import path
from users import views as userViews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from .forms import *

urlpatterns = [
    path('reg/', userViews.CreateUser.as_view(template_name='users/registration.html'), name='reg'),
    path('login/', views.LoginView.as_view(
        template_name='users/login.html',
        redirect_field_name='home'
    ),
        name='login'
    ),
    path('profile/<int:pk>/', userViews.ProfileDetailView.as_view(), name='profile'),
    path('exit/', views.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('upprofile/<int:user_id>/', userViews.update_profile, name='update_profile'),
    path('pass-reset/', userViews.password_reset_request, name='pass-reset'),
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
         ),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path('password_reset_done/', views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path("", userViews.BaseView.as_view(), name="home"),
    # path('team-create/', userViews.search_results_users, name='search'),
    path('team-create/', userViews.add_team, name='team-create'),
    path('team/<int:pk>', userViews.TeamDetailView.as_view(), name='team'),
    path('profile/<int:pk>/user-teams', userViews.UserTeamView.as_view(), name='user-teams'),
    path('update-team/<int:team_id>', userViews.update_team, name='update-team'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
