from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ProductList,
    ProductCreate,
    ProductDetail,
)


urlpatterns = [
    path('list/', ProductList.as_view()),
    path('create', ProductCreate.as_view()),
    path('<int:pk>', ProductDetail.as_view()),
]

