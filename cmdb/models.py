from django.db import models
#from accounts.models import UserInfo

# Create your models here.

#资产状态表 -- 上线--下线--维护等状态
class AssetStatus(models.Model):
    state_name = models.CharField(max_length=64,unique=True,blank=True)
    describe = models.TextField("备注",null=True,blank=True)

    def __str__(self):
        return "状态: %s" % self.state_name

    class Meta:
        verbose_name_plural = "状态表"
        verbose_name = "状态表"

#资产类型 -- 物理机，虚拟机、云主机、软件
class AssetType(models.Model):
    asset_type_name =models.CharField(max_length=128,unique=True,blank=True)
    describe = models.TextField("备注",null=True,blank=True)

    def __str__(self):
        return "资产类型: %s" % self.asset_type_name

    class Meta:
        verbose_name = "资产类型"
        verbose_name_plural = "资产类型"

#标签--通过标签更好的标注主机信息
class Tag(models.Model):
    tag_name = models.CharField(max_length=128,unique=True,blank=True)
    describe = models.TextField("备注",blank=True)

    def __str__(self):
        return '标签: %s' % self.tag_name
    class Meta:
        verbose_name = "标签信息"
        verbose_name_plural = "标签信息"

#数据中心信息---主要是物理用到该表
class DataCenter(models.Model):
    datacenter_name = models.CharField("显示名字",max_length=64)
    addr = models.CharField("数据中心地址",max_length=255,blank=True)
    tel = models.CharField("数据中心电话",max_length=20,blank=True,null=True)
    contact = models.CharField("销售/客户经理",max_length=20,null=True,blank=True)
    contact_phone = models.CharField("销售/客户经理电话",max_length=20,null=True,blank=True)
    bandwith = models.CharField("带宽",max_length=30,null=True,blank=True)
    describe = models.TextField("备注",blank=True,null=True)

    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)


    def __str__(self):
        return "数据中心: %s" % self.datacenter_name

    class Meta:
        verbose_name = "数据中心信息"
        verbose_name_plural = "数据中心信息"

#机柜规格表，标注机柜的电源插座类型，以及U数
class CabinetSpec(models.Model):
    CurrentType_Choices = (
        ("1","国标"),
        ("2","欧标")
    )
    cabinet_spec_name = models.CharField("机柜规格",max_length=64,blank=True)
    u_num = models.IntegerField("机柜U数",blank=True,default=42)
    current_type = models.CharField("电源插头类型",max_length=32,choices=CurrentType_Choices,blank=True)

    def __str__(self):
        return "机柜规格-U数: %s-%d" % (self.cabinet_spec_name,self.u_num)

    class Meta:
        verbose_name = "机柜规格信息"
        verbose_name_plural = "机柜规格信息"

#机柜信息表
class Cabinet(models.Model):
    cabinet_num = models.CharField("机柜号",max_length=30,null=True,blank=True)
    cabinet_spec = models.ForeignKey('CabinetSpec',null=True,on_delete=models.SET_NULL)
    asset = models.OneToOneField('Asset',null=True,on_delete=models.SET_NULL)
    datacenter = models.ForeignKey('DataCenter',null=True,on_delete=models.SET_NULL)

    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)


    def __str__(self):
        return "机柜信息: %s-%s" % (self.datacenter.datacenter_name,self.cabinet_num)

    class Meta:
        verbose_name = "机柜信息"
        verbose_name_plural = "机柜信息"

#产品线
class BusinessUnit(models.Model):
    business_name = models.CharField('业务线',max_length=64,unique=True,db_index=True)
    contact = models.ManyToManyField('accounts.UserInfo',verbose_name="负责人",null=True,blank=True)
    describe = models.TextField("备注",blank=True,null=True)

    def __str__(self):
        return self.business_name

    class Meta:
        verbose_name = "产品线信息"
        verbose_name_plural = "产品线信息"

#资产总表
class Asset(models.Model):
    asset_id = models.CharField('资产号',max_length=128,unique=True,db_index=True,blank=True,null=True)
    asset_type = models.ForeignKey(to='AssetType',null=True,blank=True,on_delete=models.SET_NULL)
    asset_status = models.ForeignKey(to='AssetStatus',null=True,blank=True,on_delete=models.SET_NULL)
    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)

    class Meta:
        verbose_name = "资产总表"
        verbose_name_plural = "资产总表"

#物理服务器表
class PhysicalServer(models.Model):
    ManuFactory_Choice ={
        ("1","戴尔"),
        ("2","IBM"),
        ("3","联想"),
        ("4","浪潮")
    }
    asset = models.OneToOneField("Asset",null=True,on_delete=models.SET_NULL)
    hostname = models.CharField(max_length=128,blank=True,null=True)
    sn = models.CharField('快速服务编号',max_length=128,db_index=True,blank=True,null=True)
    manufactory = models.CharField(verbose_name="厂商",max_length=128,null=True,blank=True)
    model = models.CharField("型号",max_length=128,null=True,blank=True)
    business_unit = models.ForeignKey('BusinessUnit',null=True,on_delete=models.SET_NULL)
    tag = models.ManyToManyField('Tag',null=True,blank=True)

    cabinet_num = models.ForeignKey('Cabinet',verbose_name="机柜",null=True,on_delete=models.SET_NULL)
    cabinet_order = models.CharField('机柜中的位置',max_length=32,null=True,blank=True)

    manage_ip = models.GenericIPAddressField(protocol="IPv4",verbose_name="管理IP",null=True,blank=True)
    business_ip = models.GenericIPAddressField(protocol="IPv4",verbose_name="业务IP",null=True,blank=True)

    os_platform = models.CharField('操作系统',max_length=64,null=True,blank=True)

    cpu_logic_count = models.IntegerField(null=True,blank=True)
    cpu_physical_count = models.IntegerField(null=True,blank=True)
    cpu_model = models.CharField(max_length=128,null=True,blank=True)

    memory_total = models.IntegerField(null=True,blank=True)

    purchase_time = models.DateTimeField("采购时间",blank=True,null=True)
    guarantee_repair_time = models.DateTimeField("保修时间",blank=True,null=True)

    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)

    describe = models.TextField(blank=True,null=True)
    class Meta:
        verbose_name = "物理服务器表"
        verbose_name_plural = "物理服务器表"
        index_together = ["sn","asset"]

    def __str__(self):
        return "物理服务器: %s-SN:%s" % (self.hostname,self.sn)

#物理机网卡信息
class PhysicalNic(models.Model):
    nic_name = models.CharField("网卡名",max_length=128,blank=True)
    hwaddr = models.CharField("网卡MAC",max_length=128,blank=True,null=True)
    up = models.BooleanField(default=False)
    netmask = models.CharField(max_length=64,blank=True,null=True)
    ipaddr = models.GenericIPAddressField(protocol="IPv4",verbose_name="管理IP",null=True,blank=True)

    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)

    server = models.ForeignKey("PhysicalServer",null=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "物理机网卡部件信息"
        verbose_name_plural = "物理机网卡部件信息"

    def __str__(self):
        return "网卡: %s --> MAC: %s;IP: %s;up:%s" % (self.nic_name,self.hwaddr,self.ipaddr,self.up)

#物理机硬盘信息
class PhysicalDisk(models.Model):
    disk_name = models.CharField("硬盘名",max_length=32,blank=True,null=True)
    disk_size = models.CharField("硬盘大小",max_length=32,blank=True,null=True)
    disk_type = models.CharField("硬盘类型",max_length=32,blank=True,null=True)

    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)

    server = models.ForeignKey("PhysicalServer",null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return "name: %s-type: %s-size: %s" % (self.disk_name,self.disk_type,self.disk_size)

    class Meta:
        verbose_name = "物理机硬盘信息"
        verbose_name_plural = "物理机硬盘信息"
#交换机表
class Switch(models.Model):
    switch_name = models.CharField("交换机名",max_length=32,db_index=True,unique=True,blank=True)
    asset = models.OneToOneField("Asset",null=True,on_delete=models.SET_NULL)
    sn = models.CharField("快速服务编码",max_length=32,blank=True,null=True)
    manufactory = models.CharField("厂商",max_length=32,blank=True,null=True)
    model = models.CharField("型号",max_length=32,blank=True,null=True)
    memory_total = models.CharField("内存",max_length=32,blank=True,null=True)

    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)

    def __str__(self):
        return "交换机: %s-%s" % (self.switch_name,model)
    class Meta:
        verbose_name = "交换机信息"
        verbose_name_plural = "交换机信息"


#交换机端口表
class SwitchPort(models.Model):
    port_name = models.CharField("端口名",max_length=32,blank=True,null=True)
    port_mac = models.CharField("端口mac",max_length=64,blank=True,null=True)
    study_mac = models.CharField("学习mac",max_length=64,blank=True,null=True)
    up = models.BooleanField("是否活动",default=False)

    switch = models.ForeignKey('Switch',on_delete=models.CASCADE)

    def __str__(self):
        return "端口: %s;%s;%s" % (self.switch.switch_name,self.port_name,self.up)

    class Meta:
        verbose_name = "交换机端口信息"
        verbose_name_plural = "交换机端口信息"

#云平台信息
class CloudOperator(models.Model):
    cloud_name = models.CharField("云平台",max_length=32,unique=True,blank=True,null=True)
    describe = models.TextField("备注",null=True,blank=True)

    def __str__(self):
        return "云平台: %s " % self.cloud_name

    class Meta:
        verbose_name = "云平台"
        verbose_name_plural = "云平台"

#云平台账号
class CloudAccount(models.Model):
    cloud_account = models.CharField("账号",max_length=32,blank=True,null=True)
    describe = models.TextField("备注",null=True,blank=True)
    cloud = models.ForeignKey("CloudOperator",verbose_name="所属云",on_delete=models.CASCADE)

    def __str__(self):
        return "云平台: %s-账号: %s" % (self.cloud.cloud_name,self.cloud_account)

    class Meta:
        verbose_name = "云平台账号"
        verbose_name_plural = "云平台账号"

#云平台上的项目
class CloudProject(models.Model):
    project_name = models.CharField("项目名",max_length=32,blank=True,null=True,db_index=True)
    cloud_account = models.ForeignKey("CloudAccount",verbose_name="所属云账号",on_delete=models.CASCADE)
    describe = models.TextField("备注",null=True,blank=True)

    def __str__(self):
        return "云平台: %s-账号: %s-项目: %s" % (self.cloud_account.cloud.cloud_name,self.cloud_account.cloud_account,self.project_name)

    class Meta:
        verbose_name = "云平台项目"
        verbose_name_plural = "云平台项目"

#云主机表
class CloudServer(models.Model):
    asset=models.OneToOneField('Asset',null=True,blank=True,on_delete=models.SET_NULL)
    hostname = models.CharField("主机名",max_length=64,null=True,blank=True,db_index=True,unique=True)
    uuid = models.CharField("云主机uuid",max_length=128,null=True,blank=True,unique=True)
    cloud_project = models.ForeignKey("CloudProject",verbose_name="所属项目",on_delete=models.SET_NULL,null=True,blank=True) 
    cloud = models.ForeignKey("CloudOperator",verbose_name="所属云",on_delete=models.SET_NULL,null=True,blank=True)

    inner_ip = models.GenericIPAddressField(protocol="IPv4",verbose_name="内网IP",null=True,blank=True)
    float_ip = models.GenericIPAddressField(protocol="IPv4",verbose_name="浮动IP",null=True,blank=True)

    os_platform = models.CharField("操作系统",max_length=32,null=True,blank=True)

    vcpu = models.IntegerField(null=True,blank=True)
    memory_total = models.CharField(max_length=32,null=True,blank=True)

    money = models.CharField(max_length=32,null=True,blank=True)

    create_at = models.DateTimeField(blank=True,null=True)
    update_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return "云平台: %s-项目: %s-云主机: %s" % (self.cloud.cloud_name,self.cloud_project.project_name,self.hostname)

    class Meta:
        verbose_name = "云主机信息"
        verbose_name_plural = "云主机信息"

#云主机网卡
class CloudNic(models.Model):
    nic_name = models.CharField("网卡名",max_length=64,blank=True)
    netmask = models.CharField("掩码",max_length=64,blank=True)
    ipaddr = models.GenericIPAddressField(protocol="IPv4",null=True,blank=True)

    cloud_server = models.ForeignKey('CloudServer',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return "云主机: %s-网卡: %s" % (self.cloud_server.hostname,self.nic_name)
    class Meta:
        verbose_name = "云主机网卡信息"
        verbose_name_plural = "云主机网卡信息"

#云硬盘
class CloudDisk(models.Model):
    disk_name = models.CharField("云硬盘",max_length=64,blank=True,null=True)
    disk_uuid = models.CharField("云硬盘uuid",max_length=128,blank=True,null=True)
    disk_size = models.CharField("云硬盘空间",max_length=32,blank=True,null=True)

    cloud_server = models.ForeignKey('CloudServer',null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return "云主机: %s-云盘: %s" % (self.cloud_server.hostname,self.disk_name)
    class Meta:
        verbose_name = "云主机磁盘信息"
        verbose_name_plural = "云主机磁盘信息"

