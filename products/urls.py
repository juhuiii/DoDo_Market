from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ProductList,
    ProductCreate,
    ProductDetail,
    ProductUpdate,
    ProductDelete,
    ProductImageCreate,
    ProductImageDelete,
)


urlpatterns = [
    path('list/', ProductList.as_view()),
    path('create', ProductCreate.as_view()),
    path('<int:pk>', ProductDetail.as_view()),
    path('<int:pk>/update', ProductUpdate.as_view()),
    path('<int:pk>/delete', ProductDelete.as_view()),
    path('image/create', ProductImageCreate.as_view()),
    path('image/<int:pk>/delete', ProductImageDelete.as_view()),
]

