from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name="base"),
    path('register/', views.register, name="register"),
    path('update_password/', views.update_password, name='update_password'),
    path('welcome/', views.welcome, name="welcome"),
    path('update_material/', views.update_material, name="update_material"),
    path('add_material/', views.add_material, name="add_material"),
    path('delete_material/', views.delete_material, name="delete_material"),
    path('applyfor/', views.my_applyFors, name="applyfor"),
    path('add_applyfor/', views.add_applyFors, name="add_applyfor"),
    path('update_applyfor/', views.update_applyFors, name="update_applyfor"),
    path('delete_applyfor/', views.delete_applyfor, name="delete_applyfor"),
    path('purchase/', views.my_purchase, name="purchase"),
    path('add_purchase/', views.add_purchase, name="add_purchase"),
    path('delete_purchase/', views.delete_purchase, name="delete_purchase"),
    path('update_purchase/', views.update_purchase, name="update_purchase"),
    path('update_active/', views.update_active, name='update_active'),
    path('putintolibrary/', views.myputintolibrary, name='putintolibrary'),
    path('add_putintolibrary/', views.add_putintolibrary, name="add_putintolibrary"),
    path('delete_putintolibrary/', views.delete_putintolibrary, name="delete_putintolibrary"),
    path('update_putintolibrary/', views.update_putintolibrary, name="update_putintolibrary"),
    path('inventory/', views.inventory, name="inventory"),
    path('add_inventory/', views.add_inventory, name="add_inventory"),
    path('delete_inventory/', views.delete_inventy, name="delete_inventory"),
    path('update_inventory/', views.update_inventory, name="update_inventory"),
    path('receive/', views.receive, name="receive"),
    path('add_receive/', views.add_receive, name="add_receive"),
    path('delete_receive/', views.delete_receive, name="delete_receive"),
    path('update_receive/', views.update_receive, name="update_receive"),
    path('applyoutlib/', views.applyoutlib, name="applyoutlib"),
    path('add_applyoutlib/', views.add_applyoutlib, name="add_applyoutlib"),
    path('update_amount/', views.update_amount, name="update_amount"),
    path('delete_applyoutlib/', views.delete_applyoutlib, name="delete_applyoutlib"),
    path('out_of_library/', views.out_of_library, name="out_of_library"),
    path('delete_out_of_library/', views.delete_out_of_library, name="delete_out_of_library"),
]


