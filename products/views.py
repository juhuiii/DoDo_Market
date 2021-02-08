from django.shortcuts import render
from django.db import IntegrityError  #이미지 업로드 시

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,IsAdminUser

from rest_framework import generics

from .models import Product
from .serializers import (
    ProductSerilaizer,
    ProductListSerializer,
    ProductImageCreateSerializer,
    ProductImageDeleteSerializer
)


class ProductList(generics.ListAPIView):
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        #카테고리별로 분류해서 가져오기
        query_params = self.request.query_params
        
        sort = self.request.query_params.get('sort')
        sort_values=set(['-created','price','-price','-like'])
        if sort == None or not sort in sort_values :
            sort = '-created'
        
        if 'category' in query_params.keys():
            queryset = Product.objects.filter(
                category=query_params.get('category')
            ).prefetch_related(
                'product_image',
            ).order_by(sort).all()
            
            return queryset
        else:
            queryset=Product.objects.prefetch_related(
                'product_image',
            ).order_by(sort).all()
            
            return queryset

class ProductCreate(generics.CreateAPIView):
    serializer_class = ProductSerilaizer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise exceptions.PermissionDenied('해당 매물을 수정 할 권한이 없습니다.')
        try:
            return serializer.save()
        except IntegrityError:
            raise exceptions.ValidationError('잘못된 형식입니다.')



class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerilaizer
    queryset = Product.objects.all()


class ProductImageCreate(generics.CreateAPIView):
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticatied:
            raise exceptions.PermissionDenied('로그인이 필요합니다.')
        if not self.request.user.is_superuser:
            raise exceptions.PermissionDenied('해당 매물을 수정 할 권한이 없습니다.')
        try:
            return serializer.save()
        except IntegrityError:
            raise exceptions.ValidationError('잘못된 형식입니다.')


class ProductImageDelete(generics.DestroyAPIView):
    serializer_class = ProductImageDeleteSerializer

    def get_queryset(self):
        return ProductImage.objects.select_related('product_user')

    def get_object(self):
        object = super().get_object()
        if object.product.user == self.request.user:
            return object
        else:
            raise exceptions.PermissionDenied('해당 매물을 수정할 권한이 없습니다.')