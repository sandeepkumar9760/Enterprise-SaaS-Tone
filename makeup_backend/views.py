from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def faculty(request):
    return render(request, "faculty.html")

def student(request):
    return render(request, "student.html")

def ai_insights(request):
    return render(request, "ai_insights.html")




def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            return render(request, "admin_login.html", {"error": "Invalid credentials"})

    return render(request, "admin_login.html")


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("admin_login")

    return render(request, "admin_dashboard.html")


def admin_logout_view(request):
    logout(request)
    return redirect("admin_login")