from rest_framework import serializers
from product.models import Category, Review, Product


class Categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','product_counts')

class CategoriesSerializerProduct(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class Product_Serializer(serializers.ModelSerializer):
    category = CategoriesSerializerProduct()

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']


class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('product','text','stars')


class ProductReviews_Serializer(serializers.ModelSerializer):
    product_review = Review_Serializer(many=True)
    category = Categories_Serializer()

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category','product_review', 'average_rating']
