from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews_view, name='reviews_view'),
    path('rate/', views.rate_view, name='rate_view'),
    path('submit_rating/', views.submit_rating, name='submit_rating'),
    path('search/', views.search_professors, name='search_professors'),
    path('ratings/', views.get_professor_ratings, name='get_professor_ratings'),
    path('all/', views.get_all_professors, name='get_all_professors'),
    path('login/', views.login_view, name='login_view'),
]


