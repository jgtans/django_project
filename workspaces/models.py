from django.db import models

from django.db import models


class Workspace(models.Model):
    number = models.CharField(max_length=10, verbose_name="Номер")
    floor = models.IntegerField(verbose_name="Этаж")
    workspace_type = models.CharField(max_length=50, verbose_name="Тип")

    def __str__(self):
        return f"Рабочее место {self.number}, этаж {self.floor}"
