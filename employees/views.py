from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .api_filters import EmployeeFilterSet
from .forms import EmployeeForm
from .models import Employee
from .permissions import EmployeeRolePermission
from .serializers import EmployeeSerializer


def index(request):
    total_count = Employee.objects.count()
    employees = Employee.objects.order_by("-hired_at")[:4].prefetch_related(
        "employeeskill_set__skill", "photos"
    )
    return render(
        request,
        "index.html",
        {"employees": employees, "total_count": total_count},
    )


class EmployeeListView(ListView):
    queryset = Employee.objects.all().prefetch_related(
        "employeeskill_set__skill", "photos"
    )
    template_name = "employees/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"
    queryset = Employee.objects.select_related("workspace").prefetch_related(
        "employeeskill_set__skill", "photos"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = [p for p in self.object.photos.all() if p.image]
        context["main_photo"] = photos[0] if photos else None
        context["gallery"] = photos[1:]
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"
    success_url = reverse_lazy("employee_list")


class EmployeeViewSet(viewsets.ModelViewSet):
    """CRUD-контроллер API (ДЗ 6, K4) с фильтрами (K3) и правами (K6)."""

    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilterSet
    filter_backends = [DjangoFilterBackend]
    permission_classes = [EmployeeRolePermission]

    def get_queryset(self):
        return Employee.objects.select_related("workspace").prefetch_related(
            "employeeskill_set__skill", "photos"
        )
