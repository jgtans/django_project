from django.db import models


class Workspace(models.Model):
    number = models.CharField(max_length=10, verbose_name="Номер")
    floor = models.IntegerField(verbose_name="Этаж")
    workspace_type = models.CharField(max_length=50, verbose_name="Тип")

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочее место"

    def __str__(self):
        return f"Рабочее место {self.number}, этаж {self.floor}"

    @property
    def number_int(self):
        """'A-101' > 101; 'A-202' > 202. Если цифр нет, то None"""
        digits = "".join(ch for ch in self.number if ch.isdigit())
        return int(digits) if digits else None

    def neighbors(self):
        """Все столбцы на том же этаже, кроме текущего"""
        return Workspace.objects.filter(floor=self.floor).exclude(pk=self.pk)
