from django.db import models


class Employee(models.Model):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    hired_at = models.DateField(verbose_name="Дата трудоустройства")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name"]

    # Метод для расчета стажа
    @property
    def tenure_days(self):
        from django.utils import timezone
        delta = timezone.now().date() - self.hired_at
        return delta.days

#TODO добавить сбор метрик WorkSession() "10мин простоя-пауза"