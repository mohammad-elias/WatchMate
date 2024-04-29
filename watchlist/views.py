from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import filters, pagination
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminOrReadOnly,ReviewerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import generics
# Create your views here.

class WatchListPagination(pagination.PageNumberPagination):
    page_size = 8
    page_size_query_param = page_size
    max_page_size = 100

class WatchListViewset(viewsets.ModelViewSet):
    serializer_class = serializers.WatchlistSerializer
    queryset = models.WatchList.objects.all()
    permission_classes = [AdminOrReadOnly]
    pagination_class = WatchListPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','category__name','release__year']


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    
    
class ReleaseViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ReleaseSerializer
    queryset = models.Release.objects.all()
    
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        content = models.WatchList.objects.get(pk=pk)
        user = self.request.user
        query = models.Review.objects.filter(reviewer=user,watchlist=content)
        if query.exists():
            raise ValidationError("You've already gives review for this content.")
        
        rating_count = content.total_rating
        rating_count += 1
        content.avg_rating = (content.avg_rating+serializer.validated_data['rating'])/rating_count
        content.total_rating = rating_count
        
        content.save()
        
        serializer.save(watchlist=content,reviewer=user)
    
    
class ReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watchlist=pk)



class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewerOrReadOnly]
    serializer_class =  serializers.ReviewSerializer
    queryset = models.Review.objects.all()
    
    
    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')
        
        review = models.Review.objects.get(pk=pk)
        content = review.watchlist
        
        rating_count = content.total_rating
        avg_rating = content.avg_rating-review.rating
        content.avg_rating = (avg_rating+serializer.validated_data['rating'])/rating_count
        review.rating = serializer.validated_data['rating']
        review.save()
        content.save()
        serializer.save()
        
    def perform_destroy(self, instance):
        pk = self.kwargs.get('pk')
        
        review = models.Review.objects.get(pk=pk)
        content = review.watchlist
        
        rating_count = content.total_rating
        avg_rating = content.avg_rating-review.rating
        content.avg_rating = (avg_rating)/rating_count
        content.total_rating -= 1
        
        content.save()
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)