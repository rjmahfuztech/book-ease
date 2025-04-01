from django.shortcuts import render
from books.serializers import AuthorSerializer, BookSerializer, BookAddUpdateSerializer
from rest_framework import viewsets
from books.models import Author, Book
from api.permissions import IsAdminOrReadOnly
from drf_yasg.utils import swagger_auto_schema


class AuthorViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'put', 'options']

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Get a list of Authors',
        operation_description='Any user can get or see all the available Author'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a Author by Admin',
        operation_description='Only Admin can create or add a Author'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific Author',
        operation_description='Any user can retrieve any specific Author'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update a specific Author by Admin',
        operation_description='Only Admin can update any specific Author information'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific Author by Admin',
        operation_description='Only Admin can Delete any specific Author'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BookViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'put', 'options']

    queryset = Book.objects.select_related('author').all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return BookAddUpdateSerializer
        return BookSerializer

    @swagger_auto_schema(
        operation_summary='Get a list of Books',
        operation_description='Any user can get or see all the available Books'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a Book by Admin',
        operation_description='Only Admin can create or add Books'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific Book',
        operation_description='Any user can retrieve any specific Book'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update a specific Book by Admin',
        operation_description='Only Admin can update any specific Book information'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific Book by Admin',
        operation_description='Only Admin can Delete any specific Book'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
