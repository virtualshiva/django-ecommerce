
import django_filters
from demo_app.models import Product
from django_filters import CharFilter

class ProductFilter(django_filters.FilterSet):
    productname_contains = CharFilter(field_name='product_name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ''
        exclude = ['product_price', 'product_description', 'product_image', 'category', 'created_at', 'stock']