import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count

from .models import MakeUpClass, Student, Attendance


# =====================================================
# 🔐 AUTHENTICATION SYSTEM
# =====================================================

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("dashboard")
        else:
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
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect("admin_login")
        return view_func(request, *args, **kwargs)
    return wrapper


# =====================================================
# 📊 DASHBOARD (Protected)
# =====================================================

@staff_required
def dashboard(request):
    total_classes = MakeUpClass.objects.count()
    total_attendance = Attendance.objects.count()
    active_codes = MakeUpClass.objects.filter().count()

    attendance_rate = 0
    if total_classes > 0:
        attendance_rate = round((total_attendance / total_classes) * 100, 2)

    return render(request, "index.html", {
        "total_classes": total_classes,
        "total_attendance": total_attendance,
        "active_codes": active_codes,
        "attendance_rate": attendance_rate
    })


# =====================================================
# 👨‍🏫 FACULTY PAGE (Protected)
# =====================================================

@staff_required
def faculty(request):
    classes = MakeUpClass.objects.all().order_by("-created_at")

    return render(request, "faculty.html", {
        "classes": classes
    })


# =====================================================
# 👨‍🎓 STUDENT PAGE (Protected)
# =====================================================

@staff_required
def student(request):
    return render(request, "student.html")


# =====================================================
# 🤖 AI INSIGHTS PAGE (Protected)
# =====================================================

@staff_required
def ai(request):
    return render(request, "ai_insights.html")


# =====================================================
# 🚀 API: CREATE MAKE-UP CLASS
# =====================================================

@require_POST
@staff_required
def create_makeup_class(request):
    try:
        data = json.loads(request.body)

        makeup = MakeUpClass.objects.create(
            subject=data.get("subject"),
            classroom=data.get("classroom"),
            date=data.get("date"),
            time=data.get("time"),
            description=data.get("description"),
        )

        return JsonResponse({
            "status": "success",
            "remedial_code": makeup.remedial_code
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)


# =====================================================
# 🚀 API: MARK ATTENDANCE
# =====================================================

@require_POST
@staff_required
def mark_attendance(request):
    try:
        data = json.loads(request.body)
        code = data.get("remedial_code")
        roll = data.get("roll_number")

        try:
            makeup = MakeUpClass.objects.get(remedial_code=code)
        except MakeUpClass.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Invalid Remedial Code"
            })

        student, created = Student.objects.get_or_create(
            roll_number=roll,
            defaults={
                "name": roll,
                "email": f"{roll}@example.com"
            }
        )

        if Attendance.objects.filter(student=student, makeup_class=makeup).exists():
            return JsonResponse({
                "status": "error",
                "message": "Attendance already marked"
            })

        Attendance.objects.create(
            student=student,
            makeup_class=makeup
        )

        return JsonResponse({
            "status": "success",
            "message": "Attendance marked successfully"
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)


# =====================================================
# 📊 API: DASHBOARD STATS (Optional Future Use)
# =====================================================

@staff_required
def dashboard_stats_api(request):
    total_classes = MakeUpClass.objects.count()
    total_students = Student.objects.count()
    total_attendance = Attendance.objects.count()

    return JsonResponse({
        "total_classes": total_classes,
        "total_students": total_students,
        "total_attendance": total_attendance
    })