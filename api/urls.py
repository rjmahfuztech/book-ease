from django.urls import path, include
from rest_framework import routers
from books.views import AuthorViewSet, BookViewSet
from borrow.views import BorrowRecordViewSet

router = routers.DefaultRouter()

router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='book')
router.register('borrow', BorrowRecordViewSet, basename='borrow')

urlpatterns = [
    path('', include(router.urls)),
]
