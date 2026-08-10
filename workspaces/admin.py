from django.contrib import admin
from workspaces.models import Workspace

# @admin.register(Workspace)
# class WorkspaceAdmin(admin.ModelAdmin):
    # list_display = ('id','name','description')
    # list_editable = ('title','description')
    # search_fields = ('title',)
    # list_filter = ('categories',)
    # list_display_links = ('id',)
    # filter_horizontal = ('employee',)


admin.site.register(Workspace)
