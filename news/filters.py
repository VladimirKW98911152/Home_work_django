from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from django import forms
from .models import Post, Author

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='По заголовку',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите текст...',
            'class': 'form-control',
            'style': 'width: 100%;'
        })
    )

    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        empty_label="Все авторы",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%;'
        })
    )

    date_after = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        label='Дата после',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'style': 'width: 100%;'
        }),
        input_formats=['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y']
    )

    class Meta:
        model = Post
        fields = ['title', 'author']
