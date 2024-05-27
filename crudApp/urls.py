from django.urls import path
from .views import signup_view, login_view, logout_view, home_view, update_home, delete_home, notifications_view

urlpatterns = [
  path('signup/', signup_view, name='signup'),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
  path('home/', home_view, name='home'),
  path('home/update/<int:profile_id>/', update_home, name='update'),
  path('home/delete/<int:profile_id>/', delete_home, name='delete'),
  path('home/notifications/', notifications_view, name='notifications'),
]