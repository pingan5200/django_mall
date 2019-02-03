from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('all/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # 1/coffee/
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('', views.home, name='home'),

]