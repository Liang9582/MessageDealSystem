from django.db import models
import time

# Create your models here.

class UserInfo(models.Model):
    UserId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, blank=False, verbose_name="用户名")
    password = models.CharField(max_length=32, blank=False, verbose_name="密码")
    Userrank = models.BooleanField(verbose_name="用户等级", default=False)

    class Meta:
        db_table = 'userinfo'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s' % (self.UserId, self.username)

class Material(models.Model):
    material_id = models.CharField(verbose_name='物料编号', max_length=200, primary_key=True)
    material_name = models.CharField(verbose_name='物料名称', max_length=100)
    material_Model_number = models.CharField(verbose_name='物料型号', max_length=100)
    material_describe = models.TextField(verbose_name='物料描述', blank=True)
    material_use = models.TextField(verbose_name='物料用途', blank=True)
    disburse_company = models.CharField(verbose_name='支出公司', max_length=100)

    class Meta:
        db_table = 'material'
        verbose_name = '物料表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s' % (self.material_id, self.material_name)

class Apply_for(models.Model):
    applyforId = models.CharField(verbose_name="申购编号", max_length=200, primary_key=True)
    material_id = models.CharField(verbose_name='物料编号', max_length=200, default=0)
    material_name = models.CharField(verbose_name='物料名称', max_length=100)
    material_Model_number = models.CharField(verbose_name='物料型号', max_length=100)
    material_describe = models.TextField(verbose_name='物料描述', blank=True)
    material_use = models.TextField(verbose_name='物料用途', blank=True)
    material_price = models.DecimalField(verbose_name='物料单价', max_digits=8, decimal_places=2, default=0.00)
    purchase_amount = models.IntegerField(verbose_name='采购数量')
    purchase_price = models.DecimalField(verbose_name='采购金额', max_digits=13, decimal_places=2)
    purchase_people = models.CharField(verbose_name='采购人员', max_length=200, default='')
    is_apply = models.BooleanField(verbose_name='是否提交', default=False)

    class Meta:
        db_table = 'apply_for'
        verbose_name = '申购表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s-%s' % (self.applyforId, self.material_id, self.material_name)

class Purchase(models.Model):
    purchase_number = models.CharField(verbose_name="采购单号", max_length=200, primary_key=True)
    purchase_time = models.DateTimeField(verbose_name="采购时间", default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    material_id = models.CharField(verbose_name='物料编号', max_length=200, default=0)
    material_name = models.CharField(verbose_name='物料名称', max_length=100)
    material_Model_number = models.CharField(verbose_name='物料型号', max_length=100)
    material_describe = models.TextField(verbose_name='物料描述', blank=True)
    material_use = models.TextField(verbose_name='用途描述', blank=True)
    material_price = models.DecimalField(verbose_name='成交单价', max_digits=13, decimal_places=2, default=0.00)
    purchase_amount = models.IntegerField(verbose_name='采购数量')
    purchase_price = models.DecimalField(verbose_name='采购金额', max_digits=13, decimal_places=2)
    purchase_people = models.CharField(verbose_name='采购人', max_length=200, default='')
    disburse_company = models.CharField(verbose_name='支出公司', max_length=100)
    is_active = models.BooleanField(verbose_name='是否已审核', default=False)
    is_putintolib = models.BooleanField(verbose_name="是否入库", default=False)

    class Meta:
        db_table = 'purchase'
        verbose_name = '采购表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s' % (self.purchase_number, self.material_name)


class putintoStorage(models.Model):
    PISnumber = models.CharField(verbose_name="入库编号", primary_key=True, max_length=200)
    PIStime = models.DateTimeField(verbose_name="入库时间", default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    material_id = models.CharField(verbose_name='物料编号', max_length=200, default=0)
    material_name = models.CharField(verbose_name='物料名称', max_length=100)
    material_Model_number = models.CharField(verbose_name='物料型号', max_length=100)
    material_describe = models.TextField(verbose_name='物料描述', blank=True)
    material_use = models.TextField(verbose_name='用途描述', blank=True)
    amount = models.IntegerField(verbose_name="入库数量", default=0)
    PutPeople = models.CharField(verbose_name="送料人员", max_length=200, default="")
    is_putintosttorage = models.BooleanField(verbose_name="是否更新库存", default=False)

    class Meta:
        db_table = 'putIntoStorage'
        verbose_name = "入库记录表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s-%s' % (self.PISnumber, self.material_name, self.PutPeople)


class inventory(models.Model):
    inventory_number = models.CharField(verbose_name="库存编号", max_length=200, primary_key=True)
    material_id = models.CharField(verbose_name='物料编号', max_length=200, default=0)
    material_name = models.CharField(verbose_name='物料名称', max_length=100)
    material_Model_number = models.CharField(verbose_name='物料型号', max_length=100)
    material_describe = models.TextField(verbose_name='物料描述', blank=True)
    material_use = models.TextField(verbose_name='用途描述', blank=True)
    position = models.CharField(verbose_name="库存位置", max_length=200, default='')
    put_in_amount = models.IntegerField(verbose_name="入库数量", default=0)
    out_of_amount = models.IntegerField(verbose_name="出库数量", default=0)
    surplus_amount = models.IntegerField(verbose_name="剩余库存", default=0)

    class Meta:
        db_table = "inventory"
        verbose_name = "库存表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s' % (self.inventory_number, self.material_name)

class receive(models.Model):
    receive_number = models.CharField(verbose_name="领料编号", max_length=200, primary_key=True)
    inventory_number = models.CharField(verbose_name="库存编号", max_length=200, default='')
    material_id = models.CharField(verbose_name='物料编号', max_length=200, default=0)
    material_name = models.CharField(verbose_name='物料名称', max_length=100)
    material_Model_number = models.CharField(verbose_name='物料型号', max_length=100)
    material_describe = models.TextField(verbose_name='物料描述', blank=True)
    material_use = models.TextField(verbose_name='用途描述', blank=True)
    position = models.CharField(verbose_name="库存位置", max_length=200, default='')
    receive_amount = models.IntegerField(verbose_name="领取数量", default=0)
    receive_people = models.CharField(verbose_name="领料人", max_length=200, default='')
    is_submit = models.BooleanField(verbose_name="是否提交", default=False)

    class Meta:
        db_table = "receive"
        verbose_name = "领料表"
        verbose_name_plural = verbose_name

class ApplyOutLib(models.Model):
    apply_number = models.CharField(verbose_name="申请编号", max_length=200, primary_key=True)
    receive_number = models.CharField(verbose_name="领料编号", max_length=200)
    inventory_number = models.CharField(verbose_name="库存编号", max_length=200, default='')
    apply_time = models.DateTimeField(verbose_name="申请时间",
                                       default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    material_id = models.CharField(verbose_name='物料编号', max_length=200, default=0)
    material_name = models.CharField(verbose_name='物料名称', max_length=100)
    material_Model_number = models.CharField(verbose_name='物料型号', max_length=100)
    material_describe = models.TextField(verbose_name='物料描述', blank=True)
    material_use = models.TextField(verbose_name='用途描述', blank=True)
    out_of_amount = models.IntegerField(verbose_name="申请数量", default=0)
    apply_people = models.CharField(verbose_name="申请人员", max_length=200, default="")
    is_agree = models.BooleanField(verbose_name="是否同意", default=False)

    class Meta:
        db_table = "ApplyOutLib"
        verbose_name = "领料申请表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s-%s' % (self.apply_number, self.material_name, self.apply_people)

class out_of_library(models.Model):
    out_of_number = models.CharField(verbose_name="出库编号", max_length=200, primary_key=True)
    receive_number = models.CharField(verbose_name="领料编号", max_length=200, default='')
    inventory_number = models.CharField(verbose_name="库存编号", max_length=200, default='')
    out_of_time = models.DateTimeField(verbose_name="出库时间", default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    material_id = models.CharField(verbose_name='物料编号', max_length=200, default=0)
    material_name = models.CharField(verbose_name='物料名称', max_length=100)
    material_Model_number = models.CharField(verbose_name='物料型号', max_length=100)
    material_describe = models.TextField(verbose_name='物料描述', blank=True)
    material_use = models.TextField(verbose_name='用途描述', blank=True)
    out_of_amount = models.IntegerField(verbose_name="出库数量", default=0)
    material_handler = models.CharField(verbose_name="领料人员", max_length=200, default="")

    class Meta:
        db_table = "outOfLibrary"
        verbose_name = "出库记录表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s-%s-%s' % (self.out_of_number, self.out_of_time, self.material_name, self.material_handler)


