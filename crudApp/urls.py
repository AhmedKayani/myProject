from django.urls import path
from . import views

urlpatterns = [
  path('signup/', views.signup_view, name='signup'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('home/', views.home_view, name='home'),
  path('home/update/<int:profile_id>/', views.update_home, name='update'),
  path('home/delete/<int:profile_id>/', views.delete_home, name='delete'), 
]