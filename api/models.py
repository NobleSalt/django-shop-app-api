import uuid
from django.db import models
from django.contrib.auth import get_user_model

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

User = get_user_model()

# Create your models here.
class AbstractBaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


ORDER_STATUS = (
    ("PENDING", "PENDING"),
    ("PROCESSING", "PROCESSING"),
    ("CANCELED", "CANCELED"),
    ("DELIVERED", "DELIVERED"),
)


CONDITION_CHOICES = (
    ("USED", "USED"),
    ("NEW", "NEW"),
    ("FRESH", "FRESH"),
)


ANSWER_CHOICES = (
    ("YES", "YES"),
    ("NO", "NO"),
)


# class UserProfile(AbstractBaseUser, PermissionsMixin):
#     """ Database model for users in the system """
#     email = models.EmailField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)

#     objects = UserProfileManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     def __str__(self):
#         """ Return string representation of our user """
#         return self.email


class Store(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Category(AbstractBaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to="category_image")

    def __str__(self) -> str:
        return self.name

    @property
    def get_products_by_category(self):
        final_list = []
        for sub_cat in self.sub_categories.all():
            for cat in sub_cat.products.all():
                final_list.append(cat)
        return final_list


class SubCategory(AbstractBaseModel):
    category = models.ForeignKey(
        Category, related_name="sub_categories", on_delete=models.CharField
    )
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Product(AbstractBaseModel):
    store = models.ForeignKey(Store, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField()
    sub_category = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    quantity_title = models.CharField(max_length=20, default="each")
    discount = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=999999999)
    thumbnail = models.ImageField(upload_to="p-shop-products-thumbnail")
    image = models.ImageField(upload_to="p-shop-products-image")
    stock = models.PositiveBigIntegerField()
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES)
    rating = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    @property
    def image_url(self):
        if self.image:
            return f"http://localhost:8000{self.image.url}"


class Cart(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_complete = models.CharField(
        max_length=5, choices=ANSWER_CHOICES, default="NO"
    )

    def __str__(self) -> str:
        return f"{self.user}'s Cart"


class CartItem(AbstractBaseModel):
    product = models.ForeignKey(
        Product, related_name="cartitems", on_delete=models.CASCADE
    )
    amount = models.PositiveBigIntegerField(default=1)
    cart = models.ForeignKey(Cart, related_name="cartitems", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product} from {self.cart}"


# class CustomOrderManager(models.Manager):
#     def get_pending_order


class Order(AbstractBaseModel):
    status = models.CharField(max_length=100, default="PENDING", choices=ORDER_STATUS)
    cart = models.OneToOneField(
        Cart, related_name="order", on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def total(self):
        total = 0
        for item in self.cart.cartitems.all():
            total += item.amount * item.product.price
        return total


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
