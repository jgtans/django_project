from django.contrib import admin

from .models import Workspace


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("number", "floor", "workspace_type")
    search_fields = ("floor", "workspace_type")
    list_filter = ("number",)
    list_display_links = ("number",)
