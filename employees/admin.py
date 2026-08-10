from django.contrib import admin

from .models import Employee, EmployeeSkill, Skill


class EmployeeSkillInline(admin.TabularInline):
    """Навыки редактируются прямо на странице сотрудника."""

    model = EmployeeSkill
    extra = 1
    autocomplete_fields = ("skill",)  # удобный автодополнитель


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "gender",
        "hired_at",
        "tenure_days",
        "workspace",
    )
    list_filter = ("gender", "workspace")
    search_fields = ("last_name", "first_name")
    list_display_links = ("last_name", "first_name")
    autocomplete_fields = ("workspace",)
    inlines = [EmployeeSkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
