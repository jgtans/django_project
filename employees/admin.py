from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Employee, EmployeePhoto, EmployeeSkill, Skill


class EmployeePhotoInline(admin.TabularInline):
    model = EmployeePhoto
    extra = 1
    fields = ("image", "order")
    ordering = ("order",)


class EmployeeSkillInline(admin.TabularInline):
    """Навыки редактируются прямо на странице сотрудника."""

    model = EmployeeSkill
    extra = 1
    autocomplete_fields = ("skill",)  # удобный автодополнитель


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "role",
        "gender",
        "hired_at",
        "tenure_days",
        "workspace",
    )
    list_filter = ("role", "gender", "workspace")
    search_fields = ("last_name", "first_name")
    list_display_links = ("last_name", "first_name")
    autocomplete_fields = ("workspace",)
    inlines = [EmployeeSkillInline, EmployeePhotoInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
