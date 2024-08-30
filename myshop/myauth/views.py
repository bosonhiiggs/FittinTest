from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from h11 import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from myauth.serializer import RegisterSerializer


# Create your views here.
def hello(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello world')


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Логика по очистке данных токена
        ...

