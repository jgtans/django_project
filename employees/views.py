from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Employee


def index(request):
    # ЗАЧЕМ prefetch_related: навыки всех сотрудников — двумя доп. запросами, а не по одному на карточку
    employees = Employee.objects.all().prefetch_related("employeeskill_set__skill")
    return render(request, "index.html", {"employees": employees})


class EmployeeListView(ListView):
    # ЗАЧЕМ queryset вместо model: model=Employee дал бы all() без prefetch
    queryset = Employee.objects.all().prefetch_related("employeeskill_set__skill")
    template_name = "employees/employee_list.html"
    context_object_name = (
        "employees"  # ЗАЧЕМ: дефолт — object_list, а шаблон ждёт employees
    )


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    # ЗАЧЕМ LoginRequiredMixin: классный аналог @login_required (K8 сохраняется)
    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"
    # DetailView сама делает get_object_or_404 «под капотом» — 404 при /employees/999/ остаётся
