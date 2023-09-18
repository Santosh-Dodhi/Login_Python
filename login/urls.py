from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('' , views.home , name = "home"),

    path('signup' ,views.signup , name="signup" ),

    path('signin' ,views.signin , name="signin" ),

    path('signout' ,views.signout , name="signout" ),

    path('activate/<uidb64>/<token>' , views.activate , name = "activate"),

    path('product_detail/' , views.product_detail , name = "product_detail") ,

    # Dynamic Url Type : <int: name > , <str: name> , <slug: name> 
    # slug = data-datadklsn-dsnkj-vvds
    path('company/<str:company_name>' , views.company) 
]
