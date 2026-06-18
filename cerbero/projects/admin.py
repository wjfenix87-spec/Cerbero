from django.contrib import admin
from .models import Project, ProjectFile, GlobalCounter

@admin.register(GlobalCounter)
class GlobalCounterAdmin(admin.ModelAdmin):
    list_display = ('total_extractions',)
    readonly_fields = ('total_extractions',)

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
