from django import forms 
# from django.forms import inlineformset_factory
from .models import Comment, Profile, Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        exclude = ("user",)

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

    class Meta:
        model = Profile
        fields = ('profile_image', )

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'subject', 'description', 'level_of_difficulty', 'duration_in_weeks', 'class_frequency', 'teacher']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title of course'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Enter course subject'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter course description'}),
            'level_of_difficulty': forms.Select(attrs={'placeholder': 'Select difficulty level'}),
            'duration_in_weeks': forms.NumberInput(attrs={'placeholder': 'Enter course length in weeks'}),
            'class_frequency': forms.NumberInput(attrs={'placeholder': 'Enter how often the class will meet in a week'}),
            'teacher': forms.Select(attrs={'placeholder': 'Select a teacher'}),
        }


# class ClassMeetingForm(forms.ModelForm):
#     class Meta:
#         model = ClassMeetings
#         fields = ['meeting_type', 'date', 'start_time', 'end_time', 'location', 'meeting_link', 'description']
#         widgets = {
#             'meeting_type': forms.Select(attrs={'placeholder': 'Select meeting type'}),
#             'date': forms.DateInput(attrs={'placeholder': 'Select date'}),
#             'start_time': forms.TimeInput(attrs={'placeholder': 'Select start time'}),
#             'end_time': forms.TimeInput(attrs={'placeholder': 'Select end time'}),
#             'location': forms.TextInput(attrs={'placeholder': 'Enter location'}),
#             'meeting_link': forms.URLInput(attrs={'placeholder': 'Enter meeting link'}),
#             'description': forms.Textarea(attrs={'placeholder': 'Enter meeting description'}),
#         }



# ClassMeetingFormSet = inlineformset_factory(Course, ClassMeetings, form=ClassMeetingForm, extra=1)
