import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

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
        dev.full_clean()

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

    def test_tester_two_desks_away_allowed(self):
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
            workspace=self.desk_103,
        )
        tester.full_clean()


class TenureTests(TestCase):
    """Стаж автоматически считается от даты найма."""

    def test_tenure_days(self):
        emp = Employee(
            first_name="Анна",
            last_name="Смирнова",
            gender="F",
            hired_at=timezone.localdate() - datetime.timedelta(days=10),
        )
        self.assertEqual(emp.tenure_days, 10)

    def test_tenure_zero_on_hire_day(self):
        emp = Employee(
            first_name="Новичок",
            last_name="Нулевой",
            gender="M",
            hired_at=timezone.localdate(),
        )
        self.assertEqual(emp.tenure_days, 0)


class ClientSmokeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.desk = Workspace.objects.create(
            number="A-101",
            floor=1,
            workspace_type="офисное",
        )
        cls.employee = Employee.objects.create(
            first_name="Иван",
            last_name="Иванов",
            gender="M",
            workspace=cls.desk,
        )

    def test_main_page_opens_for_anonymous(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_list_page_shows_employee_last_name(self):
        response = self.client.get("/employees/")
        self.assertContains(response, "Иванов")


class MainContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.desk = Workspace.objects.create(
            number="A-101",
            floor=1,
            workspace_type="офисное",
        )
        cls.employee = Employee.objects.create(
            first_name="Иван",
            last_name="Иванов",
            gender="M",
            workspace=cls.desk,
        )

    def test_main_uses_base_and_index_templates(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "index.html")

    def test_main_context_has_total_count(self):
        response = self.client.get("/")
        self.assertEqual(response.context["total_count"], 1)

    def test_main_context_has_recent_employees(self):
        response = self.client.get("/")
        self.assertQuerySetEqual(response.context["employees"], [self.employee])

    def test_list_uses_employee_list_template(self):
        response = self.client.get("/employees/")
        self.assertTemplateUsed(response, "employees/employee_list.html")

    def test_list_not_paginated_with_one_employee(self):
        response = self.client.get("/employees/")
        self.assertFalse(response.context["is_paginated"])

    def test_list_paginated_when_eleven_employees(self):
        for i in range(10):
            Employee.objects.create(
                first_name=f"Тест{i}",
                last_name=f"Много{i}",
                gender="M",
            )
        response = self.client.get("/employees/")
        self.assertTrue(response.context["is_paginated"])


class DetailAccessTests(TestCase):
    """ДЗ 5, K3–K4: права доступа к детальной странице."""

    @classmethod
    def setUpTestData(cls):
        cls.desk = Workspace.objects.create(
            number="A-101", floor=1, workspace_type="офисное"
        )
        cls.employee = Employee.objects.create(
            first_name="Иван", last_name="Иванов", gender="M", workspace=cls.desk
        )
        cls.user = User.objects.create_user(username="boss", password="pass12345")

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(f"/employees/{self.employee.pk}/")
        self.assertRedirects(response, f"/login/?next=/employees/{self.employee.pk}/")

    def test_authenticated_gets_200_and_context(self):
        self.client.force_login(self.user)
        response = self.client.get(f"/employees/{self.employee.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_detail.html")
        self.assertEqual(response.context["employee"], self.employee)
