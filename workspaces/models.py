from django.db import models


class Workspace(models.Model):
    number = models.CharField(max_length=10, verbose_name="Номер")
    floor = models.IntegerField(verbose_name="Этаж")
    workspace_type = models.CharField(max_length=50, verbose_name="Тип")

    class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = "Рабочее место"

    def __str__(self):
        return f"Рабочее место {self.number}, этаж {self.floor}"

