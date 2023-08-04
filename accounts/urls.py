from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('users/<int:user_id>/following/', views.following_list, name='following_list'),
    path('users/<int:user_id>/followers/', views.follower_list, name='follower_list'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('create_course/', views.create_course, name='create_course'),
    # path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    # path('courses/subject/<str:subject>/', views.courses_by_subject, name='courses_by_subject'),

]
    # path('courses/<int:course_id>/add_to_calendar/', add_course_to_calendar, name='add_to_calendar'),

    # path('students/', views.get_students, name='get_students'),


