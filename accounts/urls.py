from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/',views.SignUpCreateApiView.as_view()),
    path('login/',views.LoginApiView.as_view()),
    path('confirm/',views.ConfirmApiView.as_view())
]

