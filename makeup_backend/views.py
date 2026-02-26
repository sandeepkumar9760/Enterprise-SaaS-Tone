import json
from functools import wraps

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.db.models.functions import ExtractMonth

from .models import MakeUpClass, Student, Attendance


# =====================================================
# 🔐 AUTHENTICATION
# =====================================================

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect("dashboard")

        return render(request, "admin_login.html", {
            "error": "Invalid credentials"
        })

    return render(request, "admin_login.html")


def admin_logout_view(request):
    logout(request)
    return redirect("admin_login")


# =====================================================
# 🔒 STAFF ACCESS DECORATOR
# =====================================================

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect("admin_login")
        return view_func(request, *args, **kwargs)
    return wrapper


# =====================================================
# 📊 PAGE VIEWS (TEMPLATES ONLY)
# =====================================================

@staff_required
def dashboard(request):
    return render(request, "index.html")


@staff_required
def faculty(request):
    return render(request, "faculty.html")


@staff_required
def student(request):
    return render(request, "student.html")


@staff_required
def ai(request):
    return render(request, "ai_insights.html")


# =====================================================
# 📊 API: DASHBOARD DATA (FULLY DB DRIVEN)
# =====================================================

@staff_required
def dashboard_data(request):
    total_classes = MakeUpClass.objects.count()
    total_students = Student.objects.count()
    total_attendance = Attendance.objects.count()

    attendance_rate = 0
    if total_students > 0 and total_classes > 0:
        max_possible = total_students * total_classes
        attendance_rate = round((total_attendance / max_possible) * 100, 2)

    recent_activity = Attendance.objects.select_related("makeup_class")\
        .order_by("-marked_at")[:5]

    activity_data = [
        {
            "subject": a.makeup_class.subject,
            "date": a.marked_at.strftime("%Y-%m-%d %H:%M")
        }
        for a in recent_activity
    ]

    return JsonResponse({
        "total_classes": total_classes,
        "total_students": total_students,
        "total_attendance": total_attendance,
        "attendance_rate": attendance_rate,
        "recent_activity": activity_data
    })


# =====================================================
# 👨‍🏫 API: CREATE MAKE-UP CLASS
# =====================================================

import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@require_POST
@staff_required
def create_makeup_class(request):
    try:
        data = json.loads(request.body)

        subject = data.get("subject")
        classroom = data.get("classroom")
        date_str = data.get("date")
        time_str = data.get("time")
        description = data.get("description", "")

        # Validation
        if not all([subject, classroom, date_str, time_str]):
            return JsonResponse(
                {"message": "All required fields must be filled"},
                status=400
            )

        # Convert to proper date/time objects
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%H:%M").time()

        makeup = MakeUpClass.objects.create(
            subject=subject,
            classroom=classroom,
            date=date_obj,
            time=time_obj,
            description=description
        )

        return JsonResponse({
            "message": "Class created successfully",
            "remedial_code": makeup.remedial_code
        }, status=201)

    except Exception as e:
        return JsonResponse(
            {"message": str(e)},
            status=400
        )
# =====================================================
# 👨‍🏫 API: FACULTY CLASS LIST
# =====================================================

@staff_required
def faculty_classes(request):

    classes = MakeUpClass.objects.annotate(
        student_count=Count("attendance_set")
    ).order_by("-created_at")

    data = [
        {
            "subject": c.subject,
            "date": c.date.strftime("%Y-%m-%d"),
            "time": c.time.strftime("%H:%M"),
            "classroom": c.classroom,
            "code": c.remedial_code,
            "students": c.student_count
        }
        for c in classes
    ]

    return JsonResponse(data, safe=False)


# =====================================================
# 👨‍🎓 API: MARK ATTENDANCE
# =====================================================

@require_POST
@staff_required
def mark_attendance(request):
    try:
        data = json.loads(request.body)
        code = data.get("remedial_code")

        if not code:
            return JsonResponse({"message": "Remedial code required"}, status=400)

        try:
            makeup = MakeUpClass.objects.get(remedial_code=code)
        except MakeUpClass.DoesNotExist:
            return JsonResponse({"message": "Invalid Remedial Code"}, status=404)

        student, _ = Student.objects.get_or_create(
            roll_number=request.user.username,
            defaults={
                "name": request.user.username,
                "email": request.user.email
            }
        )

        if Attendance.objects.filter(student=student, makeup_class=makeup).exists():
            return JsonResponse(
                {"message": "Attendance already marked"},
                status=409
            )

        Attendance.objects.create(
            student=student,
            makeup_class=makeup
        )

        return JsonResponse(
            {"message": "Attendance marked successfully"},
            status=201
        )

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


# =====================================================
# 👨‍🎓 API: STUDENT HISTORY
# =====================================================

@login_required
def student_attendance_history(request):

    student, _ = Student.objects.get_or_create(
        roll_number=request.user.username,
        defaults={
            "name": request.user.username,
            "email": request.user.email
        }
    )

    attendance_records = Attendance.objects.filter(
        student=student
    ).select_related("makeup_class").order_by("-marked_at")

    data = [
        {
            "code": record.makeup_class.remedial_code,
            "subject": record.makeup_class.subject,
            "date": record.makeup_class.date.strftime("%Y-%m-%d"),
            "time": record.makeup_class.time.strftime("%H:%M"),
            "status": "Present"
        }
        for record in attendance_records
    ]

    return JsonResponse({"records": data})


# =====================================================
# 👨‍🎓 API: STUDENT METRICS
# =====================================================

@login_required
def student_metrics(request):

    student, _ = Student.objects.get_or_create(
        roll_number=request.user.username,
        defaults={
            "name": request.user.username,
            "email": request.user.email
        }
    )

    total_sessions = MakeUpClass.objects.count()
    attended_sessions = Attendance.objects.filter(student=student).count()

    attendance_rate = 0
    if total_sessions > 0:
        attendance_rate = round((attended_sessions / total_sessions) * 100, 2)

    return JsonResponse({
        "total_sessions": attended_sessions,
        "attendance_rate": attendance_rate,
        "pending_sessions": total_sessions - attended_sessions
    })


# =====================================================
# 🤖 API: AI ANALYTICS (POSTGRES SAFE)
# =====================================================

@staff_required
def ai_analytics(request):

    monthly_data = Attendance.objects.annotate(
        month=ExtractMonth("marked_at")
    ).values("month").annotate(
        count=Count("id")
    ).order_by("month")

    data = [
        {"month": m["month"], "attendance": m["count"]}
        for m in monthly_data
    ]

    return JsonResponse({"trend": data})