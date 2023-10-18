from rest_framework.response import Response
from product.models import Category, Product, Review
from rest_framework.decorators import api_view
from product.serializers import Categories_Serializer, Product_Serializer, Review_Serializer
from rest_framework import status


# Create your views here.

@api_view(['GET'])
def ListCategories_ApiView(request):
    categories = Category.objects.all()
    json = Categories_Serializer(categories, many=True).data
    return Response(data=json)


@api_view(['GET'])
def CategoryDetail_ApiView(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'message:' 'Категория не найдена!'}, status=status.HTTP_404_NOT_FOUND)
    json = Categories_Serializer(category, many=False).data
    return Response(data=json)


@api_view(['GET'])
def ListProducts_ApiView(request):
    products = Product.objects.all()
    json = Product_Serializer(products, many=True).data
    return Response(data=json)


@api_view(['GET'])
def ProductDetail_ApiView(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'message:' 'Продукт не найден!'}, status=status.HTTP_404_NOT_FOUND)
    json = Product_Serializer(product, many=False).data
    return Response(data=json)


@api_view(['GET'])
def ListReviews_ApiView(request):
    reviews = Review.objects.all()
    json = Review_Serializer(reviews, many=True).data
    return Response(data=json)


@api_view(['GET'])
def Review_ApiView(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'message:' 'Комментарий не найден!'}, status=status.HTTP_404_NOT_FOUND)
    json = Review_Serializer(review, many=False).data
    return Response(data=json)
