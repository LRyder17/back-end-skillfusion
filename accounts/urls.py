from django.urls import path
from . import views

urlpatterns = [
    path('create_student/', views.create_student, name='create_student'),
    path('students/', views.get_students, name='get_students'),
]
