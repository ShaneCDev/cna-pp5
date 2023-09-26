from django import forms
from .models import Blog
from products.widgets import CustomClearableFileInput
from django.utils.text import slugify


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']

    image = forms.ImageField(label='image', required=False, widget=CustomClearableFileInput)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('title')
        slug = slugify(name)
        cleaned_data['slug'] = slug
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-0'
