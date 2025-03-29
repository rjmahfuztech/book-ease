from django.shortcuts import render
from rest_framework import viewsets, response, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from borrow.serializers import BorrowRecordSerializer, EmptySerializer
from borrow.models import BorrowRecord
from rest_framework.decorators import action
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema


class BorrowRecordViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'delete', 'options']
    
    def get_serializer_class(self):
        if self.action == 'return_book':
            return EmptySerializer
        return BorrowRecordSerializer
    
    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    
    def get_queryset(self):
        if self.request.user.is_staff:
            return BorrowRecord.objects.select_related('book__author', 'member').all()
        return BorrowRecord.objects.select_related('book__author', 'member').filter(member=self.request.user, return_date__isnull=True)

    def perform_create(self, serializer):
        borrow_record = serializer.save(member=self.request.user)
        book = borrow_record.book
        book.availability_status = False
        book.save()

    @swagger_auto_schema(
        operation_summary='Return a specific BorrowRecord by Member',
        operation_description='Only authenticated Member can return any books that they borrowed'
    )
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        
        try:
            borrow_record = BorrowRecord.objects.get(id=pk, return_date__isnull=True)
        except BorrowRecord.DoesNotExist:
            return response.Response(f"Sorry! This borrow record not found or already returned!")
        
        if borrow_record.member != request.user:
            return response.Response({'error': 'You can only return books you borrowed!'}, status=status.HTTP_403_FORBIDDEN)
        
        borrow_record.return_date = timezone.now()
        borrow_record.save()

        # change book availability_status to True
        borrow_record.book.availability_status = True
        borrow_record.book.save()

        return response.Response({'message': f"{borrow_record.book.title} returned successful."}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='Get a list of BorrowRecords',
        operation_description='Admin can see all the BorrowRecords but User can see only his/her borrowed records'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Borrow a Book by Member',
        operation_description='Any authenticated member can borrow any available books that are not borrowed'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific BorrowRecord',
        operation_description='Any authenticated member can retrieve any specific BorrowRecord'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific BorrowRecord by Admin',
        operation_description='Only Admin can Delete any specific BorrowRecord'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)