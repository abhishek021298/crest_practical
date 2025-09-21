from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from django.http import HttpResponse
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
# from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from openpyxl import Workbook
import io

from .models import Product
from .serializers import ProductSerializer, BulkProductCreateSerializer
from .permissions import IsAdminOrReadOnly

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'price_min', 'price_max', 'is_active']

# @method_decorator(ratelimit(key='user', rate='100/h'), name='dispatch')
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_on', 'updated_on', 'price']
    ordering = ['-created_on']

# @method_decorator(ratelimit(key='user', rate='100/h'), name='dispatch')
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'message': 'Product deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)

# @method_decorator(ratelimit(key='user', rate='50/h'), name='patch')
class ProductDisableView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    @swagger_auto_schema(
        operation_description="Disable a product by setting is_active to False",
        tags=['Products']
    )
    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.is_active = False
            product.save()
            return Response({'message': 'Product disabled successfully'})
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

# @method_decorator(ratelimit(key='user', rate='20/h'), name='get')
class ProductSearchView(APIView):
    @swagger_auto_schema(
        operation_description="Search products by keyword",
        tags=['Products']
    )
    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            products = Product.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query),
                is_active=True
            )
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        return Response([])

# @method_decorator(ratelimit(key='user', rate='10/h'), name='post')
class BulkProductCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    @swagger_auto_schema(
        operation_description="Create multiple products",
        request_body=BulkProductCreateSerializer,
        tags=['Products']
    )
    def post(self, request):
        serializer = BulkProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            products = serializer.save()
            return Response({
                'message': f'{len(products)} products created successfully',
                'products': ProductSerializer(products, many=True).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(ratelimit(key='user', rate='5/h'), name='get')
class ProductExportView(APIView):
    @swagger_auto_schema(
        operation_description="Export all products to Excel",
        tags=['Products']
    )
    def get(self, request):
        wb = Workbook()
        ws = wb.active
        ws.title = "Products"
        
        headers = ['ID', 'Title', 'Description', 'Price', 'Discount', 'SSN', 'Is Active', 'Created On']
        ws.append(headers)
        
        products = Product.objects.all()
        for product in products:
            row = [
                str(product.id), product.title, product.description,
                float(product.price), float(product.discount), product.ssn,
                product.is_active, product.created_on.strftime('%Y-%m-%d %H:%M:%S')
            ]
            ws.append(row)
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'
        
        virtual_workbook = io.BytesIO()
        wb.save(virtual_workbook)
        virtual_workbook.seek(0)
        response.write(virtual_workbook.getvalue())
        
        return response