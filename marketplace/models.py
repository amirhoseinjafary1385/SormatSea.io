from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser ,User
from django.db import models
from django.conf import settings 


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class CustomUser(AbstractUser):
#     country = models.CharField(max_length= 100, blank= True)
#     city = models.CharField(max_length= 100, blank= True)

#     def __str__(self):
#        return self.username

    
class NFT(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='nft_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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