from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.dashboard, name='dashboard'),
    path('faculty/', views.faculty, name='faculty'),
    path('student/', views.student, name='student'),
    path('ai/', views.ai, name='ai'),

    # Auth
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),

    # APIs
    path('api/create-class/', views.create_makeup_class),
    path('api/mark-attendance/', views.mark_attendance),
    path('api/dashboard-stats/', views.dashboard_stats_api),
]