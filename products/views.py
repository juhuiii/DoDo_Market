from django.shortcuts import render
from django.db import IntegrityError  #이미지 업로드 시

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,IsAdminUser

from rest_framework import generics

from .models import Product
from .serializers import (
    ProductSerializer,
    ProductImageCreateSerializer,
    ProductImageDeleteSerializer,
    ProductLikeSerializer,
)


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        #카테고리별로 분류해서 가져오기
        query_params = self.request.query_params
        
        sort = query_params.get('sort')
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
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise exceptions.PermissionDenied('해당 매물을 수정 할 권한이 없습니다.')
        try:
            return serializer.save() 
        except IntegrityError:
            raise exceptions.ValidationError('잘못된 형식입니다.')


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductUpdate(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Product.objects

    def get_object(self):
        object = super().get_object()
        if self.request.user.is_superuser:
            return object
        else:
            raise exceptions.PermissionDenied('수정 할 권한이 없습니다.')


class ProductDelete(generics.DestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects

    def get_object(self):
        object = super().get_object()
        if self.request.user.is_superuser:
            return object
        else:
            raise exceptions.PermissionDenied('수정 할 권한이 없습니다.')


class ProductImageCreate(generics.CreateAPIView):
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise exceptions.PermissionDenied('해당 상품을 수정 할 권한이 없습니다.')
        try:
            return serializer.save()
        except IntegrityError:
            raise exceptions.ValidationError('잘못된 형식입니다.')


class ProductImageDelete(generics.DestroyAPIView):
    serializer_class = ProductImageDeleteSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProductImage.objects.select_related('product_user')

    def get_object(self):
        object = super().get_object()
        if self.request.user.is_superuser:
            return object
        else:
            raise exceptions.PermissionDenied('해당 상품을 수정할 권한이 없습니다.')


class ProductIncreaseLike(generics.UpdateAPIView):
    serializer_class = ProductLikeSerializer
    queryset =Product.objects.all()
    
    def get_object(self):
        object = super().get_object()
        object.like = object.like + 1
        return object


class ProductDecreaseLike(generics.UpdateAPIView):
    serializer_class = ProductLikeSerializer
    queryset = Product.objects.all()
    
    def get_object(self):
        object = super().get_object()
        object.like = object.like - 1 if object.like > 0 else 0
        return object