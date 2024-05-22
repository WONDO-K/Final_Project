
from rest_framework import serializers

class RecommendProductsQuerySerializer(serializers.Serializer):
    age = serializers.IntegerField()
    wealth = serializers.IntegerField()
    salary = serializers.IntegerField()