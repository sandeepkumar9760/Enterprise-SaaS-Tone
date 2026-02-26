from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # 🔐 Authentication
    # ==========================
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),

    # ==========================
    # 📄 Page Views
    # ==========================
    path('', views.dashboard, name='dashboard'),
    path('faculty/', views.faculty, name='faculty'),
    path('student/', views.student, name='student'),
    path('ai/', views.ai, name='ai'),

    # ==========================
    # 📊 Dashboard APIs
    # ==========================
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),

    # ==========================
    # 👨‍🏫 Faculty APIs
    # ==========================
    path('api/faculty/create-class/', views.create_makeup_class, name='create_class'),
    path('api/faculty/classes/', views.faculty_classes, name='faculty_classes'),

    # ==========================
    # 👨‍🎓 Student APIs
    # ==========================
    path('api/student/mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('api/student/history/', views.student_attendance_history, name='student_history'),
    path('api/student/metrics/', views.student_metrics, name='student_metrics'),

    # ==========================
    # 🤖 AI APIs
    # ==========================
    path('api/ai/analytics/', views.ai_analytics, name='ai_analytics'),
    path('api/faculty/delete-class/<int:class_id>/', views.delete_class, name='delete_class'),
    path('api/faculty/edit-class/<int:class_id>/', views.edit_class, name='edit_class'),
]