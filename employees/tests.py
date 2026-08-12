import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from workspaces.models import Workspace

from .models import Employee


class NeighborValidationTests(TestCase):
    """Бизнес-правило: тестировщики и разработчики не сидят за соседними столами."""

    @classmethod
    def setUpTestData(cls):
        cls.desk_101 = Workspace.objects.create(
            number="A-101", floor=1, workspace_type="офисное"
        )
        cls.desk_102 = Workspace.objects.create(
            number="A-102", floor=1, workspace_type="офисное"
        )
        cls.desk_103 = Workspace.objects.create(
            number="A-103", floor=1, workspace_type="офисное"
        )

    def test_tester_neighbour_of_developer_forbidden(self):
        Employee.objects.create(
            first_name="Иван",
            last_name="Бэкендов",
            gender="M",
            role="backend",
            workspace=self.desk_101,
        )
        tester = Employee(
            first_name="Пётр",
            last_name="Тестов",
            gender="M",
            role="tester",
            workspace=self.desk_102,
        )
        with self.assertRaises(ValidationError):
            tester.full_clean()

    def test_developer_neighbour_of_tester_forbidden(self):
        Employee.objects.create(
            first_name="Пётр",
            last_name="Тестов",
            gender="M",
            role="tester",
            workspace=self.desk_102,
        )
        dev = Employee(
            first_name="Иван",
            last_name="Фронтендов",
            gender="M",
            role="frontend",
            workspace=self.desk_103,
        )
        with self.assertRaises(ValidationError):
            dev.full_clean()

    def test_two_developers_neighbours_allowed(self):
        Employee.objects.create(
            first_name="Иван",
            last_name="Бэкендов",
            gender="M",
            role="backend",
            workspace=self.desk_101,
        )
        dev = Employee(
            first_name="Анна",
            last_name="Фронтендова",
            gender="F",
            role="frontend",
            workspace=self.desk_102,
        )
        dev.full_clean()  # не должен бросать исключение

    def test_other_role_neighbour_of_tester_allowed(self):
        Employee.objects.create(
            first_name="Пётр",
            last_name="Тестов",
            gender="M",
            role="tester",
            workspace=self.desk_101,
        )
        manager = Employee(
            first_name="Мария",
            last_name="Управляющая",
            gender="F",
            role="other",
            workspace=self.desk_102,
        )
        manager.full_clean()

    def test_employee_without_workspace_allowed(self):
        newbie = Employee(
            first_name="Новый", last_name="Сотрудник", gender="M", role="tester"
        )
        newbie.full_clean()


class TenureTests(TestCase):
    """Стаж автоматически считается от даты найма."""

    def test_tenure_days(self):
        emp = Employee.objects.create(
            first_name="Анна",
            last_name="Смирнова",
            gender="F",
            hired_at=datetime.date.today() - datetime.timedelta(days=10),
        )
        self.assertEqual(emp.tenure_days, 10)
