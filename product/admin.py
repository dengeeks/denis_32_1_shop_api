from django.contrib import admin
from product.models import Category,Review,Product,Tag
# Register your models here.

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Product)
admin.site.register(Tag)
