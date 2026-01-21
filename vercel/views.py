from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def product(request):
    return render(request, "cat.html")

def employee(request):
    return render(request, "employee.html")

def login(request):
    return render(request, "login.html")

def chat(request):
    return render(request, "chat.html")
def shop(request):
    return render(request, "shop.html")