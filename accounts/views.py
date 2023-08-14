from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .google_auth import flow
from oauth2client.client import OAuth2Credentials
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Comment, Course, Enrollment, GroupStudyMeeting, StudyRequestAcceptance   
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import CommentForm, UserRegistrationForm, ProfilePicForm, CourseForm, GroupStudyForm
from django.contrib.auth.models import User
from django.utils import timezone
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.core.files.base import ContentFile
import boto3
from io import BytesIO

# def upload_to_s3(file):
#     s3 = boto3.client('s3')
#     if file.multiple_chunks():
#         content = b''.join(chunk for chunk in file.chunks())
#     else:
#         content = file.read()
#     file_to_upload = ContentFile(content)
#     s3.upload_fileobj(file_to_upload, 'skillfusion', 'images/')


# if errors occur try changing 'skillfusion' to 'skillfusion-bucket'
def upload_to_s3(file):
    s3 = boto3.client('s3')
    if file.multiple_chunks():
        content = b''.join(chunk for chunk in file.chunks())
    else:
        content = file.read()

    file_to_upload = BytesIO(content)
    s3.upload_fileobj(file_to_upload, 'skillfusion', 'images/' + file.name)

def home(request):
    if request.user.is_authenticated:
        form = CommentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.save()
                messages.success(request,("Your comment has been posted successfully!"))
                return redirect(request.META.get("HTTP_REFERER"))
            
        comments = Comment.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"comments": comments, 
                                             "form": form})
    else:
        comments = []
        return render(request, 'home.html', {"comments": comments})

    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        comments = Comment.objects.filter(user_id=pk).order_by("-created_at")
        enrolled_courses = profile.user.enrolled_courses.all()

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

        return render(request, "profile.html", {"profile": profile, 
                                                "comments": comments,
                                                "enrolled_courses": enrolled_courses})
    else:
        messages.success(request,("You must be logged in to view this page"))
        return redirect(request.META.get("HTTP_REFERER"))

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect(request.META.get("HTTP_REFERER"))

def following_list(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        profiles = user.profile.follows.exclude(user=user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect(request.META.get("HTTP_REFERER"))

def follower_list(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        profiles = user.profile.followed_by.exclude(user=user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect(request.META.get("HTTP_REFERER"))

def comment_like(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        if comment.likes.filter(id=request.user.id):
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
    
        return redirect(request.META.get("HTTP_REFERER"))
    
def course_like(request, pk):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, id=pk)
        if course.likes.filter(id=request.user.id).exists():
            course.likes.remove(request.user)
        else:
            course.likes.add(request.user)
    
        return redirect(request.META.get("HTTP_REFERER"))

def course_favorite(request, pk):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, id=pk)
        if course.favorites.filter(id=request.user.id).exists():
            course.favorites.remove(request.user)
        else:
            course.favorites.add(request.user)
    
        return redirect(request.META.get("HTTP_REFERER"))

def comment_show(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment:
        return render(request, 'show_comment.html', {'comment': comment})
    else:
        messages.success(request, ("That Comment Does Not Exist!"))
        return redirect('home')
    
def delete_comment(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        if request.user.username == comment.user.username:
            comment.delete()
            return redirect(request.META.get("HTTP_REFERER"))
        elif request.user.username != comment.user.username:
            messages.success(request, ("That Comment Does Not Belong to You"))
            return redirect('home')
        else:
            messages.success(request, ("That Comment Does Not Exist"))
            return redirect('home')
    else:
        messages.success(request, ("Please log in to continue."))
        return redirect(request.META.get('login'))

def course_comments(request, pk):  
    course = get_object_or_404(Course, id=pk)  
    if request.user.is_authenticated:
        form = CommentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.course = course  
                comment.save()
                messages.success(request, "Your comment has been posted successfully!")
                return redirect(request.META.get("HTTP_REFERER"))

        comments = Comment.objects.filter(course=course).order_by("-created_at")  
        return render(request, 'course_comments.html', {"course": course, 
                                                        "comments": comments, 
                                                        "form": form})
    else:
        comments = []
        return render(request, 'course_comments.html', {"course": course,
                                                        "comments": comments})

def create_course(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            course_form = CourseForm(request.POST, request.FILES, user=request.user)
            if course_form.is_valid():
                course = course_form.save(commit=False) 
                course.creator = request.user
                course.teacher = course_form.cleaned_data['teacher']
                course.save()
                course.students.add(request.user)
                if course.teacher:
                    course.students.add(course.teacher)
                    profile = course.teacher.profile 
                    profile.is_teacher = True
                    profile.save()

                messages.success(request, ("Course created successfully!"))
                Enrollment.objects.create(course=course, student=request.user)
                return redirect('course_list')
        else:
            course_form = CourseForm(user=request.user) 

        return render(request, 'create_course.html', {'course_form': course_form})
    else:
        messages.success(request, ("You must be logged in to add a course!"))
        return redirect('login')

# def course_detail(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     enrolled_students_count = course.enrolled_courses.count()

#     # can_enroll = False
#     if request.user.is_authenticated:
#         # Enrollment logic
#         if request.method == "POST":
#             action = request.POST.get('enrollment')
#             if action == "unenroll":
#                 Enrollment.objects.filter(course=course, student=request.user).delete()
#                 course.students.remove(request.user)
#             elif action == "enroll":
#                 Enrollment.objects.create(course=course, 
#                                           student=request.user, 
#                                           enrolled_time=timezone.now())
#                 course.students.add(request.user)
#             course.save()

#         return render(request, "course_detail.html", {"course": course, 
#                                                       "enrolled_students_count": enrolled_students_count})
#     else:
#         return render(request, "course_detail.html", {"course": course})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrolled_students_count = course.enrolled_courses.count()

    context = {
        "course": course,
        "enrolled_students_count": enrolled_students_count
    }

    return render(request, "course_detail.html", context)

    
def course_enrollment(request, pk):
    if not request.user.is_authenticated:
        return redirect('name_of_login_page')

    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        action = request.POST.get('enrollment')

        if action == "unenroll":
            Enrollment.objects.filter(course=course, student=request.user).delete()
            course.students.remove(request.user)
        elif action == "enroll":
            Enrollment.objects.create(course=course, 
                                      student=request.user, 
                                      enrolled_time=timezone.now())
            course.students.add(request.user)

        course.save()

    return redirect('course_detail', pk=pk)

# def course_list(request):
#     course_list = Course.objects.all()
#     return render(request, 'course_list.html', {'course_list': course_list})

def search_courses(request):
    if request.method == "POST":
        searched = request.POST['searched']
        return redirect('course_list_searched', searched=searched)
    else:
        return render(request, 'search_courses.html', {})

def course_list(request, searched=None):
    if searched:
        course_list = Course.objects.filter(
            Q(title__icontains=searched) | 
            Q(category__title__icontains=searched) | 
            Q(subject__icontains=searched) |
            Q(teacher__username__icontains=searched) |
            Q(level_of_difficulty__icontains=searched)
    )
    else:
        course_list = Course.objects.all()
    return render(request, 'course_list.html', {'course_list': course_list, 'searched': searched})

def courses_by_subject(request, subject):
    course_list = Course.objects.filter(subject=subject)
    return render(request, 'course_list.html', {'course_list': course_list})

def courses_by_category(request, category_id):
    course_list = Course.objects.filter(category_id=category_id)
    return render(request, 'course_list.html', {'course_list': course_list})

def my_courses(request):
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(student=request.user)
        course_list = [enrollment.course for enrollment in enrollments]
        return render(request, 'my_courses.html', {'course_list': course_list})
    else:
        messages.success(request,("You must be logged in to view your courses!"))
        return redirect('login')

def update_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        return redirect('course_list')
    return render(request, 'update_course.html', {'course': course, 'form': form})

# def search_courses(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         courses = Course.objects.filter(title__contains=searched)
#         return render(request, 'search_courses.html', {'searched': searched,
#                                                        'courses': courses})
#     else:
#         return render(request, 'search_courses.html', {})


def delete_course(request, pk):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=pk)

        if request.user != course.creator:
            messages.error(request, "You don't have permission to delete this course.")
            return redirect('course_detail', pk=course.id)
        
        if request.method == "POST":
            course.delete()
            messages.success(request, "Your course has been successfully deleted!")
            return redirect('course_list')
        
        return render(request, 'confirm_delete_course.html', {'course': course})
    else:
        messages.error(request, ("You must be logged in to delete a course!"))
        return redirect('login')

def group_study_request(request):
    if request.user.is_authenticated:
        form = GroupStudyForm(user=request.user)  
        if request.method == 'POST':
            form = GroupStudyForm(request.POST, user=request.user)
            if form.is_valid():
                study_request = form.save(commit=False)  
                study_request.created_by = request.user  
                study_request.save() 
                messages.success(request, "You successfully created a group study meeting!")
                return redirect('course_list')
        
        return render(request, 'group_study_meeting.html', {'form': form})
    else:
        messages.error(request, ("You must be logged in to request a group study!"))
        return redirect('login')


def my_study_requests(request):
    if request.user.is_authenticated:
        enrolled_courses = Course.objects.filter(enrolled_courses__student=request.user)

        study_requests = GroupStudyMeeting.objects.filter(course__in=enrolled_courses)

        accepted_study_request_ids = StudyRequestAcceptance.objects.filter(user=request.user, 
                                                                           study_request__in=study_requests,
                                                                           accepted=True).values_list('study_request__id', flat=True)

        if request.method == "POST":
            action = request.POST.get('acceptance')
            study_request_id = request.POST.get("study_request_id")
            study_request = get_object_or_404(GroupStudyMeeting, id=study_request_id)

            if action == "cancel":
                StudyRequestAcceptance.objects.filter(study_request=study_request, 
                                                      user=request.user).delete()
            elif action == "accept":
                StudyRequestAcceptance.objects.create(study_request=study_request,
                                                      user=request.user, accepted=True)

        return render(request, 'my_study_requests.html', {
            'study_requests': study_requests,
            'accepted_study_request_ids': accepted_study_request_ids,
            })
    else:
        messages.success(request,("You must be logged in to view study requests!"))
        return redirect('login')
    
def update_study_request(request, request_id):
    if request.user.is_authenticated:
        study_request = get_object_or_404(GroupStudyMeeting, id=request_id)
        form = GroupStudyForm(user=request.user)  # default form for GET request
        if request.method == 'POST':
            form = GroupStudyForm(request.POST, instance=study_request, user=request.user)
            if form.is_valid():
                form.save()
                messages.success (request,
                            ("You successfully update the group study meeting request!"))
                return redirect('course_list')
        else:
            form = GroupStudyForm(instance=study_request, user=request.user)
        
        context = {
            'study_request': study_request,
            'form': form,
            'previous_page': request.META.get('HTTP_REFERER', None)     
        }
        return render(request, 'update_study_request.html', context)
    
    else:
        messages.error(request, ("You must be logged in to update a group study request!"))
        return redirect('login')

def delete_study_request(request, request_id):
    if request.user.is_authenticated:
        study_request = get_object_or_404(GroupStudyMeeting, id=request_id)
        if request.user == study_request.created_by:
            study_request.delete()
            messages.success(request, "You successfully deleted the study request.")
            return redirect('my_study_requests')
        else:
            if request.user != study_request.created_by:
                messages.success(request, "You do not have permission to delete this item")
            else:
                messages.success(request, "That Item Does Not Exist")
            return redirect('home')
    else:
        messages.success(request, ("Please log in to continue."))
        return redirect(request.META.get('login'))


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
        user = authenticate(request, username=username, 
                                     password=password)
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
            # last_name = form.cleaned_data['last_name']
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
        user_form = UserRegistrationForm(request.POST or None, 
                                         request.FILES or None, 
                                         instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, 
                                      request.FILES or None, 
                                      instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Refreshes the user's session to prevent them being logged out 
            update_session_auth_hash(request, current_user)

            messages.success(request, ("Your profile information has been updated"))
            return redirect(reverse('profile', kwargs={'pk': request.user.profile.pk}))

        return render(request, "update_user.html", {'user_form': user_form, 
                                                    'profile_form': profile_form})
    else:
        messages.success(request, ("You must be logged in to update your profile!"))
        return redirect('home')

def calendar_view(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )
    now = datetime.now()
    current_year = now.year
    return render(request, 'calendar_view.html', 
                  {'year': now.year,
                   'month': month,
                   'cal': cal,
                  })
    
