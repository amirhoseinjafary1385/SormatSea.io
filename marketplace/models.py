from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings 
# import NFT


#Make A Transaction Method

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique= True, blank = True)

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique= True, blank = True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        

    def __str__(self):

        return self.title




class Transaction(models.Model):

    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices= [
    
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])

    payment_gateway = models.CharField(max_length=50)
    bank_reference = models.CharField(max_length=120, blank=True)
    bank_trace_number = models.CharField(max_length=120, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.id} for {self.nft.title}"



# class CustomUser(AbstractUser):
#     country = models.CharField(max_length= 100, blank= True)
#     city = models.CharField(max_length= 100, blank= True)

#     def __str__(self):
#        return self.username





    #owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
