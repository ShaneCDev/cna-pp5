from django import forms
from django.utils.text import slugify
from .models import Product, Category
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']

    image = forms.ImageField(label='image', required=False, widget=CustomClearableFileInput)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        slug = slugify(name)
        cleaned_data['slug'] = slug
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-0'


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['friendly_name', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-0'
