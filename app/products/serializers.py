from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'created_on', 'updated_on')

class BulkProductCreateSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)

    def create(self, validated_data):
        products_data = validated_data['products']
        products = [Product(**product_data) for product_data in products_data]
        return Product.objects.bulk_create(products)