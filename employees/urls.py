from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("employees/", views.EmployeeListView.as_view(), name="employee_list"),
    path(
        "employees/<int:pk>/",
        views.EmployeeDetailView.as_view(),
        name="employee_detail",
    ),
]
