from django import forms 
from django.forms import inlineformset_factory
from .models import Comment, Profile, Course, CourseCategory, GroupStudyMeeting
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError

class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                            attrs={
                                "placeholder": "Your comment here...",
                                "class":"form-control",
                            }
                           ),
                           label="",
                           )
    class Meta:
        model = Comment
        exclude = ("user", "likes")

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label ="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': "Email Address"}))
    first_name = forms.CharField(label ="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': "First Name"}))
    last_name = forms.CharField(label ="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': "Last Name"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-_only.</span>' 

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text text-muted small"><li>Your Password can\'t be too similar to other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'



        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted small">Enter the same password for. They must be exactly the same.'

class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    about_me = forms.CharField(widget=forms.Textarea, validators=[MaxLengthValidator(500)])

    class Meta:
        model = Profile
        fields = ('profile_image', 'about_me')

class CourseForm(forms.ModelForm):
    course_image = forms.ImageField(label="Course Image", required=False)
    teacher = forms.ModelChoiceField(queryset=User.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ModelChoiceField(queryset=CourseCategory.objects.all(), 
                                      required=False, 
                                      widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Course
        fields = ['course_image','start_date','title', 'subject', 'teacher', 'description', 'category', 'level_of_difficulty',
                  'duration_in_weeks', 'class_frequency', 'max_students', 'open_enrollment']
        labels = {
            'title': '',
            'start_date': 'Start Date',
            'subject': '',
            'teacher': 'Select a Teacher',
            'description': '',
            'category': '',
            'level_of_difficulty': 'Level of Difficulty',
            'duration_in_weeks': '',
            'class_frequency': '',
            'max_students': '',
            'open_enrollment': 'open enrollment',
        }
        widgets = {
            'course_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'title': forms.TextInput(attrs={'placeholder': '*Enter title of course', 'required': True}),
            'subject': forms.TextInput(attrs={'placeholder': '*Enter course subject', 'required': True}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'placeholder': '*Enter course description', 'required': True}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'level_of_difficulty': forms.Select(choices=Course.LEVEL_CHOICES, attrs={'class': 'form-select'}),
            'duration_in_weeks': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Course length(in weeks)'}),
            'class_frequency': forms.NumberInput(attrs={'min': 0, 'placeholder': '# of meets per week'}),
            'max_students': forms.NumberInput(attrs={'min': 0, 'placeholder': 'max # of students'}),
            'open_enrollment': forms.CheckboxInput(),
        }

class StudyRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StudyRequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GroupStudyMeeting
        fields = ['course', 'meeting_type', 'date', 'start_time', 'end_time', 'location', 
                    'start_time_meridiem', 'end_time_meridiem', 'meeting_link', 'description']
        labels = {
            'course': 'Course',
            'meeting_type': 'Select Meeting Type ',
            'date': "Date: ",
            'start_time': 'Start Time ',
            'end_time': 'End Time',
            'start_time_meridiem': 'AM/PM',
            'end_time_meridiem': 'AM/PM',
            'location': 'Meeting Location',
            'meeting_link': 'Meeting Link',
            'description': 'Meeting Description',

        }
        widgets = {
            'course': forms.Select(), 
            'meeting_type': forms.Select(),
            'date': forms.DateInput(attrs={'placeholder': 'Meeting date (MM/DD)'}),
            'start_time': forms.TimeInput(attrs={'placeholder': 'start time (--:--)'}),
            'end_time': forms.TimeInput(attrs={'placeholder': 'end time(--:--)'}),
            'start_time_meridiem': forms.Select(),
            'end_time_meridiem': forms.Select(),
            'location': forms.TextInput(attrs={'placeholder': 'Enter meeting location'}),
            'meeting_link': forms.URLInput(attrs={'placeholder': 'Enter meeting link'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter meeting description'}),
        }
        required = {
            'meeting_type': False,
            'date': True,
            'start_time': True,
            'end_time': False,
            'location': False,
            'meeting_link': False,
            'description': False,
        }
    
class GroupStudyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupStudyForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(students=user)

        # Explicitly mark certain fields as not required
        self.fields['meeting_type'].required = False
        self.fields['location'].required = False
        self.fields['meeting_link'].required = False
        self.fields['description'].required = False

    class Meta:
        model = GroupStudyMeeting
        fields = ['course', 'meeting_type', 'date', 'start_time', 'end_time', 'location', 
                  'start_time_meridiem', 'end_time_meridiem', 'meeting_link', 'description']
        
        widgets = {
            'meeting_type': forms.Select(),
            'date': forms.DateInput(attrs={'placeholder': '*date (YYYY-MM-DD)'}),
            'start_time': forms.TimeInput(attrs={'placeholder': '*start time (--:--)'}),
            'end_time': forms.TimeInput(attrs={'placeholder': '*end time (--:--)'}),
            'start_time_meridiem': forms.Select(),
            'end_time_meridiem': forms.Select(),
            'location': forms.TextInput(attrs={'placeholder': 'meeting location'}),
            'meeting_link': forms.URLInput(attrs={'placeholder': 'Enter meeting link'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter meeting description'}),
        }
        labels = {
            'course': '*Select Course',
            'meeting_type': 'Select Meeting Type ',
            'date': "Date: ",
            'start_time': 'Start Time ',
            'end_time': 'End Time',
            'start_time_meridiem': '*AM/PM',
            'end_time_meridiem': '*AM/PM',
            'location': 'Meeting Location',
            'meeting_link': 'Meeting Link',
            'description': 'Meeting Description',
        }




