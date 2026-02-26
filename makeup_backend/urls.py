from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('faculty/', views.faculty, name='faculty'),
    path('student/', views.student, name='student'),
    path('ai/', views.ai_insights, name='ai'),
]