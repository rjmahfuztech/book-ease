from django.urls import path, include
from rest_framework import routers
from books.views import AuthorViewSet, BookViewSet

router = routers.DefaultRouter()

router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
