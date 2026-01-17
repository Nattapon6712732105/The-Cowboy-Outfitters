from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category", views.product, name="category"),
    path("product", views.product, name="product"),
    path("employee", views.employee, name="employee"),
    path("login", views.login, name="login"),
    path("chat", views.chat, name="chat"),
]
