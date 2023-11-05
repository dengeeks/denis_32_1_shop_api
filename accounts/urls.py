from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/',views.SignUpApiView),
    path('login/',views.LoginApiView),
    path('confirm/',views.ConfirmApiView)
]

