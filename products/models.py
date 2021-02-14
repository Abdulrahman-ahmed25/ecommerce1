from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify

class Product(models.Model):
    title = models.CharField(max_length=120)
    description =models.TextField(blank=True, null=True)
    price =models.DecimalField(decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product_details", kwargs = {"pk": self.pk})

class Variation(models.Model):
    # product = models.ForeignKey(on_delete=CASCADE, to='products.product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    price =models.DecimalField(decimal_places=2, max_digits=10)
    sale_price =models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title   
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()
    
# def product_post_saved_receiver(instance, *args, **kwargs):
#     product = instance
#     variations = product.variation_set.all()
#     if variations.count() == 0:
#         new_var = Variation()
#         new_var.product = product
#         new_var.title = "Default"
#         new_var.price = product.price
#         new_var.save()

# post_save.connect(product_post_saved_receiver, sender=Product)

def image_upload_to(instance, filename):
    title = instance.product.title
    slug  = slugify(title)
    file_extension = filename.split(".")
    # new_filename = "%s-%s.%s" %(slug, instance.id, file_extension) = 
    new_filename = f'{slug}-{instance.id}.{file_extension}' 
    return f'Product/{slug}/{new_filename}'

class ProductImage(models.Model):
    # product = models.ForeignKey(on_delete=CASCADE, to='products.product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image =  models.ImageField(upload_to = image_upload_to)

    def __str__(self):
        return self.product.title
