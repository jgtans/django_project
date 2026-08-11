import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Skill(models.Model):
    """Навык (Python, Django, тестирование и т.д.)."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Навык")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Сотрудник компании."""

    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]

    # --- Поля ---
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Пол",
    )
    hired_at = models.DateField(
        default=datetime.date.today,
        verbose_name="Дата трудоустройства",
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    workspace = models.ForeignKey(
        "workspaces.Workspace",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рабочее место",
        related_name="current_employee",
    )
    # ВАЖНО: строковая ссылка "Skill", а не сам класс Skill
    # Это защищает от NameError, если порядок классов поменяется
    skills = models.ManyToManyField(
        "Skill",
        through="EmployeeSkill",
        verbose_name="Навыки",
        blank=True,
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def tenure_days(self):
        """Стаж в днях — считается автоматически от hired_at."""
        from django.utils import timezone

        delta = timezone.now().date() - self.hired_at
        return delta.days


class EmployeeSkill(models.Model):
    """Промежуточная таблица: сотрудник + навык + уровень (1-10)."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник",
    )
    skill = models.ForeignKey(
        "Skill",  # можно "Skill" или просто Skill — Skill уже объявлен выше
        on_delete=models.CASCADE,
        verbose_name="Навык",
    )
    level = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Уровень (1-10)",
    )

    class Meta:
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "skill"],
                name="unique_employee_skill",
            )
        ]

    def __str__(self):
        return f"{self.employee} — {self.skill} ({self.level})"


class EmployeePhoto(models.Model):
    """Фото сотрудника первое в порядке сортировки, является заглавным"""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="photo",
        verbose_name="Сотрудник",
    )
    image = models.ImageField(upload_to="employees/photos/", verbose_name="Фотография")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Фото сотрудника"
        verbose_name_plural = "Фотографии сотрудников"
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "order"],
                name="unique_employee_photo_order",
            )
        ]

    def __str__(self):
        return f"{self.employee} - фото №{self.order}"


@property
def cover_photo(self):
    return self.photo.first()


# TODO: добавить сбор метрик WorkSession() "10мин простоя-пауза"
