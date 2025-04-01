from rest_framework import serializers
from books.models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography']

class BookAddUpdateSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_id', 'isbn', 'category', 'availability_status']
        read_only_fields = ['availability_status']

    def validate_author_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('Author id must be 1 or bigger')
        elif not Author.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'Author with Id {value} does not exists')
        return value
    
    def validate_isbn(self, value):
        if self.instance: # when try to update
            if Book.objects.exclude(id=self.instance.id).filter(isbn=value).exists():
                raise serializers.ValidationError('A book with this ISBN already exists.')
        else:
            if Book.objects.filter(isbn=value).exists():
                raise serializers.ValidationError('A book with this ISBN already exists.')
        return value

    def create(self, validated_data):
        author_id = validated_data.pop('author_id')
        return Book.objects.create(author_id=author_id, **validated_data)


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'category', 'availability_status']
        read_only_fields = ['availability_status']