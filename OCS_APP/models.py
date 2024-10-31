from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

def user_directory_path(instance, filename):
    return 'user_(0)/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length = 10, max_length = 20, prefix = 'cat', alphabet = 'abcdefgh12345')
    title = models.CharField(max_length = 100, default = 'Other Products')
    image = models.ImageField(upload_to = 'category', default = 'Category.jpg')
    class Meta:
        verbose_name_plural = 'Categories'
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def __str__(self):
        return self.title
    
class Manufacturer(models.Model):
    mid = ShortUUIDField(unique=True, length = 10, max_length = 20, prefix = 'manuf', alphabet = 'abcdefgh12345')
    title = models.CharField(max_length = 100, default = 'Local')
    class Meta:
        verbose_name_plural = 'Manufacturers'
    def __str__(self):
        return self.title

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length = 10, max_length = 20, alphabet = 'abcdefgh12345')
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, related_name = 'category')
    manufacturer = models.ForeignKey(Manufacturer, on_delete = models.SET_NULL, null = True)
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = user_directory_path, default = 'Product.jpg')
    description = RichTextUploadingField(null = True, blank = True, default = 'This is a dental product.')
    price = models.IntegerField(default = 1000)
    old_price = models.IntegerField(default = 2000)
    specifications = RichTextUploadingField(null = True, blank = True)
    type = models.CharField(max_length = 100, default = 'Dental Product', null = True, blank = True)
    stock = models.IntegerField(default = '1', null = True, blank = True)
    life = models.CharField(max_length = 100, default = '100 Days', null = True, blank = True)
    mfd = models.DateTimeField(auto_now_add = False, null = True, blank = True)
    #tags = models.ForeignKey(Tags, on_delete = models.SET_NULL, null = True)
    product_status = models.CharField(choices = (('draft', 'Draft'), ('disabled', 'Disabled'), ('rejected', 'Rejected'), ('in_review', 'In Review'), ('published', 'Published')), max_length = 12, default = 'in_review')
    status = models.BooleanField(default = True)
    in_stock = models.BooleanField(default = True)
    featured = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(null = True, blank = True)
    tags = TaggableManager(blank = True)
    class Meta:
        verbose_name_plural = 'Products'
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def __str__(self):
        return self.title
    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price

class ProductImages(models.Model):
    images = models.ImageField(upload_to = 'product-images', default = 'Product.jpg')
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, related_name = 'p_images')
    date = models.DateTimeField(auto_now_add = True)
    class Meta:
        verbose_name_plural = 'Product Images'

class CartOrder(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Invoice No.')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    price = models.IntegerField(default = 1000)
    paid_status = models.BooleanField(default = False)
    order_date = models.DateTimeField(auto_now_add = True)
    delivery_address = models.CharField(max_length = 150)
    payment_method = models.CharField(max_length = 25)
    product_status = models.CharField(choices = (("processing", "Processing"), ("shipped", "Shipped"), ("delivered", "Delivered")), max_length = 30, default = "processing")
    class Meta:
        verbose_name_plural = 'Orders'

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete = models.CASCADE)
    invoice_no = models.IntegerField(verbose_name='Invoice No.')
    product_status = models.CharField(max_length = 200)
    item = models.CharField(max_length = 200)
    image = models.CharField(max_length = 200)
    qty = models.IntegerField(default = 0)
    price = models.IntegerField(default = 1000)
    total = models.IntegerField(default = 1000)
    class Meta:
        verbose_name_plural = 'Order Items'
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def order_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image))

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, related_name = 'reviews')
    review = models.TextField()
    rating = models.IntegerField(choices = ((1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')), default = None)
    date = models.DateTimeField(auto_now_add = True)
    class Meta:
        verbose_name_plural = 'Product Reviews'
    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.rating

class Address(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    mobile = models.CharField(max_length = 100, null = True)
    address = models.CharField(max_length = 100, null = True)
    status = models.BooleanField(default = False)
    class Meta:
        verbose_name_plural = 'Addresses'