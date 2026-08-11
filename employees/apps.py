from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    name = "employees"
    verbose_name = "Сотрудники"


def ready(self):
    import employees.signals
