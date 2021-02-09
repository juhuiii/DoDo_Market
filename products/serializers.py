from rest_framework import serializers,fields
from .models import Product,ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        return instance.get_info()



class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'image',
            'product',
        )

    def to_representation(self, instance):
        return instance.get_info()


class ProductImageDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage