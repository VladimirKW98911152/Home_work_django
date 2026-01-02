from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category

class PostForm(forms.ModelForm):
    text = forms.CharField(
        min_length=50, 
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 80,
            'placeholder': 'Введите текст здесь...',
            'class': 'form-control'
        })
    )
    
    title = forms.CharField(
        max_length=128, 
        widget=forms.TextInput(attrs={
            'size': 80,
            'placeholder': 'Введите заголовок...',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'postCategory', 'title', 'text']
        widgets = {
            'postCategory': forms.CheckboxSelectMultiple(),
            'categoryType': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'author': 'Автор',
            'categoryType': 'Тип контента',
            'postCategory': 'Категории',
            'title': 'Заголовок',
            'text': 'Текст',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Настраиваем поле author для правильного отображения
        self.fields['author'].empty_label = "Выберите автора"
        self.fields['author'].label_from_instance = lambda obj: f"{obj.authorUser.username}"
        
        # Настраиваем поле postCategory для отображения названий
        self.fields['postCategory'].label_from_instance = lambda obj: f"{obj.name}"

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')

        if text and title and text == title:
            raise ValidationError("Заголовок не должен быть идентичен содержанию")
        return cleaned_data

    def clean_text(self):
        text = self.cleaned_data['text']
        if text and text[0].islower():
            raise ValidationError("Текст должен начинаться с заглавной буквы")
        return text

    def clean_title(self):
        title = self.cleaned_data['title']
        if title and title[0].islower():
            raise ValidationError("Заголовок должен начинаться с заглавной буквы")
        return title

class SubscribeForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите категории для подписки',
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all().order_by('name')
        self.fields['categories'].queryset = categories
        
        self.fields['categories'].choices = [
            (category.id, category.name) for category in categories
        ]
