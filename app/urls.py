from django.urls import path
from .views import ProductListView, ProductDetailView
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('detail/<pk>/', ProductDetailView.as_view(), name='product_detail'),
    # path('transaction/<str:transaction_type>/<int:product_id>/<int:quantity>/',
    #      views.create_transaction, name='create_transaction'),
    path('transaction/', views.transaction_list, name='transaction_list'),
    path('transaction_create/', views.transaction_create,
         name='transaction_create'),
    path('product_detail/<product_id>',
         views.product_detail, name='product_detail_2'),
    path('add_product/',
         views.add_product, name='add_product'),
    path('add_supplier/',
         views.add_supplier, name='add_supplier'),
    path('supplier_list/',
         views.supplier_list, name='supplier_list'),
    path('supplier_detail/<supplier_id>',
         views.supplier_detail, name='supplier_detail'),
]
