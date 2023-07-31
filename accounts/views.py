from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .google_auth import flow
from oauth2client.client import OAuth2Credentials
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Profile, Comment  
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import CommentForm, UserRegistrationForm


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
    if request.user.is_authenticated:
        form = CommentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.save()
                messages.success(request,("Your comment has been posted successfully!"))
                return redirect('home')
            
        comments = Comment.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"comments": comments, "form": form})
    else:
        comments = []
        return render(request, 'home.html', {"comments": comments})

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
        comments = Comment.objects.filter(user_id=pk).order_by("-created_at")
        # Post form logic
        if request.method == "POST":
            # Get current user ID
            current_user_profile = request.user.profile
            # Get Form Data
            action = request.POST.get('follow')
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save profile
            current_user_profile.save()

        return render(request, "profile.html", {"profile": profile, "comments": comments})
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

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request,("There was an error loggin in. Please try again!"))
            return redirect('login')
    return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out successfully!"))
    return redirect('home')

def register_user(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['second_name']
            # email = form.cleaned_data['email']
            # Log in User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Welcome to SkillFusion! You have successfully registered."))
            return redirect('home')
    return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        return render(request, "update_user.html", {})
    else:
        messages.success(request, ("You must be logged in to update your profile!"))
        return redirect('home')