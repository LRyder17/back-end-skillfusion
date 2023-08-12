from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('comment_like/<int:pk>', views.comment_like, name='comment_like'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('users/<int:user_id>/following/', views.following_list, name='following_list'),
    path('users/<int:user_id>/followers/', views.follower_list, name='follower_list'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('create_course/', views.create_course, name='create_course'),
    path('study_request/', views.group_study_request, name='group_study_request'),
    path('create_study_request/', views.create_study_request, name='create_study_request'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/comments', views.course_comments, name='course_comments'),
    path('courses/subject/<str:subject>/', views.courses_by_subject, name='courses_by_subject'),
    path('courses/category/<int:category_id>/', views.courses_by_category, name='courses_by_category'),
    path('update_course/<course_id>/', views.update_course, name='update_course'),
    path('delete_course/<int:pk>/', views.delete_course, name='delete_course'),
    path('search_courses/', views.search_courses, name='search_courses'),
    path('my_courses/', views.my_courses, name='my_courses'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('<int:year>/<str:month>/', views.calendar_view, name='calendar_view')
]
    # path('courses/<int:course_id>/add_to_calendar/', add_course_to_calendar, name='add_to_calendar'),

    # path('students/', views.get_students, name='get_students'),


