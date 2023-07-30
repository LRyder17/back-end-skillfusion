from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .google_auth import flow
from oauth2client.client import OAuth2Credentials
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Profile  
from django.contrib.auth.models import User


@csrf_exempt
def create_student(request):  
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = data.get('age')  
        grade = data.get('grade')  

        if first_name and last_name and age and grade:
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,  
                grade=grade  
            )

            return JsonResponse({'message': 'Student created successfully!'})
        else:
            return JsonResponse({'message': 'All fields are required!'}, status=400)

    return JsonResponse({'message': 'Invalid request method!'}, status=405)

def get_students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        student_list = [{'first_name': student.first_name, 'last_name': student.last_name,
                         'age': student.age, 'grade': student.grade} for student in students]
        return JsonResponse(student_list, safe=False)

    return JsonResponse({'message': 'Invalid request method!'}, status=405)

def home(request):
    return render(request, 'home.html', {})

def following_list(request, user_id):
    user = User.objects.get(id=user_id)
    profiles = user.profile.follows.all()
    return render(request, 'profile_list.html', {'profiles': profiles})

def follower_list(request, user_id):
    user = User.objects.get(id=user_id)
    profiles = user.profile.followed_by.all()
    return render(request, 'profile_list.html', {'profiles': profiles})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        return render(request, "profile.html", {"profile": profile})
    else:
        messages.success(request,("You must be logged in to view this page"))
        return redirect('home')
 

def oauth2callback(request):
    auth_code = request.GET.get('code')
    credentials = flow.step2_exchange(auth_code)
    request.user.profile.access_token = credentials.access_token
    request.user.profile.refresh_token = credentials.refresh_token
    request.user.profile.save()
    return HttpResponseRedirect('/')