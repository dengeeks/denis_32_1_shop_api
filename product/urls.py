from django.urls import path
from product import views

urlpatterns = [
    path('api/v1/categories/', views.ListCategories_ApiView),
    path('api/v1/categories/<int:id>/', views.CategoryDetail_ApiView),
    path('api/v1/products/', views.ListProducts_ApiView),
    path('api/v1/products/reviews/',views.ProductReviewsList_ApiView),
    path('api/v1/products/<int:id>/', views.ProductDetail_ApiView),
    path('api/v1/reviews/', views.ListReviews_ApiView),
    path('api/v1/reviews/<int:id>/', views.Review_ApiView),
    path('api/v1/tags/',views.ListTagsView),
]
