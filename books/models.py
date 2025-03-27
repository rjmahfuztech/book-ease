from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=150)
    biography = models.TextField()

    def __str__(self):
        return f"Author {self.name}"
    

class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book')
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')
    category = models.CharField(max_length=200)
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        return self.title
