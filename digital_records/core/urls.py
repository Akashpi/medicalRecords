from django.urls import path
from core import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_record, name='upload'),
    path('records/', views.records, name='records'),
    path('ai-chat/', views.ai_chat, name='ai_chat'),
]
