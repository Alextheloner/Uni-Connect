from django import forms
from .models import Thread, Reply, Course, Department


class ThreadForm(forms.ModelForm):
    attachment = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control glass-input'}))
    voice_note = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control glass-input'}))

    class Meta:
        model = Thread
        fields = ['course', 'title', 'content', 'tags', 'attachment', 'voice_note']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Ask a clear, specific question...'}),
            'content': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 6, 'placeholder': 'Provide context, what you have tried, relevant course material...'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkbox'}),
            'course': forms.Select(attrs={'class': 'form-select glass-input'}),
        }

    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        self._restricted_course_ids = None
        if department:
            qs = Course.objects.filter(department=department, is_active=True)
            self.fields['course'].queryset = qs
            self._restricted_course_ids = set(qs.values_list('id', flat=True))
        elif school:
            # No specific department pre-selected (e.g. lecturer with no
            # department) — still keep the picker limited to their own school.
            qs = Course.objects.filter(department__school=school, is_active=True)
            self.fields['course'].queryset = qs
            self._restricted_course_ids = set(qs.values_list('id', flat=True))

    def clean_course(self):
        """Defense in depth: even if a course id from another school is
        submitted directly (bypassing the narrowed dropdown), reject it here
        too — the view is responsible for passing `department`/`school`."""
        course = self.cleaned_data.get('course')
        if course and self._restricted_course_ids is not None and course.id not in self._restricted_course_ids:
            raise forms.ValidationError('Please choose a course from your own school and department.')
        return course


class ReplyForm(forms.ModelForm):
    attachment = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control glass-input'}))
    voice_note = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control glass-input'}))

    class Meta:
        model = Reply
        fields = ['content', 'attachment', 'voice_note']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control glass-input',
                'rows': 4,
                'placeholder': 'Share your knowledge, be clear and helpful...'
            }),
        }


class ChatMessageForm(forms.Form):
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control glass-input',
        'rows': 3,
        'placeholder': 'Type a message or attach a file...'
    }))
    attachment = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control glass-input'}))


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control glass-input',
            'placeholder': 'Search threads, courses, topics...',
        })
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label='All Departments',
        widget=forms.Select(attrs={'class': 'form-select glass-input'})
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        required=False,
        empty_label='All Courses',
        widget=forms.Select(attrs={'class': 'form-select glass-input'})
    )
    status = forms.ChoiceField(
        choices=[('', 'Any Status'), ('open', 'Open'), ('resolved', 'Resolved')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select glass-input'})
    )
