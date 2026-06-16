from django.contrib import admin
from .models import Project, ProjectFile, ExtractionLog

@admin.register(ExtractionLog)
class ExtractionLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'file_count')
    list_filter = ('created_at',)
    readonly_fields = ('file_count', 'created_at')

    def has_add_permission(self, request):
        return False  # Los logs se crean solos, no manualmente
