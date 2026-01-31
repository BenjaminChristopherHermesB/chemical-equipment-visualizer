from django.contrib import admin
from .models import EquipmentDataset


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'row_count', 'uploaded_at')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('filename', 'user__username')
    readonly_fields = ('uploaded_at', 'raw_data', 'summary_stats', 'equipment_types')
