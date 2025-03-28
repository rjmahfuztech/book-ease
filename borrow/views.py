from django.shortcuts import render
from rest_framework import viewsets, response, status
from borrow.serializers import BorrowRecordSerializer, EmptySerializer
from borrow.models import BorrowRecord
from rest_framework.decorators import action
from django.utils import timezone


class BorrowRecordViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'delete', 'options']
    queryset = BorrowRecord.objects.select_related('book__author').all()

    def get_serializer_class(self):
        if self.action == 'return_book':
            return EmptySerializer
        return BorrowRecordSerializer

    def perform_create(self, serializer):
        borrow_record = serializer.save()
        book = borrow_record.book
        book.availability_status = False
        book.save()

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        
        try:
            borrow_record = BorrowRecord.objects.get(id=pk, return_date__isnull=True)
        except BorrowRecord.DoesNotExist:
            return response.Response(f"Sorry! This borrow record not found or already returned!")
        
        borrow_record.return_date = timezone.now()
        borrow_record.save()

        # change book availability_status to True
        borrow_record.book.availability_status = True
        borrow_record.book.save()

        return response.Response({'message': f"{borrow_record.book.title} returned successful."}, status=status.HTTP_200_OK)