from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import EmployeeForm
from .models import Employee


def index(request):
    # count() - бд считает строки сама, объекты не создаются
    total_count = Employee.objects.count()
    # перед полем: сортировка по убыванию даты
    # срез [:4] в SQL превращается в LIMIT 4
    employees = Employee.objects.order_by("-hired_at")[:4].prefetch_related(
        "employeeskill_set__skill", "photos"
    )
    return render(
        request, "index.html", {"employees": employees, "total_count": total_count}
    )


class EmployeeListView(ListView):
    # queryset вместо model: model=Employee дал бы all() без prefetch
    queryset = Employee.objects.all().prefetch_related(
        "employeeskill_set__skill", "photos"
    )
    template_name = "employees/employee_list.html"
    context_object_name = "employees"  # дефолт — object_list, а шаблон ждёт employees
    paginate_by = 10  # окно из 10 карточек, в SQL - LIMIT 10 OFFSET


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    # LoginRequiredMixin: классный аналог @login_required (K8 сохраняется)
    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"
    # DetailView сама делает get_object_or_404 «под капотом» — 404 при /employees/999/ остаётся
    queryset = Employee.objects.select_related("workspace").prefetch_related(
        "employeeskill_set__skill", "photos"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ЗАЧЕМ .all() + list comprehension: берём фото ИЗ КЭША prefetch (0 доп. запросов)
        # и в Python отсеиваем призраков без файла
        photos = [p for p in self.object.photos.all() if p.image]
        context["main_photo"] = photos[0] if photos else None
        context["gallery"] = photos[1:]
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"
    success_url = reverse_lazy("employee_list")
