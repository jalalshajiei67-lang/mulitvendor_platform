# blog/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from tinymce.widgets import TinyMCE
from .models import BlogPost, BlogCategory, BlogComment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_display', 'linked_product_category', 'post_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'linked_product_category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['linked_subcategories']  # Better UI for ManyToMany fields
    actions = ['delete_selected']  # Include delete action
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'color', 'is_active')
        }),
        ('Product Category Link', {
            'fields': ('linked_product_category',),
            'description': 'Optional: Link this blog category to a product category'
        }),
        ('Subcategories', {
            'fields': ('linked_subcategories',),
            'description': 'Select multiple subcategories to link this blog category to product subcategories'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_display(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'
    
    def post_count(self, obj):
        return obj.blog_posts.filter(status='published').count()
    post_count.short_description = 'Published Posts'
    
    def has_delete_permission(self, request, obj=None):
        """Explicitly allow delete permission"""
        return True
    
    class Media:
        js = ('admin/js/fix_action_button.js', 'admin/js/tinymce_image_picker.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="Blog post content with rich text formatting"
    )
    
    # Custom field for display_locations with checkboxes
    display_locations = forms.MultipleChoiceField(
        choices=BlogPost.DISPLAY_LOCATION_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select where this post should be displayed. You can select multiple locations. "
                  "For seller education, check 'Seller Education'. For buyer education, check 'Buyer Education'."
    )
    
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert JSONField value to list for checkbox widget
        if self.instance and self.instance.pk:
            # If editing existing post, convert display_locations from JSON to list
            if self.instance.display_locations:
                self.initial['display_locations'] = self.instance.display_locations
            else:
                self.initial['display_locations'] = ['main_blog']  # Default
        else:
            # For new posts, default to main_blog
            self.initial['display_locations'] = ['main_blog']
    
    def clean_display_locations(self):
        """Clean and validate display_locations"""
        locations = self.cleaned_data.get('display_locations', [])
        # If no location selected, default to main_blog
        if not locations:
            return ['main_blog']
        return locations
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Save display_locations as JSON
        instance.display_locations = self.cleaned_data.get('display_locations', ['main_blog'])
        if commit:
            instance.save()
            # Save many-to-many relationships if any
            self.save_m2m()
        return instance

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'display_locations_display', 'view_count', 'created_at', 'published_at']
    list_filter = ['status', 'is_featured', 'category', 'author', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'published_at']
    raw_id_fields = ['author']
    filter_horizontal = ['linked_subcategories']  # Better UI for ManyToMany fields
    actions = ['delete_selected']  # Include delete action
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('Subcategories', {
            'fields': ('linked_subcategories',),
            'description': 'Select multiple subcategories to link this blog post to product subcategories'
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_locations'),
            'description': '📍 <strong>Display Locations:</strong> Select where this post should be displayed. '
                          'Check "Seller Education" to show in seller dashboard education section. '
                          'Check "Buyer Education" to show in buyer dashboard education section. '
                          'You can select multiple locations. Posts default to "Main Blog" if none selected.'
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_locations_display(self, obj):
        """Display display_locations as readable badges in list view"""
        if not obj.display_locations:
            return format_html('<span style="color: #999;">—</span>')
        
        location_names = {
            'main_blog': ('Main Blog', '#2196F3'),
            'seller_education': ('Seller Education', '#FF9800'),
            'buyer_education': ('Buyer Education', '#4CAF50')
        }
        
        badges = []
        for loc in obj.display_locations:
            name, color = location_names.get(loc, (loc, '#757575'))
            badges.append(
                format_html(
                    '<span style="background-color: {}; color: white; padding: 2px 8px; '
                    'border-radius: 12px; font-size: 11px; margin-left: 4px;">{}</span>',
                    color,
                    name
                )
            )
        
        return format_html(''.join(badges))
    display_locations_display.short_description = 'Display Locations'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def has_delete_permission(self, request, obj=None):
        """Explicitly allow delete permission"""
        return True
    
    class Media:
        js = ('admin/js/fix_action_button.js', 'admin/js/tinymce_image_picker.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post__category']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['post', 'author', 'parent']
    
    actions = ['approve_comments', 'disapprove_comments', 'delete_selected']  # Include delete action
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments were approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def disapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments were disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'
    
    def has_delete_permission(self, request, obj=None):
        """Explicitly allow delete permission"""
        return True
    
    class Media:
        js = ('admin/js/fix_action_button.js', 'admin/js/tinymce_image_picker.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }