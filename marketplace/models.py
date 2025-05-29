from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator

# from .models import NFT

class Subcategory(models.Model):
    category = models.ForeignKey('marketplace.Category', on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class NFT(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="nft_images/", blank=True, null=True)
    price_irt = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price_polygon = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(NFT, through="CartItem")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        unique_together = ("cart", "nft")
        ordering = ["-added_at"]
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        db_table = "marketplace_cart_items"
        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["nft"]),
            models.Index(fields=["added_at"]),
            models.Index(fields=["added_at", "cart"]),
            models.Index(fields=["updated_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0), name="positive_quantity"
            ),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.nft.title}"

    @property
    def subtotal(self):
        return self.qiuantity * self.nft.price

    @property
    def total_price(self):
        return self.quantity * (self.unit_price or self.nft.price)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.nft.price
        super().save(*args, **kwargs)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("purchase", "Purchase"),
        ("bid", "Bid"),
        ("royalty", "Royalty Payment"),
        ("refund", "Refund"),
        ("withdrawal", "Withdrawal"),
    ]

    PAYMENT_METHODS = [
        ("credit_card", "Credit Card"),
        ("bank_transfer", "Bank Transfer"),
        ("crypto", "Cryptocurrency"),
        ("wallet", "Digital Wallet"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
        ("disputed", "Disputed"),
        ("cancelled", "Cancelled"),
    ]

    nft = models.ForeignKey(
        NFT,
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(
        max_digits=20, decimal_places=8, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=10, default="IRT")
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES, default="purchase"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, blank=True, null=True
    )
    payment_gateway = models.CharField(max_length=50)
    bank_reference = models.CharField(max_length=120, blank=True)
    bank_trace_number = models.CharField(max_length=120, blank=True)
    transaction_hash = models.CharField(max_length=120, blank=True)
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["user"]),
            models.Index(fields=["nft"]),
            models.Index(fields=["transaction_hash"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def is_successful(self):
        return self.status == "completed"

    def mark_as_completed(self, save=True):
        self.status = "completed"
        self.completed_at = timezone.now()
        if save:
            self.save()

    def mark_as_failed(self, error_message, save=True):
        self.status = "failed"
        self.error_message = error_message
        if save:
            self.save()

    @property
    def duration(self):
        if self.completed_at and self.created_at:
            return self.completed_at - self.created_at
        return None

    def __str__(self):
        if self.nft:
            return f"Transaction #{self.id} for {self.nft.title} ({self.status})"
        return f"Transaction #{self.id} ({self.status})"
