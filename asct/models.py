from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SSHInfo(models.Model):
    user = models.ManyToManyField(User)
    
    login_id = models.CharField(max_length=20, null=False)
    ip = models.GenericIPAddressField(null=False)
    port = models.IntegerField(default=22, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    
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
    role = models.CharField(max_length=10, choices=role_choices, null=False, default='other') # e.g., web server, db server
    role_version = models.CharField(max_length=255, null=False) # apache 2.4.46, mysql 8.0.23
    
    ip_real = models.GenericIPAddressField(null=False)
    
    os = models.CharField(max_length=255, null=False) # e.g., Ubuntu 20.04, RHEL 7, Windows Server 2019, etc.
    kernel = models.CharField(max_length=255, null=False)
    cpu_core_count = models.IntegerField(null=False)
    total_memory = models.IntegerField(null=False) # GB 단위
    total_disk = models.IntegerField(null=False) # GB 단위
    uptime = models.IntegerField(null=False) # in days
    
    is_virtual = models.BooleanField(default=True, null=False) # 가상서버여부
    is_master = models.BooleanField(default=True, null=False) # 마스터서버여부
    
    checked_at = models.DateTimeField(default=timezone.now)
    
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'{self.hostname} ({self.ip_real})'
    
    class Meta:
        ordering = ['hostname','-checked_at']
        unique_together = ('hostname','ip_real', 'checked_at')

class CPUUsage(models.Model):
    server = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    
    checked_at = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(default=timezone.now, null=False)
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def cpu_core_count(self):
        return self.server.cpu_core_count
    
    def __str__(self) -> str:
        return f'CPU Usage for {self.server.hostname}'
    
    class Meta:
        ordering = ['server__hostname','-timestamp']
        unique_together = ('server','timestamp')

class MemoryUsage(models.Model):
    server = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    def total_memory(self):
        return self.server.total_memory
    usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    
    checked_at = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(default=timezone.now, null=False)
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'Memory Usage for {self.server.hostname}'
    
    class Meta:
        ordering = ['server__hostname','-timestamp']
        unique_together = ('server', 'timestamp')

class DiskUsage(models.Model):
    server = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    storage_local_total = models.IntegerField(null=False) 
    storage_local_usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    
    checked_at = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(default=timezone.now, null=False)
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'Disk Usage for {self.server.hostname}'
    
    class Meta:
        ordering = ['server__hostname','-timestamp']
        unique_together = ('server', 'timestamp')

class NetworkUsage(models.Model):
    server = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    network_type = [
        ('100M','100M'),('1G','1G'), ('10G','10G'), ('40G','40G'), ('100G','100G'), 
        ('8G','8G FC'), ('16G','16G FC'), ('32G','32G FC'), ('64G','64G FC')]
    network_service = models.CharField(max_length=10, choices=network_type, default='10G', null=False)
    network_service_inbound = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    network_service_outbound = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    
    checked_at = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(default=timezone.now, null=False)
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Network Usage for {self.server.hostname}'
    
    class Meta:
        ordering = ['server__hostname','-timestamp']
        unique_together = ('server', 'timestamp')

class SysctlSetting(models.Model):
    server = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    parameter = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False)
    
    checked_at =models.DateTimeField(default=timezone.now)
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'Sysctl {self.parameter}: {self.value} for {self.server.hostname}'
    
    class Meta:
        ordering = ['server','-checked_at']
        unique_together = ('server','checked_at',)

class SystemLog(models.Model):
    server = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    log_level_choices = [
        ('DEBUG','DEBUG'),('INFO','INFO'), ('WARNING','WARNING'), ('ERROR','ERROR'), ('CRITICAL','CRITICAL')]
    
    log_level = models.CharField(max_length=10, choices=log_level_choices, null=False, default='ERROR')
    log_message = models.TextField(null=False)
    
    checked_at = models.DateTimeField(default=timezone.now)
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def save(self, *args, **kwargs):
        # log_message에 'error' 또는 'info'가 포함된 경우에만 저장합니다.(개발시는 info 등도 저장 가능)
        if 'error' in self.log_message.lower() or 'info' in self.log_message.lower():
            super().save(*args, **kwargs)
        # 'error' 또는 'info'가 없으면 아무 작업도 하지 않아 저장을 건너뜁니다.

    def __str__(self) -> str:
        return f'Log from {self.server.hostname} at {self.checked_at}'
    
    class Meta:
        ordering = ['server','-checked_at']
        unique_together = ('server', 'checked_at')
