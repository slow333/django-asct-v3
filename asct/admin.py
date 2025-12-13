from django.contrib import admin
from .models import SSHInfo, ServerInfo, CPUUsage, MemoryUsage, DiskUsage, NetworkUsage, SysctlSetting, SystemLog

class ServerInfoInline(admin.StackedInline):
    model = ServerInfo
    extra = 0

@admin.register(SSHInfo)
class SSHInfoAdmin(admin.ModelAdmin):
    list_display = ('get_users','login_id', 'ip', 'port', 'created_date',)
    search_fields = ('login_id', 'ip')
    inlines = [ServerInfoInline]
    filter_horizontal = ('user',)

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.user.all()])
    get_users.short_description = 'Users'

    def created_date(self, obj):
        return obj.created_at.date()
    created_date.short_description = 'Created At'
    created_date.admin_order_field = 'created_at'

@admin.register(ServerInfo)
class ServerInfoAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'role', 'os','cpu_core_count', 'total_memory', 'total_disk', 'ip_real', 'is_virtual', 'is_master', 'checked_at', 'is_confirmed')
    search_fields = ('hostname', 'ip_real', 'role')
    list_filter = ('role', 'is_virtual', 'is_master', 'is_confirmed')
    date_hierarchy = 'checked_at'
    ordering = ('hostname','-checked_at',)

@admin.register(CPUUsage)
class CPUUsageAdmin(admin.ModelAdmin):
    list_display = ('server__hostname', 'usage_percent', 'timestamp')
    search_fields = ('server__hostname','usage_percent')
    ordering = ('server__hostname','-timestamp')

@admin.register(MemoryUsage)
class MemoryUsageAdmin(admin.ModelAdmin):
    list_display = ('server__hostname', 'usage_percent', 'timestamp')
    search_fields = ('server__hostname','usage_percent')
    ordering = ('server__hostname','-timestamp')

@admin.register(DiskUsage)
class DiskUsageAdmin(admin.ModelAdmin):
    list_display = ('server__hostname', 'storage_local_usage_percent', 'timestamp')
    search_fields = ('server__hostname',)
    ordering = ('server__hostname','-timestamp')

@admin.register(NetworkUsage)
class NetworkUsageAdmin(admin.ModelAdmin):
    list_display = ('server__hostname', 'network_service','network_service_inbound', 'network_service_outbound', 'timestamp')
    search_fields = ('server__hostname',)
    ordering = ('server__hostname','-timestamp')

@admin.register(SysctlSetting)
class SysctlSettingAdmin(admin.ModelAdmin):
    list_display = ('server__hostname', 'parameter', 'value', 'checked_at')
    search_fields = ('server__hostname', 'parameter')
    ordering = ('server__hostname','parameter','-checked_at')

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('server__hostname', 'log_level', 'log_message', 'checked_at')
    search_fields = ('server__hostname', 'log_message')
    ordering = ('server__hostname','-checked_at')