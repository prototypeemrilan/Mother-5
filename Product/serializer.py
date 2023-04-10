from django.db.models import Avg
from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError
# =================================================================================
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars product_id'.split()
# =================================================================================
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price description category_name'.split()
# =================================================================================
class CategorySerializer(serializers.ModelSerializer):
    product_count = ProductSerializer
    class Meta:
        model = Category
        fields = 'name product_count'.split()
# =================================================================================
class ReviewProductSerializer(serializers.Serializer):
    average_rating = serializers.SerializerMethodField()
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=150)
    reviews = ReviewSerializer(many=True)

    def get_average_rating(self, obj):
        avg_rating = obj.reviews.aggregate(avg_rating=Avg('stars'))['avg_rating']
        return round(avg_rating, 2) if avg_rating is not None else 0.0

# =================================================================================
# =================================================================================

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False, default='Нет описания!')
    price = serializers.IntegerField(required=True)
    category_id = serializers.IntegerField(required=False, default='Не указано!')

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(f'Category with id {category_id} not found!')
        return category_id
# =================================================================================
class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
# =================================================================================
class ReviewValidateSerializer(serializers.Serializer):
    stars = serializers.IntegerField()
    text = serializers.CharField()
    product_id = serializers.IntegerField(required=True)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Такого продукта не существует!')
        return product_id


