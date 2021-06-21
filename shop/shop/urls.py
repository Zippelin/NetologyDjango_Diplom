"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_view
from products.views_api import ProductAPIView
from reviews.views_api import ReviewsAPIView
from orders.views_api import OrderAPIView
from collections_.views_api import CollectionsAPIView


from rest_framework import routers

API_VERSION = [None, 'v1/']
API_BASE_URL = 'api'

router = routers.DefaultRouter()
router.register('products', ProductAPIView)
router.register('product-reviews', ReviewsAPIView)
router.register('orders', OrderAPIView)
router.register('product-collections', CollectionsAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authenticate/', auth_view.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path('/'.join([API_BASE_URL, API_VERSION[1]]), include(router.urls)),
]
