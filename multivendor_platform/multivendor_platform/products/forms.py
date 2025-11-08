# multivendor_platform/products/forms.py

from django import forms
from .models import Product, Subcategory, Category, Department

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Fields to include in the form
        fields = ['name', 'supplier', 'subcategories', 'description', 'price', 'stock', 'image', 'is_active', 'meta_title', 'meta_description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders and styling to form fields
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter product name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter a detailed description'})
        self.fields['price'].widget.attrs.update({'placeholder': '0.00'})
        self.fields['stock'].widget.attrs.update({'placeholder': '0'})
        self.fields['meta_title'].widget.attrs.update({'placeholder': 'SEO title (max 60 characters)'})
        self.fields['meta_description'].widget.attrs.update({'placeholder': 'SEO description (max 160 characters)'})
        
        # Filter subcategories to only show active ones
        self.fields['subcategories'].queryset = Subcategory.objects.filter(is_active=True)
        
        # Add Bootstrap classes for better styling (optional, but recommended)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'departments', 'subcategories', 'is_active', 'sort_order', 'meta_title', 'meta_description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departments'].queryset = Department.objects.filter(is_active=True)
        self.fields['subcategories'].queryset = Subcategory.objects.filter(is_active=True)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'description', 'image', 'categories', 'is_active', 'sort_order', 'meta_title', 'meta_description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(is_active=True)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'image', 'is_active', 'sort_order', 'meta_title', 'meta_description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
