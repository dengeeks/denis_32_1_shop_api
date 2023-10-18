from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(to='Category', on_delete=models.SET_NULL, related_name='product_category', null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='product_review')

    def __str__(self):
        return self.text
