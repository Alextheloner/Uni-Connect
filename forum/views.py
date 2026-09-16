from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, F
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .models import Department, Course, Thread, Reply, Vote, Bookmark, Notification, Tag, ChatRoom, ChatMessage
from .forms import ThreadForm, ReplyForm, SearchForm, ChatMessageForm

User = get_user_model()


def home(request):
    departments = Department.objects.annotate(num_courses=Count('courses')).order_by('name')
    total_threads = Thread.objects.filter(is_deleted=False).count()
    total_users = User.objects.count()
    resolved_threads = Thread.objects.filter(status='resolved', is_deleted=False).count()
    recent_threads = Thread.objects.filter(is_deleted=False).select_related('author', 'course__department')

    # Personalize for logged-in users: show their own school's departments
    # and discussions first, without hiding the platform's overall reach.
    if request.user.is_authenticated and request.user.school_id:
        departments = departments.filter(school=request.user.school)
        recent_threads = recent_threads.filter(course__department__school=request.user.school)

    recent_threads = recent_threads[:6]

    return render(request, 'marketing/index.html', {
        'departments': departments,
        'total_threads': total_threads,
        'total_users': total_users,
        'resolved_threads': resolved_threads,
        'recent_threads': recent_threads,
    })


def department_list(request):
    departments = Department.objects.select_related('school').annotate(
        num_courses=Count('courses', distinct=True),
        num_threads=Count('courses__threads', filter=Q(courses__threads__is_deleted=False), distinct=True)
    ).order_by('school__name', 'name', 'id')
    if request.user.is_authenticated and request.user.school_id:
        departments = departments.filter(school=request.user.school)

    seen = set()
    deduped = []
    for dept in departments:
        key = (dept.school_id, dept.name.strip().lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(dept)

    return render(request, 'forum/departments.html', {'departments': deduped})


def department_detail(request, pk):
    department = get_object_or_404(Department.objects.select_related('school'), pk=pk)
    if request.user.is_authenticated and not request.user.can_access_department(department):
        messages.error(request, "That department belongs to another institution, so you can't view its discussions.")
        return redirect('forum:departments')
    courses = Course.objects.filter(department=department, is_active=True).annotate(
        thread_count=Count('threads', filter=Q(threads__is_deleted=False))
    )
    recent_threads = Thread.objects.filter(
        course__department=department, is_deleted=False
    ).select_related('author', 'course').order_by('-created_at')[:10]
    return render(request, 'forum/department_detail.html', {
        'department': department,
        'courses': courses,
        'recent_threads': recent_threads,
    })


def course_detail(request, pk):
    course = get_object_or_404(Course.objects.select_related('department__school'), pk=pk)
    if request.user.is_authenticated and not request.user.can_access_department(course.department):
        messages.error(request, "That course belongs to another institution, so you can't view its discussions.")
        return redirect('forum:departments')
    threads_qs = Thread.objects.filter(course=course, is_deleted=False).select_related('author').annotate(
        reply_count_ann=Count('replies', filter=Q(replies__is_deleted=False))
    )
    status_filter = request.GET.get('status', '')
    if status_filter in ['open', 'resolved', 'closed']:
        threads_qs = threads_qs.filter(status=status_filter)
    sort = request.GET.get('sort', 'latest')
    if sort == 'popular':
        threads_qs = threads_qs.order_by('-views', '-created_at')
    elif sort == 'unanswered':
        threads_qs = threads_qs.filter(reply_count_ann=0)
    else:
        threads_qs = threads_qs.order_by('-is_pinned', '-created_at')
    paginator = Paginator(threads_qs, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'forum/course_detail.html', {
        'course': course,
        'page_obj': page,
        'status_filter': status_filter,
        'sort': sort,
    })


def thread_list(request):
    threads_qs = Thread.objects.filter(is_deleted=False).select_related(
        'author', 'course__department__school'
    ).annotate(reply_count_ann=Count('replies', filter=Q(replies__is_deleted=False)))

    # By default, students only see discussions from their own institution.
    # Passing ?scope=all opts in to browsing every school's discussions.
    scope = request.GET.get('scope', '')
    show_all_schools = scope == 'all' or not (request.user.is_authenticated and request.user.school_id)
    if not show_all_schools:
        threads_qs = threads_qs.filter(course__department__school=request.user.school)

    form = SearchForm(request.GET or None)
    if form.is_valid():
        q = form.cleaned_data.get('q')
        department = form.cleaned_data.get('department')
        course = form.cleaned_data.get('course')
        status = form.cleaned_data.get('status')
        if q:
            threads_qs = threads_qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        if department:
            threads_qs = threads_qs.filter(course__department=department)
        if course:
            threads_qs = threads_qs.filter(course=course)
        if status:
            threads_qs = threads_qs.filter(status=status)
    paginator = Paginator(threads_qs.order_by('-created_at'), 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'forum/thread_list.html', {
        'page_obj': page,
        'form': form,
        'show_all_schools': show_all_schools,
    })


def thread_detail(request, pk):
    thread = get_object_or_404(
        Thread.objects.select_related('course__department__school'), pk=pk, is_deleted=False
    )
    if request.user.is_authenticated and not request.user.can_access_department(thread.course.department):
        messages.error(request, "That discussion belongs to another institution, so you can't view it.")
        return redirect('forum:thread_list')
    Thread.objects.filter(pk=pk).update(views=F('views') + 1)
    replies = thread.replies.filter(is_deleted=False, parent=None).select_related(
        'author', 'verified_by'
    ).prefetch_related('children')
    reply_form = ReplyForm()
    user_bookmarked = False
    user_voted_thread = False
    if request.user.is_authenticated:
        user_bookmarked = Bookmark.objects.filter(user=request.user, thread=thread).exists()
        user_voted_thread = Vote.objects.filter(user=request.user, thread=thread).exists()
    return render(request, 'forum/thread_detail.html', {
        "thread": thread,
        "replies": replies,
        "reply_form": reply_form,
        "user_bookmarked": user_bookmarked,
        "user_voted_thread": user_voted_thread,
    })


@login_required
def create_thread(request, course_pk=None):
    course = None
    if course_pk:
        course = get_object_or_404(Course.objects.select_related('department__school'), pk=course_pk)
        if not request.user.can_access_department(course.department):
            messages.error(request, "You can only start discussions within your own institution.")
            return redirect('forum:departments')

    form_kwargs = {
        'department': request.user.department,
        'school': request.user.school,
    }

    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES, **form_kwargs)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            form.save_m2m()
            messages.success(request, 'Thread posted successfully!')
            return redirect('forum:thread_detail', pk=thread.pk)
    else:
        initial = {}
        if course:
            initial['course'] = course
        form = ThreadForm(initial=initial, **form_kwargs)

    courses = Course.objects.filter(is_active=True).select_related('department')
    if request.user.school_id:
        courses = courses.filter(department__school=request.user.school)
    return render(request, 'forum/create_thread.html', {
        'form': form,
        'course': course,
        'courses': courses,
    })


@login_required
def add_reply(request, thread_pk):
    thread = get_object_or_404(
        Thread.objects.select_related('course__department__school'), pk=thread_pk, is_deleted=False
    )
    if not request.user.can_access_department(thread.course.department):
        messages.error(request, "You can only reply to discussions within your own institution.")
        return redirect('forum:thread_list')
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    reply.parent = Reply.objects.get(pk=parent_id)
                except Reply.DoesNotExist:
                    pass
            reply.save()
            if thread.author != request.user:
                Notification.objects.create(
                    user=thread.author,
                    type='reply',
                    message=f'{request.user.username} replied to your thread: "{thread.title[:60]}"',
                    thread=thread,
                )
            messages.success(request, 'Reply posted!')
    return redirect('forum:thread_detail', pk=thread_pk)


@login_required
def vote_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    vote, created = Vote.objects.get_or_create(user=request.user, thread=thread, defaults={'value': 1})
    if not created:
        vote.delete()
        voted = False
    else:
        voted = True
    return JsonResponse({'voted': voted, 'count': thread.upvote_count})


@login_required
def vote_reply(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    vote, created = Vote.objects.get_or_create(user=request.user, reply=reply, defaults={'value': 1})
    if not created:
        vote.delete()
        voted = False
    else:
        voted = True
    return JsonResponse({'voted': voted, 'count': reply.upvote_count})


@login_required
def verify_reply(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    thread = reply.thread
    if request.user == thread.author or request.user.is_lecturer:
        reply.is_verified = not reply.is_verified
        reply.verified_by = request.user if reply.is_verified else None
        reply.save()
        if reply.is_verified:
            thread.status = 'resolved'
            thread.save()
            if reply.author != request.user:
                Notification.objects.create(
                    user=reply.author,
                    type='verified',
                    message=f'Your reply was verified as the correct answer!',
                    thread=thread,
                )
    return redirect('forum:thread_detail', pk=thread.pk)


@login_required
def bookmark_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, thread=thread)
    if not created:
        bookmark.delete()
        bookmarked = False
    else:
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked})


@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related(
        'thread__author', 'thread__course__department'
    ).order_by('-created_at')
    return render(request, 'forum/bookmarks.html', {'bookmarks': bookmarks})


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'forum/notifications.html', {'notifications': notifs})


def leaderboard(request):
    top_users = User.objects.annotate(
        total_threads=Count('threads', filter=Q(threads__is_deleted=False)),
        total_replies=Count('replies', filter=Q(replies__is_deleted=False)),
    ).order_by('-reputation')[:20]
    return render(request, 'forum/leaderboard.html', {'top_users': top_users})


@login_required
def chat_list(request):
    rooms = (
        request.user.chat_rooms
        .prefetch_related('participants', 'messages')
        .all()
    )

    chat_rooms = []

    for room in rooms:
        last_message = room.messages.order_by('-created_at').first()

        chat_rooms.append({
            'room': room,
            'other_user': room.get_other_user(request.user),
            'last_message': last_message,
        })

    return render(request, 'forum/chat_list.html', {
        'chat_rooms': chat_rooms,
    })


@login_required
def chat_room(request, room_pk):
    room = get_object_or_404(ChatRoom, pk=room_pk)
    if request.user not in room.participants.all():
        return redirect('forum:chat_list')

    if request.method == 'POST':
        form = ChatMessageForm(request.POST, request.FILES)
        if form.is_valid():
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                content=form.cleaned_data.get('content', '').strip(),
                attachment=form.cleaned_data.get('attachment'),
            )
            return redirect('forum:chat_room', room_pk=room.pk)
    else:
        form = ChatMessageForm()

    messages_qs = room.messages.select_related('sender')
    other_user = room.get_other_user(request.user)
    return render(request, 'forum/chat_room.html', {
        'room': room,
        'messages': messages_qs,
        'form': form,
        'other_user': other_user,
    })


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return redirect('forum:chat_list')

    room = ChatRoom.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not room:
        room = ChatRoom.objects.create()
        room.participants.set([request.user, other_user])
    return redirect('forum:chat_room', room_pk=room.pk)
