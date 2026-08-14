from django.shortcuts import get_object_or_404, render

from .models import Employee


def index(request):
    return render(request, "index.html")


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "employees/employee_list.html", {"employees": employees})


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/employee_detail.html", {"employee": employee})
