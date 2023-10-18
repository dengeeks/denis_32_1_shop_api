from rest_framework import serializers
from product.models import Category, Review, Product


class Categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']


class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text', 'product']
