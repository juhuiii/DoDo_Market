from django.db import models
from products.models import Product

class Order(models.Model):
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    email=models.EmailField()

    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)
    # 결제 시도 전에 주문을 먼저 생성한다.

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    # 주문 시스템을 구현할 때는 변동될 수 있는 정보는
    # 항상 별도로 복사해서 저장해둔다.
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='ordered_items')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order #{self.order.id} item {self.product.name}"

    def get_item_total_price(self):
        return self.price * self.quantity


#결제 정보 저장
class OrderTransaction(models.Model):
    partner_order_id = models.CharField(max_length=100,null=False) #가맹점 주문번호
    partner_user_id =  models.CharField(max_length=100,null=False) #가맹점 회원 id
    payment_method_type= models.CharField(max_length=5,null=False) #CARD 혹은 MONEY
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transaction')
    created =models.DateTimeField(blank=False)
    approved=models.DateTimeField(blank=False)