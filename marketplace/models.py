from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings 
from django.utils import timezone
from django.core.validators import MinValueValidator


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
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class NFT(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='nft_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', 'Purchase'),
        ('bid', 'Bid'),
        ('royalty', 'Royalty Payment'),
        ('refund', 'Refund'),
        ('withdrawal', 'Withdrawal'),
    ]
    
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
        ('wallet', 'Digital Wallet'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('disputed', 'Disputed'),
        ('cancelled', 'Cancelled'),
    ]

    nft = models.ForeignKey(
        NFT,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(
        max_length=10,
        default='IRT'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        default='purchase'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        blank=True,
        null=True
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
            models.Index(fields=['status']),
            models.Index(fields=['user']),
            models.Index(fields=['nft']),
            models.Index(fields=['transaction_hash']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def is_successful(self):
        return self.status == 'completed'

    def mark_as_completed(self, save=True):
        self.status = 'completed'
        self.completed_at = timezone.now()
        if save:
            self.save()

    def mark_as_failed(self, error_message, save=True):
        self.status = 'failed'
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