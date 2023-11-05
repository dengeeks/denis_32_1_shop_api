from django.urls import path
from product import views

urlpatterns = [
    path('categories/', views.ListCategories_ApiView),
    path('categories/<int:id>/', views.CategoryDetail_ApiView),
    path('products/', views.ListProducts_ApiView),
    path('products/reviews/',views.ProductReviewsList_ApiView),
    path('products/<int:id>/', views.ProductDetail_ApiView),
    path('reviews/', views.ListReviews_ApiView),
    path('reviews/<int:id>/', views.Review_ApiView),
    path('tags/',views.ListTagsView),
]
