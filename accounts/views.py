from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .google_auth import flow
from oauth2client.client import OAuth2Credentials
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Comment, Course, Enrollment   
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import CommentForm, UserRegistrationForm, ProfilePicForm, CourseForm
from django.contrib.auth.models import User
from django.utils import timezone



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
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        profiles = user.profile.follows.exclude(user=user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def follower_list(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        profiles = user.profile.followed_by.exclude(user=user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

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
    
def create_course(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            course_form = CourseForm(request.POST) # Get the data from the POST request
            if course_form.is_valid():
                course = course_form.save() # Save the form data to the database
                course.creator = request.user
                messages.success(request, ("Course created successfully!"))
                Enrollment.objects.create(course=course, student=request.user)
                return redirect('home') # Redirect to home or another success page
        else:
            course_form = CourseForm() 

        return render(request, 'create_course.html', {'course_form': course_form} )
    else:
        messages.success(request, ("You must be logged in to add a course!"))
        return redirect('home')

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    can_enroll = False
    if request.user.is_authenticated:
        # Enrollment logic
        if request.method == "POST":
            action = request.POST.get('enrollment')
            if action == "unenroll":
                # Unenroll the user from the course
                Enrollment.objects.filter(course=course, student=request.user).delete()
                course.students.remove(request.user)
            elif action == "enroll":
                # Enroll the user in the course
                Enrollment.objects.create(course=course, student=request.user, enrolled_time=timezone.now())
                course.students.add(request.user)
            course.save()

        return render(request, "course_detail.html", {"course": course})
    else:
        return render(request, "course_detail.html", {"course": course})
    
def course_list(request):
    course_list = Course.objects.all()
    return render(request, 'course_list.html', {'course_list': course_list})


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
            return redirect(reverse('profile', kwargs={'pk': user.profile.pk}))
    return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        # Get forms
        user_form = UserRegistrationForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Refreshes the user's session to prevent them being logged out 
            update_session_auth_hash(request, current_user)

            messages.success(request, ("Your profile information has been updated"))
            return redirect(reverse('profile', kwargs={'pk': request.user.profile.pk}))

        return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, ("You must be logged in to update your profile!"))
        return redirect('home')
    
