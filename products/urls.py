from django.urls import path
from .views import ProductDetailView,  ProductListView, VariationListView


app_name='products'
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('<int:pk>/inventory/', VariationListView.as_view(), name='product_inventory'),


]
