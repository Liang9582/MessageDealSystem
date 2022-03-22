from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from . import models
import time
import hashlib

# Create your views here.

def home(request):
    if request.method =="GET":
        return render(request, "home.html")
    else:
        name = request.POST.get("username", None)
        pwd = request.POST.get("password", None)
        rank = request.POST.get('rank', None)
        # 获取数据库中的账号密码数据
        if rank == 'on':
            rank = 1
        else:
            rank = 0
        s = models.UserInfo.objects.get(username=name)
        if s.password == pwd:
            emp = models.UserInfo.objects.filter(username=name, password=pwd, Userrank=rank)
        elif s.password == setPassword(pwd):
            emp = models.UserInfo.objects.filter(username=name, password=setPassword(pwd), Userrank=rank)
        else:
            emp = models.UserInfo.objects.filter(username=name, password=pwd, Userrank=rank)

        if emp.count() == 0:
            return render(request, "home.html", {"msg": "登录失败"})
        else:
            response = HttpResponseRedirect("/welcome")
            response.set_cookie('login_name', name)
            response.set_cookie('rank', rank)
            return response

def setPassword(password):
    """
    加密密码，算法单次md5
    :param apssword: 传入的密码
    :return: 加密后的密码
    """
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        password1 = data.get("password1")
        emp = models.UserInfo.objects.filter(username=username)
        if emp.count() != 0:
            return render(request, 'register.html', {'err': "该用户已存在，请重新注册"})
        elif password != password1:
            return render(request, 'register.html', {'err': "两次密码不一致，请重新输入"})
        else:
            user = models.UserInfo()
            user.username = username
            user.password = setPassword(password)
            user.save()
            return render(request, 'register.html', {'success': "注册成功"})

def update_password(request):
    if request.method == 'GET':
        name = request.COOKIES.get('login_name')
        return render(request, 'user/update_password.html', {'name': name})
    else:
        list = ['username', 'password', 'password1']
        info = []
        for li in list:
            info.append(request.POST.get(li))

        user = models.UserInfo.objects.get(username=info[0])
        if info[1] != info[2]:
            return render(request, 'user/update_password.html', {'name': info[0], 'err': "两次密码输入不一致，请重新输入"})
        else:
            user.password = setPassword(info[1])
            user.save()
            return render(request, 'user/update_password.html', {'name': info[0], 'success': "修改成功"})


def welcome(request):
    if request.method == 'GET':
        name = request.COOKIES.get('login_name')
        material_message = models.Material.objects.all()
        return render(request, 'welcome.html', {"materials": material_message, "name": name})

def update_material(request):
    if request.method == 'GET':
        material_id = request.GET.get('id')
        material = models.Material.objects.get(material_id=material_id)
        name = request.COOKIES.get('login_name')
        return render(request, 'materials/update_material.html', {"material": material, "name": name})
    else:
        list = ['material_id', 'material_name', 'material_Model_number', 'material_describe', 'material_use', 'disburse_company']
        info = []
        for li in list:
            info.append(request.POST.get(li))

        info[0] = request.GET.get('id')
        m_msg = models.Material()
        m_msg.material_id = info[0]
        m_msg.material_name = info[1]
        m_msg.material_Model_number = info[2]
        m_msg.material_describe = info[3]
        m_msg.material_use = info[4]
        m_msg.disburse_company = info[5]
        m_msg.save()

        name = request.COOKIES.get('login_name')
        return render(request, 'materials/update_material.html', {'success': "物料信息修改成功！", 'material': m_msg, 'name': name})

def add_material(request):
    if request.method == 'GET':
        name = request.COOKIES.get('login_name')
        return render(request, 'materials/add_material.html', {'name': name})
    else:
        list = ['material_id', 'material_name', 'material_Model_number', 'material_describe', 'material_use',
                'disburse_company']
        info = []
        for li in list:
            info.append(request.POST.get(li))
        id = request.POST.get('material_id', None)
        if id.isspace() == True:
            return render(request, 'materials/add_material.html', {'err': '物料型号不能为空格组成,请重新输入！'})
        s = models.Material.objects.filter(material_id=info[0])
        if s.count() != 0:
            return render(request, 'materials/add_material.html', {'err': "此物料编号已经存在， 请重新编写物料编号"})
        m_msg = models.Material()
        m_msg.material_id = info[0]
        m_msg.material_name = info[1]
        m_msg.material_Model_number = info[2]
        m_msg.material_describe = info[3]
        m_msg.material_use = info[4]
        m_msg.disburse_company = info[5]
        m_msg.save()

        name = request.COOKIES.get('login_name')
        return render(request, 'materials/add_material.html', {'success': "物料信息添加成功！", 'name': name})

def delete_material(request):
    id = request.GET.get('id')
    if models.Material.objects.get(material_id=id).delete():
        return redirect('/welcome/')
    else:
        return redirect('/welcome/')

def my_applyFors(request):
    if request.method == 'GET':
        applyfors = models.Apply_for.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyFor/applyFors.html', {'applyfors': applyfors, 'name': name})

def add_applyFors(request):
    if request.method == 'GET':
        materials = models.Material.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyFor/add_applyFors.html', {'materials': materials, 'name': name})
    else:
        applyforId = request.POST.get('applyforId', None)
        s = models.Apply_for.objects.filter(applyforId=applyforId)
        material_price = request.POST.get('material_price', None)
        purchase_amount = request.POST.get('purchase_amount', None)
        if material_price == None or purchase_amount == None:
            materials = models.Material.objects.all()
            name = request.COOKIES.get('login_name')
            return render(request, 'applyFor/add_applyFors.html', {'materials': materials, 'err': '物料单价和采购数量不能为空', 'name': name})
        elif s.count() != 0:
            materials = models.Material.objects.all()
            name = request.COOKIES.get('login_name')
            return render(request, 'applyFor/add_applyFors.html', {'materials': materials, 'err': '此申购编号已存在, 请重新输入', 'name': name})
        else:
            purchase_price = float(material_price) * float(purchase_amount)
            purchase_people = request.POST.get('purchase_people', None)

        id = request.POST.get('id')
        materials = models.Material.objects.filter(material_id=id)
        a_msg = models.Apply_for()
        a_msg.applyforId = applyforId
        a_msg.material_id = materials.get(material_id=id).material_id
        a_msg.material_name = materials.get(material_id=id).material_name
        a_msg.material_Model_number = materials.get(material_id=id).material_Model_number
        a_msg.material_describe = materials.get(material_id=id).material_describe
        a_msg.material_use = materials.get(material_id=id).material_use
        a_msg.material_price = material_price
        a_msg.purchase_amount = purchase_amount
        a_msg.purchase_price = purchase_price
        a_msg.purchase_people = purchase_people
        a_msg.save()

        name = request.COOKIES.get('login_name')
        return render(request, 'applyFor/add_applyFors.html', {'materials': materials, 'success': "申购信息添加成功", 'name': name})

def update_applyFors(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        applyFors = models.Apply_for.objects.get(applyforId=id)
        materials = models.Material.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyFor/update_applyFors.html', {'applyFors': applyFors, 'materials': materials, 'name': name})
    else:
        list = ['applyforId', 'materialId', 'material_price', 'purchase_amount', 'purchase_people']
        info = []
        for li in list:
            info.append(request.POST.get(li, None))
        if info[2] == None or info[3] ==None:
            name = request.COOKIES.get('login_name')
            return render(request, 'applyFor/update_applyFors.html', {'err': '物料单价和采购数量不能为空！', 'name': name})

        info[0] = request.GET.get('id')
        materials = models.Material.objects.filter(material_id=info[1])
        a_msg = models.Apply_for()
        a_msg.applyforId = info[0]
        a_msg.material_id = materials.get(material_id=info[1]).material_id
        a_msg.material_name = materials.get(material_id=info[1]).material_name
        a_msg.material_Model_number = materials.get(material_id=info[1]).material_Model_number
        a_msg.material_describe = materials.get(material_id=info[1]).material_describe
        a_msg.material_use = materials.get(material_id=info[1]).material_use
        a_msg.material_price = info[2]
        a_msg.purchase_amount = info[3]
        a_msg.purchase_price = float(info[2]) * float(info[3])
        a_msg.purchase_people = info[4]
        a_msg.is_apply = False
        a_msg.save()

        applyFors = models.Apply_for.objects.get(applyforId=info[0])
        materials = models.Material.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyFor/update_applyFors.html', {'success': "申购信息修改成功！",
                                                                  'applyFors': applyFors, 'materials': materials, 'name': name})

def delete_applyfor(request):
    id = request.GET.get('id')
    if models.Apply_for.objects.get(applyforId=id).delete():
        return redirect('/applyfor/')
    else:
        return redirect('/applyfor/')

def my_purchase(request):
    if request.method == 'GET':
        purchases = models.Purchase.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'Purchase/purchases.html', {'purchases': purchases, 'name': name})

def add_purchase(request):
    id = request.GET.get('id')
    applyfor = models.Apply_for.objects.get(applyforId=id)
    s = models.Purchase.objects.filter(purchase_number=id)
    if s.count() != 0:
        applyfors = models.Apply_for.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyFor/applyFors.html', {'applyfors': applyfors, 'err': '此采购编号已存在, 请重新申请', 'name': name})

    p_msg = models.Purchase()
    p_msg.purchase_number = str(applyfor.applyforId) + str('-') + \
                            str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    p_msg.purchase_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    p_msg.material_id = applyfor.material_id
    p_msg.material_name = applyfor.material_name
    p_msg.material_Model_number = applyfor.material_Model_number
    p_msg.material_describe = applyfor.material_describe
    p_msg.material_use = applyfor.material_use
    p_msg.material_price = applyfor.material_price
    p_msg.purchase_amount = applyfor.purchase_amount
    p_msg.purchase_price = float(applyfor.material_price) * float(applyfor.purchase_amount)
    p_msg.purchase_people = applyfor.purchase_people
    p_msg.disburse_company = models.Material.objects.get(material_id=applyfor.material_id).disburse_company
    p_msg.save()

    if applyfor.is_apply == False:
        applyfor.is_apply = True
        applyfor.save()
        applyfors = models.Apply_for.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyFor/applyFors.html', {'applyfors': applyfors, 'name': name})
    else:
        applyfors = models.Apply_for.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyFor/applyFors.html', {'applyfors': applyfors, 'name': name})

def delete_purchase(request):
    id = request.GET.get('id')
    if models.Purchase.objects.get(purchase_number=id).delete():
        return redirect('/purchase/')
    else:
        return redirect('/purchase/')

def update_active(request):
    id = request.GET.get('id')
    purchase = models.Purchase.objects.get(purchase_number=id)
    if purchase.is_active == False:
        purchase.is_active = True
        purchase.purchase_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        purchase.save()
        return redirect('/purchase/')
    else:
        return redirect('/purchase/')

def update_purchase(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        purchase = models.Purchase.objects.get(purchase_number=id)
        name = request.COOKIES.get('login_name')
        return render(request, 'Purchase/update_purchase.html', {'purchase': purchase, 'name': name})
    else:
        list = ['purchase_number', 'material_price', 'purchase_amount']
        info = []
        for li in list:
            info.append(request.POST.get(li, None))
        if info[1] == None or info[2] == None:
            name = request.COOKIES.get('login_name')
            return render(request, 'Purchase/update_purchase.html', {'err': '成交单价和采购数量不能为空！', 'name': name})

        purchase = models.Purchase.objects.get(purchase_number=info[0])
        p_msg = models.Purchase()
        p_msg.purchase_number = purchase.purchase_number
        p_msg.purchase_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        p_msg.material_id = purchase.material_id
        p_msg.material_name = purchase.material_name
        p_msg.material_Model_number = purchase.material_Model_number
        p_msg.material_describe = purchase.material_describe
        p_msg.material_use = purchase.material_use
        p_msg.material_price = info[1]
        p_msg.purchase_amount = info[2]
        p_msg.purchase_price = float(info[1]) * float(info[2])
        p_msg.purchase_people = purchase.purchase_people
        p_msg.disburse_company = purchase.disburse_company
        p_msg.is_active = False
        p_msg.is_putintolib = False
        p_msg.save()

        name = request.COOKIES.get('login_name')
        return render(request, 'Purchase/update_purchase.html', {'purchase': p_msg, 'success': "采购信息修改成功", 'name': name})

def myputintolibrary(request):
    if request.method == 'GET':
        putintoStorages = models.putintoStorage.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'putintolibrary/putintolibrary.html', {'putintoStorages': putintoStorages, 'name': name})

def update_putintolibrary(request):
    id = request.GET.get('id')
    pis = models.putintoStorage.objects.get(PISnumber=id)
    if pis.is_putintosttorage == True:
        pis.is_putintosttorage = False
        pis.save()
        putintoStorages = models.putintoStorage.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'putintolibrary/putintolibrary.html', {'putintoStorages': putintoStorages, 'name': name})

def add_putintolibrary(request):
    id = request.GET.get('id')
    purchase = models.Purchase.objects.get(purchase_number=id)

    put_msg = models.putintoStorage()
    put_msg.PISnumber = purchase.purchase_number
    put_msg.PIStime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    put_msg.material_id = purchase.material_id
    put_msg.material_name = purchase.material_name
    put_msg.material_Model_number = purchase.material_Model_number
    put_msg.material_describe = purchase.material_describe
    put_msg.material_use = purchase.material_use
    put_msg.PutPeople = request.COOKIES.get('login_name')
    s = models.putintoStorage.objects.filter(PISnumber=purchase.purchase_number)
    if s.count() != 0:
        put = models.putintoStorage.objects.get(PISnumber=purchase.purchase_number)
        put_msg.amount = purchase.purchase_amount + put.amount
    else:
        put_msg.amount = purchase.purchase_amount
    put_msg.save()

    if purchase.is_putintolib == False:
        purchase.is_putintolib = True
        purchase.save()
        purchases = models.Purchase.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'Purchase/purchases.html', {'purchases': purchases, 'name': name})
    else:
        purchase.is_putintolib = False
        purchase.save()
        purchases = models.Purchase.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'Purchase/purchases.html', {'purchases': purchases, 'name': name})

def delete_putintolibrary(request):
    id = request.GET.get('id')
    if models.putintoStorage.objects.get(PISnumber=id).delete():
        return redirect('/putintolibrary/')
    else:
        return redirect('/putintolibrary/')

def inventory(request):
    if request.method == 'GET':
        inventory = models.inventory.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'Inventory/inventory.html', {'inventory': inventory, 'name': name})

def add_inventory(request):
    id = request.GET.get('id')
    putintolibrary = models.putintoStorage.objects.get(PISnumber=id)

    in_msg = models.inventory()
    in_msg.inventory_number = putintolibrary.PISnumber
    in_msg.material_id = putintolibrary.material_id
    in_msg.material_name = putintolibrary.material_name
    in_msg.material_Model_number = putintolibrary.material_Model_number
    in_msg.material_describe = putintolibrary.material_describe
    in_msg.material_use = putintolibrary.material_use
    s = models.inventory.objects.filter(inventory_number=putintolibrary.PISnumber)
    if s.count() != 0:
        inven = models.inventory.objects.get(inventory_number=putintolibrary.PISnumber)
        in_msg.put_in_amount = inven.put_in_amount + putintolibrary.amount
        in_msg.position = inven.position
        in_msg.out_of_amount = inven.out_of_amount
    else:
        in_msg.put_in_amount = putintolibrary.amount
    in_msg.save()
    in_msg.surplus_amount = float(in_msg.put_in_amount) - float(in_msg.out_of_amount)
    in_msg.save()

    if putintolibrary.is_putintosttorage == False:
        putintolibrary.is_putintosttorage = True
        putintolibrary.save()
        putintoStorages = models.putintoStorage.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'putintolibrary/putintolibrary.html', {'putintoStorages': putintoStorages, 'name': name})

def delete_inventy(request):
    id = request.GET.get('id')
    if models.inventory.objects.get(inventory_number=id).delete():
        return redirect('/inventory/')
    else:
        return redirect('/inventory/')

def update_inventory(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        inventory = models.inventory.objects.get(inventory_number=id)
        name = request.COOKIES.get('login_name')
        return render(request, 'Inventory/update_inventory.html', {'inventory': inventory, 'name': name})
    else:
        id = request.POST.get('inventory_number')
        inventory = models.inventory.objects.get(inventory_number=id)
        position = request.POST.get('position', None)
        inventory.position = position
        inventory.save()

        name = request.COOKIES.get('login_name')
        return render(request, 'Inventory/update_inventory.html', {'inventory': inventory, 'success': "添加成功", 'name': name})

def receive(request):
    if request.method == 'GET':
        receives = models.receive.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'receive/receive.html', {'receives': receives, 'name': name})

def add_receive(request):
    if request.method == 'GET':
        inventory = models.inventory.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'receive/add_receive.html', {'inventory': inventory, 'name': name})
    else:
        inventory_number = request.POST.get('inventory_number')
        receive_amount = request.POST.get('receive_amount')
        receive_people = request.POST.get('receive_people')
        inventory = models.inventory.objects.get(inventory_number=inventory_number)

        receivemodel = models.receive()
        receivemodel.receive_number = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        receivemodel.inventory_number = inventory_number
        receivemodel.material_id = inventory.material_id
        receivemodel.material_name = inventory.material_name
        receivemodel.material_Model_number = inventory.material_Model_number
        receivemodel.material_describe = inventory.material_describe
        receivemodel.material_use = inventory.material_use
        receivemodel.position = inventory.position
        if int(receive_amount) > inventory.surplus_amount:
            name = request.COOKIES.get('login_name')
            return render(request, 'receive/add_receive.html', {'err': "添加失败，领料数量不能比剩余库存大。" + "剩余库存为：%s"
                                                                       % (inventory.surplus_amount), 'name': name})
        receivemodel.receive_amount = receive_amount
        receivemodel.receive_people = receive_people
        receivemodel.save()
        name = request.COOKIES.get('login_name')
        return render(request, 'receive/add_receive.html', {'success': "添加成功", 'name': name})

def delete_receive(request):
    id = request.GET.get('id')
    if models.receive.objects.get(receive_number=id).delete():
        return redirect('/receive/')
    else:
        return redirect('/receive/')

def update_receive(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        receive = models.receive.objects.get(receive_number=id)
        inventory = models.inventory.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'receive/update_receive.html', {'receive': receive, 'inventory': inventory, 'name': name})

    else:
        receive_number = request.POST.get('receive_number')
        post_receive = models.receive.objects.get(receive_number=receive_number)
        inventory_number = request.POST.get('inventory_number')
        receive_amount = request.POST.get('receive_amount', None)
        post_inventory = models.inventory.objects.get(inventory_number=inventory_number)
        receive_people = request.POST.get('receive_people', None)

        receivemodel = models.receive()
        receivemodel.receive_number = post_receive.receive_number
        receivemodel.inventory_number = post_inventory.inventory_number
        receivemodel.material_id = post_inventory.material_id
        receivemodel.material_name = post_inventory.material_name
        receivemodel.material_Model_number = post_inventory.material_Model_number
        receivemodel.material_describe = post_inventory.material_describe
        receivemodel.material_use = post_inventory.material_use
        receivemodel.position = post_inventory.position
        if int(receive_amount) > post_inventory.surplus_amount:
            inventory = models.inventory.objects.all()
            name = request.COOKIES.get('login_name')
            return render(request, 'receive/update_receive.html', {'err': "编辑失败，领料数量不能比剩余库存大。" + "剩余库存为：%s" % (post_inventory.surplus_amount),
                                                                   'receive': post_receive, 'inventory': inventory, 'name': name})
        receivemodel.receive_amount = receive_amount
        receivemodel.receive_people = receive_people

        receivemodel.save()
        inventory = models.inventory.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'receive/update_receive.html', {'success': "修改成功", 'receive': post_receive, 'inventory': inventory, 'name': name})

def applyoutlib(request):
    if request.method == 'GET':
        applyoutlib = models.ApplyOutLib.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyoutlib/applyoutlib.html', {'applyoutlib': applyoutlib, 'name': name})

def delete_applyoutlib(request):
    id = request.GET.get('id')
    if models.ApplyOutLib.objects.get(apply_number=id).delete():
        return redirect('/applyoutlib/')
    else:
        return redirect('/applyoutlib/')

def add_applyoutlib(request):
    id = request.GET.get('id')
    receive = models.receive.objects.get(receive_number=id)

    in_msg = models.ApplyOutLib()
    in_msg.apply_number = "Apply" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    in_msg.receive_number = receive.receive_number
    in_msg.inventory_number = receive.inventory_number
    in_msg.apply_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    in_msg.material_id = receive.material_id
    in_msg.material_name = receive.material_name
    in_msg.material_Model_number = receive.material_Model_number
    in_msg.material_describe = receive.material_describe
    in_msg.material_use = receive.material_use
    in_msg.out_of_amount = receive.receive_amount
    in_msg.apply_people = receive.receive_people
    in_msg.save()

    if receive.is_submit == False:
        receive.is_submit = True
        receive.save()
        receives = models.receive.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'receive/receive.html', {'receives': receives, 'name': name})

def update_amount(request):
    id = request.GET.get('id')
    applyoutlib = models.ApplyOutLib.objects.get(apply_number=id)

    s = models.inventory.objects.filter(inventory_number=applyoutlib.inventory_number)
    if s.count() != 0:
        inventory = models.inventory.objects.get(inventory_number=applyoutlib.inventory_number)
        inventory.out_of_amount = applyoutlib.out_of_amount + inventory.out_of_amount
        inventory.save()
        inventory.surplus_amount = int(inventory.put_in_amount) - int(inventory.out_of_amount)
        inventory.save()
    else:
        inventory = models.inventory.objects.get(inventory_number=applyoutlib.inventory_number)
        inventory.out_of_amount = applyoutlib.out_of_amount
        inventory.save()
        inventory.surplus_amount = int(inventory.put_in_amount) - int(inventory.out_of_amount)
        inventory.save()

    out = models.out_of_library()
    out.out_of_number = "Out-" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    out.receive_number = applyoutlib.receive_number
    out.inventory_number = applyoutlib.inventory_number
    out.out_of_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    out.material_id = applyoutlib.material_id
    out.material_name = applyoutlib.material_name
    out.material_Model_number = applyoutlib.material_Model_number
    out.material_describe = applyoutlib.material_describe
    out.material_use = applyoutlib.material_use
    out.out_of_amount = applyoutlib.out_of_amount
    out.material_handler = applyoutlib.apply_people
    out.save()

    if applyoutlib.is_agree == False:
        applyoutlib.is_agree = True
        applyoutlib.save()
        applyoutLib = models.ApplyOutLib.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'applyoutlib/applyoutlib.html', {'applyoutlib': applyoutLib, 'name': name})

def out_of_library(request):
    if request.method == 'GET':
        out_of_library = models.out_of_library.objects.all()
        name = request.COOKIES.get('login_name')
        return render(request, 'outoflibrary/outoflib.html', {'out_of_library': out_of_library, 'name': name})

def delete_out_of_library(request):
    id = request.GET.get('id')
    if models.out_of_library.objects.get(out_of_number=id).delete():
        return redirect('out_of_library')
    else:
        return redirect('out_of_library')


















