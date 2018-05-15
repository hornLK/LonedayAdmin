from django.contrib import admin
from cmdb import models

# Register your models here.

admin.site.register(models.AssetType)
admin.site.register(models.AssetStatus)
admin.site.register(models.Asset)
admin.site.register(models.CabinetSpec)
admin.site.register(models.Cabinet)
admin.site.register(models.DataCenter)
admin.site.register(models.Tag)
admin.site.register(models.BusinessUnit)
admin.site.register(models.PhysicalServer)
admin.site.register(models.PhysicalNic)
admin.site.register(models.PhysicalDisk)
admin.site.register(models.Switch)
admin.site.register(models.SwitchPort)
admin.site.register(models.CloudOperator)
admin.site.register(models.CloudAccount)
admin.site.register(models.CloudProject)
admin.site.register(models.CloudServer)
admin.site.register(models.CloudNic)
admin.site.register(models.CloudDisk)

