from rest_framework import serializers
from borrow.models import BorrowRecord
from books.models import Book
from books.serializers import AuthorSerializer
from users.models import Member

class SimpleBookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category']

class SimpleMemberSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_full_name')
    class Meta:
        model = Member
        fields = ['id', 'name']

    def get_current_user_full_name(self, obj):
        return obj.get_full_name()


class BorrowRecordSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(write_only=True)
    book = SimpleBookSerializer(read_only=True)
    member = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'book_id', 'member', 'borrow_date', 'return_date']
        read_only_fields = ['book', 'member', 'return_date']

    def get_user(self, obj):
        return SimpleMemberSerializer(obj.member).data

    def validate_book_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(f'Book Id must be 1 or bigger')
        elif not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'Book with id {value} does not exists')
        elif Book.objects.filter(id=value, availability_status=False).exists():
            raise serializers.ValidationError('Sorry this book is already borrowed')
        
        return value
    
class EmptySerializer(serializers.Serializer):
    pass