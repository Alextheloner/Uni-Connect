from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
    ]
    is_email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    school = models.ForeignKey(
        'forum.School', on_delete=models.SET_NULL, null=True, blank=True, related_name='members'
    )
    department = models.ForeignKey(
        'forum.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='members'
    )
    matric_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    reputation = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_lecturer(self):
        return self.role == 'lecturer'


    def can_access_department(self, department):
        """Users may only view/post in a department that belongs to their
        own school. Superusers and staff are exempt. If a user has not
        selected a school yet, access is allowed (legacy/incomplete profile)."""
        if self.is_superuser or self.is_staff:
            return True
        if not self.school_id:
            return True
        if department is None:
            return True
        return department.school_id == self.school_id


    @property
    def thread_count(self):
        return self.threads.filter(is_deleted=False).count()

    @property
    def reply_count(self):
        return self.replies.filter(is_deleted=False).count()


class OTPCode(models.Model):
    PURPOSE_CHOICES = [
        ('email_verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=8)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.purpose}"

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at
