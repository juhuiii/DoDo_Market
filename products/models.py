from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('VGTBL', '채소'),  # Vegetable
        ('FRUIT', '과일'),  # Fruit
        ('SFD', '수산'),  # Seafood
        ('MEAT', '정육'),  # Meat
        ('DE', '유제품/계란'),  # Dairy/Eggs
        ('FRZ', '냉동식품'),  # Frozen
        ('PNTRY', '가공식품'),  # Pantry
        ('HSHLD', '생필품'),  # Household
    )

    category = models.CharField(
        max_length=5,
        null=False,
        choices=CATEGORY_CHOICES,
    )
    name = models.CharField(max_length=200,null=False)
    origin = models.CharField(max_length=200,default="상세설명참조")
    description = models.TextField(max_length=2000, null=True)
    price = models.PositiveIntegerField(null=False)
    stock = models.PositiveIntegerField(null=False)
    like = models.IntegerField(default=0)
    availble_display = models.BooleanField(default=True)
    available_order = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '['+self.category+']'+self.name

    def get_info(self):
        return {
            'id': self.pk,
            'name': self.name,
            'origin': self.origin,
            'thumbnail': self.product_image.get_info().filter('defalut' == True),
            'images': [
                image.get_info()
                for image
                in self.product_image.order_by('id').all()
            ],
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'like': self.like,
            'availble_display': self.availabe_display,
            'available_order': self.available_order,
            'created': self.created,
            'updated': self.updated,
        }


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        models.CASCADE,
        related_name='product_image',
        default=None,
    )
    image = models.ImageField(upload_to='products/')
    default = models.BooleanField(default=False)  # 대표이미지

    def get_info(self):
        return {
            'id': self.pk,
            'image': self.image.url,
            'thumbnail': self.default,
        }

    # 자동삭제
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(ProductImage, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
