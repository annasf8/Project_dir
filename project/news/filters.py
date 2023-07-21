from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from django import forms

class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains', label='По заголовку')
    author__user__username = CharFilter(lookup_expr='icontains', label='По имени автора')
    time_create = DateFilter(field_name='time_create', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}), label='Позднее чем')

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'time_create']