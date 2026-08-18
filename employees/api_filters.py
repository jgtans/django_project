import datetime

import django_filters
from django.utils import timezone

from .models import Employee


class EmployeeFilterSet(django_filters.FilterSet):
    # Фильтрация по навыку через связь (K3)
    skill = django_filters.CharFilter(
        field_name="employeeskill_set__skill__name", lookup_expr="iexact"
    )
    # Фильтрация по стажу через дату приёма (K3)
    tenure_gte = django_filters.NumberFilter(method="filter_tenure_gte")
    tenure_lte = django_filters.NumberFilter(method="filter_tenure_lte")

    class Meta:
        model = Employee
        fields = ["role", "skill", "tenure_gte", "tenure_lte"]

    def filter_tenure_gte(self, queryset, name, value):
        cutoff = timezone.localdate() - datetime.timedelta(days=int(value))
        return queryset.filter(hired_at__lte=cutoff)

    def filter_tenure_lte(self, queryset, name, value):
        cutoff = timezone.localdate() - datetime.timedelta(days=int(value))
        return queryset.filter(hired_at__gte=cutoff)
