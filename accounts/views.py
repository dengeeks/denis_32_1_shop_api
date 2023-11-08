from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.serializers import *
from accounts.models import ConfirmUser
from rest_framework import generics


# Create your views here.

class SignUpCreateApiView(generics.CreateAPIView):
    serializer_class = CreateAccountValidate

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            user.is_active = False
            user.save()
            confirm = ConfirmUser.objects.create(user_id=user.id)
            confirm.send_email()
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': 'Account was successfully created',
                                  'user': user.id})
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)


# @api_view(['POST'])
# def SignUpApiView(request):
#     serializer = CreateAccountValidate(data=request.data)
#     if serializer.is_valid():
#         user = User.objects.create_user(**serializer.validated_data)
#         user.is_active = False
#         user.save()
#         confirm = ConfirmUser.objects.create(user_id=user.id)
#         confirm.send_email()
#         return Response(status=status.HTTP_201_CREATED,
#                         data={'message': 'Account was successfully created',
#                               'user': user.id})
#     else:
#         return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                         data=serializer.errors)

class LoginApiView(generics.CreateAPIView):
    serializer_class = LoginValidateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(data={'message': 'Successfully authorized',
                                      'token': token.key})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={'message_error': 'unauthorized'})


# @api_view(['POST'])
# def LoginApiView(request):
#     serializer = LoginValidateSerializer(data=request.data)
#     if serializer.is_valid():
#         user = authenticate(**serializer.validated_data)
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response(data={'message': 'Successfully authorized',
#                                   'token': token.key})
#         else:
#             return Response(status=status.HTTP_401_UNAUTHORIZED,
#                             data={'message_error': 'unauthorized'})


class ConfirmApiView(generics.CreateAPIView):
    serializer_class = ConfirmUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            ConfirmUser.objects.get(code=serializer.validated_data['code']).delete()
            serializer.user.is_active = True
            serializer.user.save()
            return Response(status=status.HTTP_202_ACCEPTED,
                            data={'message': 'You are registered'})
        else:
            return Response(data={"message": serializer.errors})


# @api_view(['POST'])
# def ConfirmApiView(request):
#     serializer = ConfirmUserSerializer(data=request.data)
#     if serializer.is_valid():
#         ConfirmUser.objects.get(code=serializer.validated_data['code']).delete()
#         serializer.user.is_active = True
#         serializer.user.save()
#         return Response(status=status.HTTP_202_ACCEPTED,
#                         data={'message': 'You are registered'})
#     else:
#         return Response(data={"message": serializer.errors})
