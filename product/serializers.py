from rest_framework import serializers
from product.models import Category, Review, Product, Tag
from rest_framework.exceptions import ValidationError


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class TagValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class Categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'product_counts')


class CategoriesSerializerProduct(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=36)

    @staticmethod
    def validate_name(name):
        category = list(Category.objects.values_list('name', flat=True))
        if name in category:
            raise ValidationError(f'Category `{name}` already exists!')
        return name


class Product_Serializer(serializers.ModelSerializer):
    category = CategoriesSerializerProduct()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'tags']

    def get_tags(self, products):
        return [tag.name for tag in products.tags.all()]


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    price = serializers.FloatField(min_value=0.0)
    category_id = serializers.IntegerField()
    tags = serializers.ListSerializer(required=False, child=serializers.IntegerField())

    def create_validated_data(self):
        validated = self.validated_data
        return {'title': validated['title'],
                'description': validated['description'],
                'price': validated['price'],
                'category_id': validated['category_id']}

    @staticmethod
    def validate_category_id(category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(f'Category `{category_id}` doesnt exists')
        return category_id

    def validate_tags(self, tags):
        error_tags = []
        tags_exists = list(Tag.objects.filter(id__in=tags).values_list('id', flat=True))
        for i in tags:
            if i not in tags_exists:
                error_tags.append(i)
        if error_tags:
            raise ValidationError(f'Tags under indexes{[tags.index(i) for i in error_tags]}')
        return tags


class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('product_id', 'text', 'stars')


class ReviewValidatedSerializer(serializers.Serializer):
    text = serializers.CharField()
    product_id = serializers.IntegerField()
    stars = serializers.IntegerField(max_value=5, default=5)

    @staticmethod
    def validate_product_id(product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError(f'Product {product_id} does not exists')
        return product_id


class ProductReviews_Serializer(serializers.ModelSerializer):
    product_review = Review_Serializer(many=True)
    category = Categories_Serializer()

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'product_review', 'average_rating']
