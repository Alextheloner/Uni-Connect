from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from forum.models import School, Department


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('lecturer', 'Lecturer')])
    school = forms.ModelChoiceField(
        queryset=School.objects.filter(is_active=True),
        required=True,
        empty_label='Select your school...',
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        required=True,
        empty_label='Select your school first...',
    )
    matric_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'school', 'department', 'matric_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control glass-input'})
        self.fields['department'].widget.attrs.update({'id': 'id_department'})
        self.fields['school'].widget.attrs.update({'id': 'id_school'})

        # Populate the department dropdown so validation succeeds whether the
        # school was chosen via POST data or a bound instance is re-rendered
        # after a validation error (progressive enhancement; JS narrows this
        # further on the client without a page reload).
        school = None
        if self.data.get('school'):
            try:
                school = School.objects.get(pk=self.data.get('school'))
            except (School.DoesNotExist, ValueError, TypeError):
                school = None
        if school:
            self.fields['department'].queryset = Department.objects.filter(school=school)
        else:
            self.fields['department'].queryset = Department.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        school = cleaned_data.get('school')
        department = cleaned_data.get('department')
        if school and department and department.school_id != school.id:
            self.add_error('department', 'Please choose a department that belongs to the selected school.')
        return cleaned_data


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control glass-input'})


class ProfileEditForm(forms.ModelForm):
    school = forms.ModelChoiceField(
        queryset=School.objects.filter(is_active=True),
        required=True,
        empty_label='Select your school...',
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        empty_label='Select your department...',
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'school', 'department', 'matric_number', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control glass-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'bio':
                field.widget.attrs.update({'class': 'form-control glass-input'})
        self.fields['department'].widget.attrs.update({'id': 'id_department'})
        self.fields['school'].widget.attrs.update({'id': 'id_school'})

        # Narrow the department dropdown to the currently selected/submitted
        # school so a full page load already shows the right options; the
        # AJAX endpoint refines this further without reloading the page.
        school = None
        if self.data.get('school'):
            try:
                school = School.objects.get(pk=self.data.get('school'))
            except (School.DoesNotExist, ValueError, TypeError):
                school = None
        elif self.instance and self.instance.school_id:
            school = self.instance.school
        if school:
            self.fields['department'].queryset = Department.objects.filter(school=school)

    def clean(self):
        cleaned_data = super().clean()
        school = cleaned_data.get('school')
        department = cleaned_data.get('department')
        if school and department and department.school_id != school.id:
            self.add_error('department', 'Please choose a department that belongs to the selected school.')
        return cleaned_data


class VerifyOTPForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control glass-input'}))
    otp_code = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'class': 'form-control glass-input'}))


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control glass-input'}))


class PasswordResetConfirmForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control glass-input'}))
    otp_code = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'class': 'form-control glass-input'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control glass-input'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control glass-input'}))
