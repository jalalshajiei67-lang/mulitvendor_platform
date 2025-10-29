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
    actions = ['delete_selected']  # Include delete action
    
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
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="Blog post content with rich text formatting"
    )
    
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'view_count', 'created_at', 'published_at']
    list_filter = ['status', 'is_featured', 'category', 'author', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'published_at']
    raw_id_fields = ['author']
    actions = ['delete_selected']  # Include delete action
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Settings', {
            'fields': ('is_featured', 'meta_title', 'meta_description')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

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
    
    class Media:
        js = ('admin/js/fix_action_button.js',)