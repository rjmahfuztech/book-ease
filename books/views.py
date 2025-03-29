from django.shortcuts import render
from books.serializers import AuthorSerializer, BookSerializer
from rest_framework import viewsets
from books.models import Author, Book
from api.permissions import IsAdminOrReadOnly


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
