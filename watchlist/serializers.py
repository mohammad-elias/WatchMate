from rest_framework import serializers
from .models import Category,WatchList,Release,Review

class WatchlistSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True,read_only=True)
    category = serializers.StringRelatedField(many=True)
    release = serializers.StringRelatedField()
    class Meta:
        model = WatchList
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        

class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField()
    class Meta:
        model = Review
        exclude = ('watchlist',)