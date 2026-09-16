from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='home'),
    path('departments/', views.department_list, name='departments'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('threads/', views.thread_list, name='thread_list'),
    path('threads/new/', views.create_thread, name='create_thread'),
    path('threads/new/<int:course_pk>/', views.create_thread, name='create_thread_course'),
    path('threads/<int:pk>/', views.thread_detail, name='thread_detail'),
    path('threads/<int:thread_pk>/reply/', views.add_reply, name='add_reply'),
    path('threads/<int:pk>/vote/', views.vote_thread, name='vote_thread'),
    path('threads/<int:pk>/bookmark/', views.bookmark_thread, name='bookmark_thread'),
    path('replies/<int:pk>/vote/', views.vote_reply, name='vote_reply'),
    path('replies/<int:pk>/verify/', views.verify_reply, name='verify_reply'),
    path('bookmarks/', views.my_bookmarks, name='bookmarks'),
    path('notifications/', views.notifications, name='notifications'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('chats/', views.chat_list, name='chat_list'),
    path('chats/start/<str:username>/', views.start_chat, name='start_chat'),
    path('chats/<int:room_pk>/', views.chat_room, name='chat_room'),
]
