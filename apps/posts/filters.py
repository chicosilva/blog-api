from django_filters import rest_framework as filters

from apps.posts.models import Post


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['title', 'author', 'status']
