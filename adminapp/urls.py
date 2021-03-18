from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/read/', adminapp.UsersListView.as_view(), name='users_read'),
    path('users/create/', adminapp.UsersCreate.as_view(), name='users_create'),
    path('users/update/<int:user_pk>/', adminapp.UsersUpdate.as_view(), name='users_update'),
    path('users/delete/<int:user_pk>/', adminapp.UsersDelete.as_view(), name='users_delete'),

    path('categories/read/', adminapp.CategoriesListView.as_view(), name='categories_read'),
    path('categories/create/', adminapp.CategoriesCreate.as_view(), name='categories_create'),
    path('categories/update/<int:category_pk>/', adminapp.CategoriesUpdate.as_view(), name='categories_update'),
    path('categories/delete/<int:category_pk>/', adminapp.CategoriesDelete.as_view(), name='categories_delete'),

    path('products/read/<int:category_pk>/', adminapp.ProductsListView.as_view(), name='products_read'),
    path('products/create/<int:category_pk>/', adminapp.ProductsCreate.as_view(), name='products_create'),
    path('products/update/<int:category_pk>/<int:product_pk>/', adminapp.ProductsUpdate.as_view(), name='products_update'),
    path('products/delete/<int:category_pk>/<int:product_pk>/', adminapp.ProductsDelete.as_view(), name='products_delete'),
    path('product/single/read/<int:product_pk>/', adminapp.ProductView.as_view(), name='product'),
]
