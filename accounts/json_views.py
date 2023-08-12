

def home_view(request):
    response_data = {}

    if request.user.is_authenticated:
        form = CommentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                response_data['message'] = "Your comment has been posted successfully!"
                response_data['status'] = 'success'
                status = 201

        comments = Comment.objects.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        response_data['comments'] = serializer.data
    else:
        response_data['comments'] = []
        response_data['status'] = 'unauthenticated'
        status = 401

    return JsonResponse(response_data, status=status)

def following_list_view(request, user_id):
    response_data = {}
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        profiles = user.profile.follows.exclude(user=user)
        serializer = ProfileSerializer(profiles, many=True)
        response_data['profiles'] = serializer.data
        response_data['status'] = 'success'
        status = 201
    else:
        response_data['message'] = "You must be logged in to view this page"
        response_data['status'] = 'unauthenticated'
        status = 401

    return JsonResponse(response_data, status=status)

def follower_list_view(request, user_id):
    response_data = {}
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        profiles = user.profile.followed_by.exclude(user=user)
        serializer = ProfileSerializer(profiles, many=True)
        response_data['profiles'] = serializer.data
        response_data['status'] = 'success'
        status = 201
    else:
        response_data['message'] = "You must be logged in to view this page"
        response_data['status'] = 'unauthenticated'
        status = 401

    return JsonResponse(response_data, status=status)

def comment_like_view(request, pk):
    response_data = {}
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        if comment.likes.filter(id=request.user.id):
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        response_data['message'] = "Action performed successfully!"
        response_data['status'] = 'success'
        status = 201
    else:
        response_data['message'] = "Please log in to continue."
        response_data['status'] = 'unauthenticated'
        status = 401
    return JsonResponse(response_data, status=status)

def comment_show_view(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    response_data ={}
    if comment:
        serializer = CommentSerializer(comment)
        response_data['comment'] = serializer.data
        response_data['status'] = 'success'
        status = 201
    else:
        response_data['message'] = "That Comment Does Not Exist!"
        response_data['status'] = 'error'
        status = 404
    
    return JsonResponse(response_data, status=status)


def delete_comment_view(request, pk):
    response_data = {}
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        if request.user.username == comment.user.username:
            comment.delete()
            response_data['message'] = "Comment deleted successfully!"
            response_data['status'] = 'success'
        elif request.user.username != comment.user.username:
            response_data['message'] = "That Comment Does Not Belong to You"
            response_data['status'] = 'error'
            status = 401
        else:
            response_data['message'] = "That Comment Does Not Exist"
            response_data['status'] = 'error'
            status = 404
    else:
        response_data['message'] = "Please log in to continue."
        response_data['status'] = 'unauthenticated'
        status = 401

    return JsonResponse(response_data, status=status)

def profile_view(request, pk):
    response_data = {}

    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        comments = Comment.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST.get('follow')
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
            response_data['message'] = "Action performed successfully!"

        profile_serializer = ProfileSerializer(profile)
        comments_serializer = CommentSerializer(comments, many=True)
        response_data['profile'] = profile_serializer.data
        response_data['comments'] = comments_serializer.data
        response_data['status'] = 'success'
        status = 201
    else:
        response_data['message'] = "You must be logged in to view this page"
        response_data['status'] = 'unauthenticated'
        status = 401

    return JsonResponse(response_data, status=status)

def create_course_view(request):
    response_data = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            course_form = CourseForm(request.POST, request.FILES)
            if course_form.is_valid():
                user = request.user
                course = course_form.save(commit=False)
                course.creator = request.user
                course.teacher = course_form.cleaned_data['teacher']
                course.save()
                course.students.add(user)
                if course.teacher:
                    course.students.set(user)
                    profile = course.teacher.profile 
                    profile.is_teacher = True
                    profile.save()

                response_data['message'] = "Course created successfully!"
                response_data['course'] = CourseSerializer(course).data
                response_data['status'] = 'success'
                status = 201
            else:
                response_data['message'] = "Form is not valid"
                response_data['status'] = 'error'
                status = 400
        else:
            response_data['message'] = "Method not allowed"
            response_data['status'] = 'error'
            status = 403
    else:
        response_data['message'] = "You must be logged in to add a course!"
        response_data['status'] = 'unauthenticated'
        status = 401

    return JsonResponse(response_data, status=status)

def group_study_request_view(request):
    response_data = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = GroupStudyForm(user=request.user)  # default form for GET request
            if form.is_valid():
                group_study_meeting = form.save()
                response_data['message'] = "You successfully created a group study meeting!"
                response_data['status'] = 'success'
                response_data['group_study_meeting'] = GroupStudyMeetingSerializer(group_study_meeting).data
                status = 201
            else:
                response_data['message'] = 'Invalid form data'
                response_data['status'] = 'error'
                status = 400
        else:
            response_data['message'] = "Method not allowed"
            response_data['status'] = 'error'
            status = 405
    else:
        response_data['message'] = "You must be logged in to request a group study!"
        response_data['status'] = 'unauthenticated'
        status = 401

    return JsonResponse(response_data, status=status)

def course_detail_view(request, pk):
    response_data = {}
    course = get_object_or_404(Course, pk=pk)

    if request.user.is_authenticated:
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
            response_data['message'] = "Action performed successfully!"
            response_data['status'] = 'success'
            status = 201
        else:
            response_data['message'] = "Method not allowed"
            response_data['status'] = 'error'
            status = 400

        response_data['course'] = CourseSerializer(course).data
    else:
        response_data['message'] = "You must be logged in to view this page"
        response_data['status'] = 'unauthenticated'
        status = 401

    return JsonResponse(response_data, status=status)

def courses_by_subject_view(request, subject):
    response_data = {}
    course_list = Course.objects.filter(subject=subject)

    if course_list.exists():
        serializer = CourseSerializer(course_list, many=True)
        response_data['courses'] = serializer.data
        response_data['status'] = 'success'
        status = 201
    else:
        response_data['message'] = f"No courses found for subject: {subject}"
        response_data['status'] = 'not_found'
        status = 404

    return JsonResponse(response_data, status=status)

def course_list_view(request):
    response_data = {}
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)

    response_data['courses'] = serializer.data
    response_data['status'] = 'success'
    status = 201

    return JsonResponse(response_data, status=status)

def courses_by_category_view(request, category_id):
    response_data = {}
    course_list = Course.objects.filter(category_id=category_id)

    if course_list.exists():
        serializer = CourseSerializer(course_list, many=True)
        response_data['courses'] = serializer.data
        response_data['status'] = 'success'
        status = 201
    else:
        response_data['message'] = f"No courses found for category ID: {category_id}"
        response_data['status'] = 'not_found'
        status = 404

    return JsonResponse(response_data, status=status)

def search_courses_view(request):
    response_data = {}
    if request.method == "POST":
        searched = request.POST['searched']
        courses = Course.obbjects.filter(title__contains=searched)
        response_data['searched'] = searched
        response_data['courses'] = CourseSerializer(courses, many=True).data
        response_data['status'] = 'success'
        status = 201
    else:
        response_data['message'] = 'Method not allowed'
        response_data['status'] = 'error'
        status = 403

    return JsonResponse(response_data, status=status)