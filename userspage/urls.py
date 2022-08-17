from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('products/', views.products),
    path('productdetails/<int:product_id>', views.product_details),
    path('add_to_cart/<int:product_id>',views.add_to_cart),
    path('mycart/',views.show_cart_items),
    path('orderform/<int:product_id>/<int:cart_id>', views.order_form),
    path('myorder/', views.show_order_items),
    path('esewa_verify/', views.esewa_verify),
    path('remove_cart/<int:cart_id>', views.remove_cart_items)
]