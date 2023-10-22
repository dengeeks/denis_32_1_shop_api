from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def product_counts(self):
        return self.product_category.count()


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(to='Category', on_delete=models.SET_NULL, related_name='product_category', null=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        return sum([i.stars for i in self.product_review.all()]) / self.product_review.count()


class Review(models.Model):
    STARS = (
        (1, '* '),
        (2, '* ' * 2),
        (3, '* ' * 3),
        (4, '* ' * 4),
        (5, '* ' * 5),
    )
    text = models.TextField()
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='product_review')
    stars = models.IntegerField(choices=STARS,default=5)

    def __str__(self):
        return self.text
