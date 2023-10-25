from rest_framework.response import Response
from product.models import Category, Product, Review
from rest_framework.decorators import api_view
from product.serializers import Categories_Serializer, Product_Serializer, Review_Serializer, ProductReviews_Serializer
from rest_framework import status


# Create your views here.

@api_view(['GET', 'POST'])
def ListCategories_ApiView(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        json = Categories_Serializer(categories, many=True).data
        return Response(data=json)

    if request.method == 'POST':
        name = request.data.get('name')
        category = Category.objects.create(
            name=name
        )
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Category successfully created',
                              'name': category.name})


@api_view(['GET', 'PUT', 'DELETE'])
def CategoryDetail_ApiView(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'message:' 'Категория не найдена!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        json = Categories_Serializer(category, many=False).data
        return Response(data=json)

    if request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_200_OK,
                        data={'message': 'Category successfully updated',
                              'name': category.name})

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'The Category was deleted'})


@api_view(['GET', 'POST'])
def ListProducts_ApiView(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        json = Product_Serializer(products, many=True).data
        return Response(data=json)
    if request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Product successfully created',
                              'title': product.title, 'description': product.description,
                              'price': product.price, 'category': product.category_id})


@api_view(['GET', 'PUT', 'DELETE'])
def ProductDetail_ApiView(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'message:' 'Продукт не найден!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        json = Product_Serializer(product, many=False).data
        return Response(data=json)
    if request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(status=status.HTTP_200_OK,
                        data={'message': 'Product successfully updated',
                              'title': product.title, 'description': product.description,
                              'price': product.price, 'category': product.category_id})
    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'The Product was deleted'})


@api_view(['GET', 'POST'])
def ListReviews_ApiView(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        json = Review_Serializer(reviews, many=True).data
        return Response(data=json)

    if request.method == 'POST':
        text = request.data.get('text')
        product_id = request.data.get('product_id')
        stars = request.data.get('stars')
        review = Review.objects.create(
            text=text,
            product_id=product_id,
            stars=stars
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Review successfully created',
                              'text': review.text,
                              'product_id': review.product_id,
                              'stars': review.stars})


@api_view(['GET', 'PUT','DELETE'])
def Review_ApiView(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'message:' 'Комментарий не найден!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        json = Review_Serializer(review, many=False).data
        return Response(data=json)
    if request.method == 'PUT':
        review.text = request.data.get('text')
        review.product_id = request.data.get('product_id')
        review.stars = request.data.get('stars')
        review.save()
        return Response(status=status.HTTP_200_OK,
                        data={'message': 'Review successfully updated',
                              'text': review.text, 'stars': review.stars,
                              'product_id': review.product_id})
    if request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'The Review was deleted'})


@api_view(['GET'])
def ProductReviewsList_ApiView(request):
    products_reviews = Product.objects.select_related('category').prefetch_related('product_review').all()
    json = ProductReviews_Serializer(products_reviews, many=True).data
    return Response(data=json)
