from rest_framework.response import Response
from product.models import Category, Product, Review, Tag
from rest_framework.decorators import api_view
from product.serializers import Categories_Serializer, Product_Serializer, Review_Serializer, ProductReviews_Serializer, \
    CategoryValidateSerializer, ProductValidateSerializer, ReviewValidatedSerializer, TagListSerializer, \
    TagValidateSerializer
from rest_framework import status
from rest_framework import generics


# Create your views here.
class ListCreateCategoriesView(generics.ListCreateAPIView):
    serializer_class = Categories_Serializer
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'message': serializer.errors})
        name = serializer.validated_data.get('name')
        category = Category.objects.create(
            name=name
        )
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Category successfully created',
                              'name': category.name})

    # @api_view(['GET', 'POST'])
    # def ListCategories_ApiView(request):
    #     if request.method == 'GET':
    #         categories = Category.objects.all()
    #         json = Categories_Serializer(categories, many=True).data
    #         return Response(data=json)
    # if request.method == 'POST':
    #     serializer = CategoryValidateSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(data={'message': serializer.errors})
    #     name = serializer.validated_data.get('name')
    #     category = Category.objects.create(
    #         name=name
    #     )
    #     category.save()
    #     return Response(status=status.HTTP_201_CREATED,
    #                     data={'message': 'Category successfully created',
    #                           'name': category.name})


class RetriveCategoryView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Categories_Serializer
    queryset = Category.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid():
            category = self.get_object()
            category.name = serializer.validated_data.get('name')
            category.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': 'Category successfully updated',
                                  'name': category.name})
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={"message": serializer.errors})


# @api_view(['GET', 'PUT', 'DELETE'])
# def CategoryDetail_ApiView(request, id):
#     try:
#         category = Category.objects.get(id=id)
#     except Category.DoesNotExist:
#         return Response(data={'message:' 'Категория не найдена!'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         json = Categories_Serializer(category, many=False).data
#         return Response(data=json)
#     if request.method == 'PUT':
#         serializer = CategoryValidateSerializer(data=request.data)
#         if serializer.is_valid():
#             category.name = serializer.validated_data.get('name')
#             category.save()
#             return Response(status=status.HTTP_201_CREATED,
#                             data={'message': 'Category successfully updated',
#                                   'name': category.name})
#         return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                         data={"message": serializer.errors})
#     if request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT,
#                         data={'message': 'The Category was deleted'})

class ListProductsCreateView(generics.ListCreateAPIView):
    serializer_class = Product_Serializer
    queryset = Product.objects.select_related('category').all()

    def post(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create(**serializer.create_validated_data())
            product.tags.set(serializer.validated_data.get('tags'))
            product.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': 'Product successfully created',
                                  "product": serializer.data})
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data=serializer.errors)


# @api_view(['GET', 'POST'])
# def ListProducts_ApiView(request):
#     if request.method == 'GET':
#         products = Product.objects.select_related('category').all()
#         json = Product_Serializer(products, many=True).data
#         return Response(data=json)
#     if request.method == 'POST':
#         serializer = ProductValidateSerializer(data=request.data)
#         if serializer.is_valid():
#             product = Product.objects.create(**serializer.create_validated_data())
#             product.tags.set(serializer.validated_data.get('tags'))
#             product.save()
#             return Response(status=status.HTTP_201_CREATED,
#                             data={'message': 'Product successfully created',
#                                   "product": serializer.data})
#         return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                         data=serializer.errors)

class ProductRetriveApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Product_Serializer
    queryset = Product.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid():
            product = self.get_object()
            product.title = serializer.validated_data.get('title')
            product.description = serializer.validated_data.get('description')
            product.price = serializer.validated_data.get('price')
            product.category_id = serializer.validated_data.get('category_id')
            product.tags.set(serializer.validated_data.get('tags'))
            product.save()
            return Response(status=status.HTTP_200_OK,
                            data={'message': 'Product successfully updated',
                                  'product': serializer.data})
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'message': serializer.errors})


# @api_view(['GET', 'PUT', 'DELETE'])
# def ProductDetail_ApiView(request, id):
#     try:
#         product = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         return Response(data={'message:' 'Продукт не найден!'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         json = Product_Serializer(product, many=False).data
#         return Response(data=json)
#     if request.method == 'PUT':
#         serializer = ProductValidateSerializer(data=request.data)
#         if serializer.is_valid():
#             product.title = serializer.validated_data.get('title')
#             product.description = serializer.validated_data.get('description')
#             product.price = serializer.validated_data.get('price')
#             product.category_id = serializer.validated_data.get('category_id')
#             product.tags.set(serializer.validated_data.get('tags'))
#             product.save()
#             return Response(status=status.HTTP_200_OK,
#                             data={'message': 'Product successfully updated',
#                                   'product': serializer.data})
#         else:
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data={'message': serializer.errors})
#     if request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT,
#                         data={'message': 'The Product was deleted'})


class ListReviewsApiView(generics.ListCreateAPIView):
    serializer_class = Review_Serializer
    queryset = Review.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = ReviewValidatedSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data.get('text')
            product_id = serializer.validated_data.get('product_id')
            stars = serializer.validated_data.get('stars')
            review = Review.objects.create(
                text=text,
                product_id=product_id,
                stars=stars
            )
            review.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': 'Review successfully created',
                                  'review': serializer.data})
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"message": serializer.errors})

# @api_view(['GET', 'POST'])
# def ListReviews_ApiView(request):
#     if request.method == 'GET':
#         reviews = Review.objects.all()
#         json = Review_Serializer(reviews, many=True).data
#         return Response(data=json)
#     if request.method == 'POST':
#         serializer = ReviewValidatedSerializer(data=request.data)
#         if serializer.is_valid():
#             text = serializer.validated_data.get('text')
#             product_id = serializer.validated_data.get('product_id')
#             stars = serializer.validated_data.get('stars')
#             review = Review.objects.create(
#                 text=text,
#                 product_id=product_id,
#                 stars=stars
#             )
#             review.save()
#             return Response(status=status.HTTP_201_CREATED,
#                             data={'message': 'Review successfully created',
#                                   'review': serializer.data})
#         else:
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data={"message": serializer.errors})
#

class ReviewDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Review_Serializer
    queryset = Review.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        serializer = ReviewValidatedSerializer(data=request.data)
        if serializer.is_valid():
            review = self.get_object()
            review.text = serializer.validated_data.get('text')
            review.product_id = serializer.validated_data.get('product_id')
            review.stars = serializer.validated_data.get('stars')
            review.save()
            return Response(status=status.HTTP_200_OK,
                            data={'message': 'Review successfully updated',
                                  'review': serializer.data})
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"message": serializer.errors})

# @api_view(['GET', 'PUT', 'DELETE'])
# def Review_ApiView(request, id):
#     try:
#         review = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response(data={'message:' 'Комментарий не найден!'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         json = Review_Serializer(review, many=False).data
#         return Response(data=json)
#     if request.method == 'PUT':
#         serializer = ReviewValidatedSerializer(data=request.data)
#         if serializer.is_valid():
#             review.text = serializer.validated_data.get('text')
#             review.product_id = serializer.validated_data.get('product_id')
#             review.stars = serializer.validated_data.get('stars')
#             review.save()
#             return Response(status=status.HTTP_200_OK,
#                             data={'message': 'Review successfully updated',
#                                   'review': serializer.data})
#         else:
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data={"message": serializer.errors})
#     if request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT,
#                         data={'message': 'The Review was deleted'})


class ListProductReviewApiView(generics.ListAPIView):
    serializer_class = ProductReviews_Serializer
    queryset = Product.objects.select_related('category').prefetch_related('product_review').all()

# @api_view(['GET'])
# def ProductReviewsList_ApiView(request):
#     products_reviews = Product.objects.select_related('category').prefetch_related('product_review').all()
#     json = ProductReviews_Serializer(products_reviews, many=True).data
#     return Response(data=json)

class ListTagsApiView(generics.ListCreateAPIView):
    serializer_class = TagListSerializer
    queryset = Tag.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = TagValidateSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            tags = Tag.objects.create(
                name=name
            )
            tags.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': 'Tag successfully created',
                                  'Tag': serializer.data})
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"message": serializer.errors})


# @api_view(['GET', 'POST'])
# def ListTagsView(request):
#     if request.method == 'GET':
#         tags = Tag.objects.all()
#         json = TagListSerializer(tags, many=True).data
#         return Response(json)
#     if request.method == 'POST':
#         serializer = TagValidateSerializer(data=request.data)
#         if serializer.is_valid():
#             name = serializer.validated_data.get('name')
#             tags = Tag.objects.create(
#                 name=name
#             )
#             tags.save()
#             return Response(status=status.HTTP_201_CREATED,
#                             data={'message': 'Tag successfully created',
#                                   'Tag': serializer.data})
#         else:
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data={"message": serializer.errors})
