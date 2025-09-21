from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<uuid:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<uuid:pk>/disable/', views.ProductDisableView.as_view(), name='product-disable'),
    path('search/', views.ProductSearchView.as_view(), name='product-search'),
    path('bulk-create/', views.BulkProductCreateView.as_view(), name='product-bulk-create'),
    path('export/', views.ProductExportView.as_view(), name='product-export'),
]