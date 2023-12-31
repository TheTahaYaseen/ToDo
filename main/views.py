from django.shortcuts import redirect, render

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Todo

# Create your views here.
def home_view(request):
    # Home View Would Contain Recent Todos Of People (Globally)
    context = {}
    return render(request, "main/home_view.html", context)

def registration_view(request):
    # Allows User To Register
    
    form = UserCreationForm()

    error = ""

    if request.method == "POST":        
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        
        else:
            error = "An Error Occured During Registration!"

    context = {"form": form, "error": error}
    return render(request, "main/registration_view.html", context)

def login_view(request):
    # Allows User To Login
    
    error = "" 

    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
    
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            error = "User Does Not Exist"

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = "Username Or Password Is Incorrect!"

    context = {"error": error}
    return render(request, "main/login_view.html", context)

@login_required(login_url='/login')
def todos_view(request):
    # Shows The User's Todos With The Actions
    context = {}
    return render(request, "main/todos_view.html", context)

@login_required(login_url='/login')
def create_todo_view(request):
    # Will Contain All Attributes Inputs
    
    subtask_of = request.GET.get("subtask_of") if request.GET.get("subtask_of") else None

    if request.method == "POST":

        Todo.objects.create(
            task = request.POST.get("task"),
            details = request.POST.get("details"),
            deadline = request.POST.get("deadline") if request.POST.get("deadline") else None,
            subtask_of = request.POST.get("subtask_of") if request.POST.get("subtask_of") != "None"  else None,
            task_by = request.user,
            media = None
        )

    context = {"subtask_of": subtask_of}
    return render(request, "main/create_todo_view.html", context)

@login_required(login_url='/login')
def update_todo_view(request):
    # Will Contain All Attributes Inputs
    context = {}
    return render(request, "main/update_todo_view.html", context)

@login_required(login_url='/login')
def delete_todo_view(request):
    # Will Delete Todo With A Confirmation Check
    context = {}
    return render(request, "main/delete_todo_view.html", context)

@login_required(login_url='/login')
def complete_todo_view(request):
    # Will Require User To Submit Atleast One Piece Of Media According To Task
    context = {}
    return render(request, "main/complete_todo_view.html", context)

def user_profile_view(request):
    # Will Display User's Name And Email Along With His Completed Todos Having Medias In Them
    context = {}
    return render(request, "main/user_profile_view.html", context)

@login_required(login_url='/login')
def update_user_profile_view(request):
    # Will Display Form To Update Username, Email Or Password
    context = {}
    return render(request, "main/update_user_profile_view.html", context)

@login_required(login_url='/login')
def logout_view(request):
    # Will Directly Logout And Redirect User
    logout(request)
    return redirect("home")