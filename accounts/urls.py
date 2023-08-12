from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('course_comments/<int:course_id>', views.course_comments, name="course_comments"),

    # Authentication
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),

    # Profile
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('users/<int:user_id>/following/', views.following_list, name='following_list'),
    path('users/<int:user_id>/followers/', views.follower_list, name='follower_list'),

    # Comments
    path('comment_like/<int:pk>', views.comment_like, name='comment_like'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('create_course/', views.create_course, name='create_course'),
    path('update_course/<course_id>/', views.update_course, name='update_course'),
    path('delete_course/<int:pk>/', views.delete_course, name='delete_course'),
    path('courses/subject/<str:subject>/', views.courses_by_subject, name='courses_by_subject'),
    path('courses/category/<int:category_id>/', views.courses_by_category, name='courses_by_category'),
    path('search_courses/', views.search_courses, name='search_courses'),
    path('my_courses/', views.my_courses, name='my_courses'),

    # Study Requests
    path('create_study_request/', views.group_study_request, name='group_study_request'),
    path('all_study_requests/', views.study_request_list, name='study_request_list'),
    # path('study_requests/<int:id>', views.study_request, name='study_request'),
    path('delete_study_request/<int:id>', views.delete_study_request, name='delete_study_request'),
    # path('create_study_request/', views.create_study_request, name='create_study_request'),
    path('update_study_request/<int:id>/', views.update_study_request, name='update_study_request'),
    path('notes_text', views.notes_text, name='notes_text'),

    # Calendar
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('<int:year>/<str:month>/', views.calendar_view, name='calendar_view')
]

    # path('courses/<int:course_id>/add_to_calendar/', add_course_to_calendar, name='add_to_calendar'),

    # path('students/', views.get_students, name='get_students'),


