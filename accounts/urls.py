from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('skillfusion-db.onrender.com/profile_list/', views.profile_list, name="profile_list"),
    path('users/<int:user_id>/following/', views.following_list, name='following_list'),
    path('users/<int:user_id>/followers/', views.follower_list, name='follower_list'),
    # path('create_student/', views.create_student, name='create_student'),
    # path('students/', views.get_students, name='get_students'),
]

