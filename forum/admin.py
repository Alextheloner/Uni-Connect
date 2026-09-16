from django.contrib import admin
from .models import School, Department, Course, Thread, Reply, Tag, Vote, Bookmark, Notification


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'school_type', 'state', 'is_active', 'get_department_count']
    list_filter = ['school_type', 'state', 'is_active']
    search_fields = ['name', 'short_name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    fieldsets = (
        (None, {'fields': ('name', 'short_name', 'slug', 'school_type', 'state', 'is_active')}),
    )

    @admin.display(description='Departments')
    def get_department_count(self, obj):
        return obj.get_department_count()


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'school', 'faculty', 'get_course_count']
    list_filter = ['school', 'faculty']
    search_fields = ['name', 'code', 'faculty', 'school__name', 'school__short_name']
    autocomplete_fields = ['school']
    ordering = ['school__name', 'name']
    fieldsets = (
        (None, {'fields': ('school', 'name', 'code', 'faculty', 'description')}),
        ('Appearance', {'fields': ('color', 'icon')}),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'department', 'level', 'semester', 'units', 'is_active']
    list_filter = ['department__school', 'department', 'level', 'semester', 'is_active']
    search_fields = ['code', 'title']
    autocomplete_fields = ['department']


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'course', 'status', 'views', 'is_pinned', 'created_at']
    list_filter = ['status', 'is_pinned', 'course__department__school', 'course__department']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['views', 'created_at', 'updated_at']
    autocomplete_fields = ['course', 'author']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'thread', 'is_verified', 'created_at']
    list_filter = ['is_verified']


admin.site.register(Tag)
admin.site.register(Vote)
admin.site.register(Bookmark)
admin.site.register(Notification)
