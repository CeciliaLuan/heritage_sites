from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),  # This is the homepage view
    path('heritage_sites/', views.map_view, name='heritage_sites'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update_location/', views.update_location, name='update_location'),
    path('signup/', views.signup_view, name='signup'),
]
