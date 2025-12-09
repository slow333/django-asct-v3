from django.db import models
from django.contrib.auth.models import User

class SSHInfo(models.Model):
    user = models.ManyToManyField(User)
    
    login_id = models.CharField(max_length=20, null=False)
    ip = models.GenericIPAddressField(null=False)
    port = models.IntegerField(default=22, null=False)
    password = models.TextField(null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'SSH Info: {self.login_id}@{self.ip}:{self.port}'

class ServerInfo(models.Model):
    sshinfo = models.OneToOneField(SSHInfo, on_delete=models.PROTECT)
    
    role_choices = [
        ('web','Web Server'),
        ('was','Web Application Server'),
        ('db', 'Database Server'),
        ('api', 'API Server'),
        ('mgmt', 'Management Server'),
        ('cache', 'Cache Server'),
        ('proxy', 'Proxy Server'),
        ('other', 'Other'),
    ]
    
    hostname = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=50, choices=role_choices, null=False, default='other') # e.g., web server, db server
    role_version = models.CharField(max_length=255, null=False) # apache 2.4.46, mysql 8.0.23
    is_virtual = models.BooleanField(default=False) # 가상서버여부
    is_master = models.BooleanField(default=False) # 마스터서버여부
    
    ip_real = models.GenericIPAddressField(null=False)
    ip_management = models.GenericIPAddressField(null=True, blank=True)
    ip_virtual = models.GenericIPAddressField(null=True, blank=True) # nat, vip 등 가상아이피
    
    os = models.CharField(max_length=255, null=False) # e.g., Ubuntu 20.04, RHEL 7, Windows Server 2019, etc.
    kernel = models.CharField(max_length=255, null=False)
    cpu_core_count = models.IntegerField(null=False)
    total_memory = models.IntegerField(null=False) # GB 단위
    total_disk = models.IntegerField(null=False) # GB 단위
    uptime = models.IntegerField(null=False) # in days
    
    checked_at = models.DateTimeField(null=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.hostname} ({self.ip_real})'

class CPUUsage(models.Model):
    server = models.OneToOneField(ServerInfo, on_delete=models.PROTECT)
    
    def cpu_core_count(self):
        return self.server.cpu_core_count
    usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    
    checked_at = models.DateTimeField(null=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'CPU Usage for {self.server.hostname}'
    
class MemoryUsage(models.Model):
    server = models.OneToOneField(ServerInfo, on_delete=models.PROTECT)
    
    def total_memory(self):
        return self.server.total_memory
    usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    
    checked_at = models.DateTimeField(null=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Memory Usage for {self.server.hostname}'

class DiskUsage(models.Model):
    server = models.OneToOneField(ServerInfo, on_delete=models.PROTECT)
    
    storage_local_total = models.IntegerField(null=False) 
    storage_local_usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    
    storage_san_total = models.IntegerField(null=True, blank=True)
    storage_san_usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    storage_nfs_total = models.IntegerField(null=True, blank=True)
    storage_nfs_usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    checked_at = models.DateTimeField(null=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Disk Usage for {self.server.hostname}'

class NetworkUsage(models.Model):
    server = models.OneToOneField(ServerInfo, on_delete=models.PROTECT)
    
    network_type = [
        ('100M','100M'),('1G','1G'), ('10G','10G'), ('40G','40G'), ('100G','100G'), 
        ('8G','8G FC'), ('16G','16G FC'), ('32G','32G FC'), ('64G','64G FC')]
    network_local_1 = models.CharField(max_length=10, choices=network_type, default='10G', null=False)
    network_local_1_inbound = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    network_local_1_outbound = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    
    network_local_2 = models.CharField(max_length=10, choices=network_type, default='10G', null=True, blank=True)
    network_local_2_inbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    network_local_2_outbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    network_nas_1 = models.CharField(max_length=10, choices=network_type, default='10G', null=True, blank=True)
    network_nas_1_inbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    network_nas_1_outbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    network_nas_2 = models.CharField(max_length=10, choices=network_type, default='10G', null=True, blank=True)
    network_nas_2_inbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    network_nas_2_outbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    network_san_1 = models.CharField(max_length=10, choices=network_type, default='16G', null=True, blank=True)
    network_san_1_inbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    network_san_1_outbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    network_san_2 = models.CharField(max_length=10, choices=network_type, default='16G', null=True, blank=True)
    network_san_2_inbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    network_san_2_outbound = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    network_mgmt_1 = models.CharField(max_length=20, choices=network_type, default='1G', null=False)
    network_mgmt_2 = models.CharField(max_length=20, choices=network_type, default='1G', null=True, blank=True)
    
    checked_at = models.DateTimeField(null=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Network Usage for {self.server.hostname}'

class SysctlSetting(models.Model):
    server = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    parameter = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False)
    
    checked_at = models.DateTimeField(null=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Sysctl {self.parameter}: {self.value} for {self.server.hostname}'

class SystemLog(models.Model):
    server = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    log_level_choices = [
        ('DEBUG','DEBUG'),('INFO','INFO'), ('WARNING','WARNING'), ('ERROR','ERROR'), ('CRITICAL','CRITICAL')]
    
    log_level = models.CharField(max_length=10, choices=log_level_choices, null=False, default='ERROR')
    message = models.TextField(null=False)
    
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Log from {self.server.hostname} at {self.recorded_at}'
