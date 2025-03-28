from django.db import models
from books.models import Book
from users.models import Member

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrow')
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.first_name}"