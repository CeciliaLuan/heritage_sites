from django.urls import path
from . import views
from .views import HeritageSiteListView, FavouriteListView, FavouriteDetailView

urlpatterns = [
    path('', views.login_view, name='home'),
    path('heritage_sites/', views.map_view, name='heritage_sites'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('favourites/', views.favourites_view, name='favourites'),
    path('favourites/api/add/', views.add_to_favourites, name='add_to_favourites'),
    path('favourites/api/remove/', views.remove_favourite, name='remove_favourite'),

    # API routes
    path('api/sites/', HeritageSiteListView.as_view(), name='api_sites'),
    path('api/favourites/', FavouriteListView.as_view(), name='api_favourites'),
    path('api/favourites/<int:pk>/', FavouriteDetailView.as_view(), name='api_favourite_detail'),
]
