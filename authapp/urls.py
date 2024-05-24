from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile_view, name='user_profile'),
    path('profile/update/<int:profile_id>/', views.update_profile, name='update_profile'),
    path('profile/delete/<int:profile_id>/', views.delete_profile, name='delete_profile'),
]
