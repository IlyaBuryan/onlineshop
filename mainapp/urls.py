from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
   path('', mainapp.main, name='main'),
   path('category/<int:pk>/', mainapp.category, name='category'),
   path('category/search/', mainapp.search, name='search'),
   path('products/', mainapp.products, name='products'),
   path('product/<int:pk>/', mainapp.single, name="single"),
   path('reviews/<int:pk>', mainapp.reviews, name='reviews'),
   path('contacts/', mainapp.contacts, name='contacts'),
]