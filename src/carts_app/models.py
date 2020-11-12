from django.db import models
from products_app.models import Products
from django.contrib.auth import get_user_model

Users = get_user_model()

# Create your models here.


class Cart(models.Model):
    user_id = models.ForeignKey(
        Users,
        db_column="user_id",
        on_delete=models.PROTECT,
        related_name="cart_user_id",
    )
    product_id = models.ForeignKey(
        Products,
        db_column="product_id",
        on_delete=models.PROTECT,
        related_name="cart_product_id",
    )
    ratings = models.IntegerField(default=5)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        db_table = "carts"

    def __str__(self):
        return str(self.user_id) + " | " + str(self.product_id)
