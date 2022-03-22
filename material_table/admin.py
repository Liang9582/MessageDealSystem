from django.contrib import admin
from .models import Material, Apply_for, Purchase, putintoStorage, inventory, out_of_library, UserInfo

# Register your models here.

class UserInfoManager(admin.ModelAdmin):
    list_display = ['UserId', 'username', 'password', 'Userrank']
    list_display_links = ['UserId']
    list_filter = ['Userrank']
    search_fields = ['username']
    list_editable = ['username', 'password', 'Userrank']

admin.site.register(UserInfo, UserInfoManager)


class MaterialManager(admin.ModelAdmin):
    # 列表页显示哪些字段的列
    list_display = ['material_id', 'material_name', 'material_Model_number', 'material_describe', 'material_use',
                    'disburse_company']
    # 控制list_display中的字段， 哪些可以链接到修改页
    list_display_links = ['material_id']
    # 添加过滤器
    list_filter = ['material_name']
    # 添加搜索框[模糊查询]
    search_fields = ['material_id', 'material_name']
    #添加可在列表页编辑的字段
    list_editable = ['material_name', 'material_Model_number', 'material_describe', 'material_use',
                    'disburse_company']


admin.site.register(Material, MaterialManager)


class Apply_forManager(admin.ModelAdmin):
    list_display = ['applyforId', 'material_id', 'material_name', 'material_Model_number', 'material_describe', 'material_use',
                    'material_price', 'purchase_amount', 'purchase_price', 'purchase_people', 'is_apply']
    # 控制list_display中的字段， 哪些可以链接到修改页
    list_display_links = ['applyforId']
    # 添加过滤器
    list_filter = ['material_name',  'purchase_people', 'is_apply']
    # 添加搜索框[模糊查询]
    search_fields = ['material_name', 'purchase_people']
    # 添加可在列表页编辑的字段
    list_editable = ['material_id', 'material_price', 'purchase_amount', 'purchase_price', 'purchase_people', 'is_apply']

admin.site.register(Apply_for, Apply_forManager)


class PurchaseManager(admin.ModelAdmin):
    list_display = ['purchase_number', 'purchase_time', 'material_name', 'material_Model_number', 'material_describe',
                    'material_use', 'material_price', 'purchase_amount', 'purchase_price', 'purchase_people', 'disburse_company', 'is_active']
    # 控制list_display中的字段， 哪些可以链接到修改页
    list_display_links = ['purchase_number']
    # 添加过滤器
    list_filter = ['material_name', 'disburse_company', 'purchase_people', 'is_active']
    # 添加搜索框[模糊查询]
    search_fields = ['purchase_number', 'material_name', 'purchase_people']

admin.site.register(Purchase, PurchaseManager)


class putintoStorageManager(admin.ModelAdmin):
    list_display = ['PISnumber', 'PIStime', 'material_name', 'material_Model_number',
                    'material_describe', 'material_use', 'amount', 'PutPeople']
    # 控制list_display中的字段， 哪些可以链接到修改页
    list_display_links = ['PISnumber']
    # 添加过滤器
    list_filter = ['material_name', 'PutPeople']
    # 添加搜索框[模糊查询]
    search_fields = ['PISnumber', 'material_name']
    # 添加可在列表页编辑的字段
    list_editable = ['material_name', 'material_Model_number', 'material_describe', 'material_use', 'amount', 'PutPeople']

admin.site.register(putintoStorage, putintoStorageManager)


class inventoryManager(admin.ModelAdmin):
    list_display = ['inventory_number', 'material_id', 'material_name', 'material_Model_number', 'material_describe',
                    'material_use', 'put_in_amount', 'out_of_amount', 'surplus_amount']
    # 控制list_display中的字段， 哪些可以链接到修改页
    list_display_links = ['inventory_number']
    # 添加过滤器
    list_filter = ['material_name']
    # 添加搜索框[模糊查询]
    search_fields = ['inventory_number', 'material_name', 'material_id']

admin.site.register(inventory, inventoryManager)

class out_of_libraryManager(admin.ModelAdmin):
    list_display = ['out_of_number', 'out_of_time', 'material_name', 'material_Model_number', 'material_describe',
                    'material_use', 'out_of_amount', 'material_handler']
    # 控制list_display中的字段， 哪些可以链接到修改页
    list_display_links = ['out_of_number']
    # 添加过滤器
    list_filter = ['material_name']
    # 添加搜索框[模糊查询]
    search_fields = ['material_handler', 'material_name']
    list_editable = ['material_name', 'material_Model_number', 'material_handler', 'out_of_amount']

admin.site.register(out_of_library, out_of_libraryManager)