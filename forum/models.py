from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.functions import Lower


class School(models.Model):
    """A tertiary institution in Nigeria: university, polytechnic, college of
    education, or monotechnic. Every Department belongs to exactly one School,
    and every User belongs to exactly one School."""

    SCHOOL_TYPE_CHOICES = [
        ('university', 'University'),
        ('polytechnic', 'Polytechnic'),
        ('college_of_education', 'College of Education'),
        ('monotechnic', 'Monotechnic'),
    ]

    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(
        max_length=50, blank=True,
        help_text='Common abbreviation, e.g. UNN, UNILAG, FUTA'
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    school_type = models.CharField(max_length=30, choices=SCHOOL_TYPE_CHOICES, default='university')
    state = models.CharField(max_length=100, blank=True, help_text='Nigerian state where the school is located')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['short_name']),
        ]

    def __str__(self):
        return self.short_name or self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.short_name or self.name)
            slug = base_slug
            counter = 1
            while School.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f'{base_slug}-{counter}'
            self.slug = slug
        super().save(*args, **kwargs)

    def get_department_count(self):
        return self.departments.count()

    def get_thread_count(self):
        return Thread.objects.filter(
            course__department__school=self, is_deleted=False
        ).count()


class Department(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='departments',
        null=True, blank=True,
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    faculty = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6C63FF')
    icon = models.CharField(max_length=50, default='bi-mortarboard')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = ['school', 'code']
        constraints = [
            models.UniqueConstraint(
                Lower('name'), 'school',
                name='unique_department_name_per_school',
            ),
        ]
        indexes = [
            models.Index(fields=['school', 'code']),
        ]

    def __str__(self):
        if self.school_id:
            return f"{self.name} ({self.school})"
        return self.name

    def get_course_count(self):
        return self.courses.count()

    def get_thread_count(self):
        return Thread.objects.filter(course__department=self, is_deleted=False).count()


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=10, default='100L')
    semester = models.CharField(max_length=20, default='First Semester')
    units = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']
        unique_together = ['department', 'code']

    def __str__(self):
        return f"{self.code} - {self.title}"

    def get_thread_count(self):
        return self.threads.filter(is_deleted=False).count()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#6C63FF')

    def __str__(self):
        return self.name


class Thread(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='threads')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=300)
    content = models.TextField()
    attachment = models.FileField(upload_to='thread_attachments/', blank=True, null=True)
    voice_note = models.FileField(upload_to='thread_voice_notes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    is_pinned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    @property
    def reply_count(self):
        return self.replies.filter(is_deleted=False).count()

    @property
    def upvote_count(self):
        return self.votes.filter(value=1).count()

    @property
    def has_verified_answer(self):
        return self.replies.filter(is_verified=True).exists()


    @property
    def department(self):
        return self.course.department

    @property
    def school(self):
        return self.course.department.school


class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    attachment = models.FileField(upload_to='reply_attachments/', blank=True, null=True)
    voice_note = models.FileField(upload_to='reply_voice_notes/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='verified_replies'
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_verified', 'created_at']

    def __str__(self):
        return f"Reply by {self.author} on {self.thread}"

    @property
    def upvote_count(self):
        return self.votes.filter(value=1).count()


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    value = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'thread'),
            ('user', 'reply'),
        ]


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'thread']


class Notification(models.Model):
    TYPE_CHOICES = [
        ('reply', 'Reply to your thread'),
        ('vote', 'Upvote on your post'),
        ('verified', 'Your reply was verified'),
        ('mention', 'You were mentioned'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ChatRoom(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' / '.join([user.username for user in self.participants.all()])

    def get_other_user(self, user):
        return self.participants.exclude(pk=user.pk).first()


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
