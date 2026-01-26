from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category", views.product, name="category"),
    path("product", views.product, name="product"),
    path("employee", views.employee, name="employee"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("employee-login", views.employee_login, name="employee_login"),
    path("employee-sell", views.employeesell, name="employeesell"),
    path("update-order-status/<str:order_id>", views.update_order_status, name="update_order_status"),
    path("create-order", views.create_order, name="create_order"),
    path("chat", views.chat, name="chat"),
    path("shop", views.shop, name="shop"),
    path("booking", views.booking, name="booking"),
    path("add-product", views.add_product, name="add_product"),
    path("cancel-booking/<str:booking_id>", views.cancel_booking, name="cancel_booking"),
]
