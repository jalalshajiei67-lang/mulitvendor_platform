# products/admin_filters.py
from django.contrib import admin
from django.db.models import Q


class SearchableRelatedFieldListFilter(admin.RelatedFieldListFilter):
    """
    A custom filter that adds search functionality to related field filters.
    """
    template = 'admin/searchable_filter.html'
    
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.search_param = f'{self.lookup_kwarg}_search'
        self.search_term = request.GET.get(self.search_param, '')
    
    def choices(self, changelist):
        # Get base choices
        for choice in super().choices(changelist):
            yield choice
    
    def queryset(self, request, queryset):
        # Apply search filter if search term exists
        if self.search_term:
            lookup = f'{self.field_path}__name__icontains'
            queryset = queryset.filter(**{lookup: self.search_term})
        return super().queryset(request, queryset)
    
    def expected_parameters(self):
        return super().expected_parameters() + [self.search_param]


class SubcategorySearchFilter(admin.RelatedFieldListFilter):
    """Custom filter for subcategories with search functionality"""
    template = 'admin/searchable_filter.html'
    
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.search_param = f'{field_path}_search'
        self.search_term = request.GET.get(self.search_param, '')
        super().__init__(field, request, params, model, model_admin, field_path)
    
    def expected_parameters(self):
        return super().expected_parameters() + [self.search_param]
    
    def choices(self, changelist):
        from .models import Subcategory
        
        # Get all subcategories
        lookup_choices = Subcategory.objects.filter(is_active=True)
        
        # Apply search filter
        if self.search_term:
            lookup_choices = lookup_choices.filter(name__icontains=self.search_term)
        
        lookup_choices = lookup_choices.order_by('name')
        
        # Yield "All" option
        yield {
            'selected': self.lookup_val is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull, self.search_param]),
            'display': 'All',
        }
        
        # Yield filtered choices
        for obj in lookup_choices:
            yield {
                'selected': str(obj.pk) == self.lookup_val,
                'query_string': changelist.get_query_string({self.lookup_kwarg: obj.pk}, [self.lookup_kwarg_isnull, self.search_param]),
                'display': obj.name,
            }


class CategorySearchFilter(admin.RelatedFieldListFilter):
    """Custom filter for categories with search functionality"""
    template = 'admin/searchable_filter.html'
    
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.search_param = f'{field_path}_search'
        self.search_term = request.GET.get(self.search_param, '')
        super().__init__(field, request, params, model, model_admin, field_path)
    
    def expected_parameters(self):
        return super().expected_parameters() + [self.search_param]
    
    def choices(self, changelist):
        from .models import Category
        
        # Get all categories
        lookup_choices = Category.objects.filter(is_active=True)
        
        # Apply search filter
        if self.search_term:
            lookup_choices = lookup_choices.filter(name__icontains=self.search_term)
        
        lookup_choices = lookup_choices.order_by('name')
        
        # Yield "All" option
        yield {
            'selected': self.lookup_val is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull, self.search_param]),
            'display': 'All',
        }
        
        # Yield filtered choices
        for obj in lookup_choices:
            yield {
                'selected': str(obj.pk) == self.lookup_val,
                'query_string': changelist.get_query_string({self.lookup_kwarg: obj.pk}, [self.lookup_kwarg_isnull, self.search_param]),
                'display': obj.name,
            }
