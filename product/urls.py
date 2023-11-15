from django.urls import path
from product import views

urlpatterns = [
    path('categories/', views.ListCreateCategoriesView.as_view()),
    path('categories/<int:id>/', views.RetriveCategoryView.as_view()),
    path('products/', views.ListProductsCreateView.as_view()),
    path('products/reviews/', views.ListProductReviewApiView.as_view()),
    path('products/<int:id>/', views.ProductRetriveApiView.as_view()),
    path('reviews/', views.ListReviewsApiView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailApiView.as_view()),
    path('tags/', views.ListTagsApiView.as_view()),
]
