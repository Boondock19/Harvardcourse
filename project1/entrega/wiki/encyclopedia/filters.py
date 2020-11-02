import django_filters

from .models import search
from django_filters import CharFilter

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model=search
        fields='__all__'
        title= CharFilter(lookup_expr='icontains')
