from django.contrib import admin
from books.models import Book, Author

admin.site.register(Author)
admin.site.register(Book)