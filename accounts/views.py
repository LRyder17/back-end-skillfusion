from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student  # Import the Student model instead of User

@csrf_exempt
def create_student(request):  # Rename the view function to create_student
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = data.get('age')  # Rename the 'date_of_birth' field to 'age'
        grade = data.get('grade')  # Add 'grade' field

        if first_name and last_name and age and grade:
            student = Student.objects.create(  # Use Student instead of User
                first_name=first_name,
                last_name=last_name,
                age=age,  # Update the field name
                grade=grade  # Add the 'grade' field
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