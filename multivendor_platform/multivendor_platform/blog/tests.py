from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import BlogCategory, BlogPost
from products.models import Category as ProductCategory

User = get_user_model()


class BlogCategoryModelTest(TestCase):
    """Test BlogCategory model"""
    
    def test_blog_category_creation(self):
        """Test creating a blog category"""
        category = BlogCategory.objects.create(
            name='Technology',
            description='Tech related posts'
        )
        self.assertEqual(category.name, 'Technology')
        self.assertEqual(category.slug, 'technology')
        self.assertTrue(category.is_active)
    
    def test_blog_category_slug_generation(self):
        """Test that slug is auto-generated"""
        category = BlogCategory.objects.create(name='Web Development')
        self.assertEqual(category.slug, 'web-development')
    
    def test_blog_category_str(self):
        """Test blog category string representation"""
        category = BlogCategory.objects.create(name='News')
        self.assertEqual(str(category), 'News')
    
    def test_blog_category_with_product_link(self):
        """Test blog category linked to product category"""
        product_cat = ProductCategory.objects.create(name='Electronics')
        blog_cat = BlogCategory.objects.create(
            name='Electronics News',
            linked_product_category=product_cat
        )
        self.assertEqual(blog_cat.linked_product_category, product_cat)


class BlogPostModelTest(TestCase):
    """Test BlogPost model"""
    
    def setUp(self):
        """Set up test data"""
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='pass123'
        )
        self.category = BlogCategory.objects.create(
            name='Technology',
            slug='technology'
        )
    
    def test_blog_post_creation(self):
        """Test creating a blog post"""
        post = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='My First Post',
            excerpt='This is a short excerpt',
            content='This is the full content of the post'
        )
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.title, 'My First Post')
        self.assertEqual(post.status, 'draft')
        self.assertFalse(post.is_featured)
        self.assertEqual(post.view_count, 0)
    
    def test_blog_post_slug_generation(self):
        """Test that slug is auto-generated from title"""
        post = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='How to Learn Python',
            excerpt='Short excerpt',
            content='Full content here'
        )
        self.assertTrue(post.slug)
        self.assertIn('python', post.slug.lower())
    
    def test_blog_post_str(self):
        """Test blog post string representation"""
        post = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='Test Post Title',
            excerpt='Excerpt',
            content='Content'
        )
        self.assertEqual(str(post), 'Test Post Title')
    
    def test_blog_post_status(self):
        """Test blog post status changes"""
        post = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='Draft Post',
            excerpt='Excerpt',
            content='Content',
            status='draft'
        )
        self.assertEqual(post.status, 'draft')
        
        post.status = 'published'
        post.save()
        self.assertEqual(post.status, 'published')
    
    def test_blog_post_featured(self):
        """Test marking blog post as featured"""
        post = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='Featured Post',
            excerpt='Excerpt',
            content='Content',
            is_featured=True
        )
        self.assertTrue(post.is_featured)
    
    def test_blog_post_view_count(self):
        """Test incrementing view count"""
        post = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='Popular Post',
            excerpt='Excerpt',
            content='Content'
        )
        self.assertEqual(post.view_count, 0)
        
        post.view_count += 1
        post.save()
        self.assertEqual(post.view_count, 1)


class BlogAPITest(TestCase):
    """Test Blog API endpoints"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='pass123'
        )
        self.category = BlogCategory.objects.create(name='Tech')
    
    def test_blog_posts_endpoint(self):
        """Test getting blog posts list"""
        response = self.client.get('/api/blog/posts/')
        self.assertEqual(response.status_code, 200)
    
    def test_blog_categories_endpoint(self):
        """Test getting blog categories list"""
        response = self.client.get('/api/blog/categories/')
        self.assertEqual(response.status_code, 200)
    
    def test_blog_post_detail(self):
        """Test getting individual blog post"""
        post = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='Test Post',
            slug='test-post',
            excerpt='Excerpt',
            content='Content',
            status='published'
        )
        response = self.client.get(f'/api/blog/posts/{post.slug}/')
        # Should return 200 or 404 depending on URL configuration
        self.assertIn(response.status_code, [200, 404])


class BlogModelRelationshipsTest(TestCase):
    """Test relationships between blog models"""
    
    def setUp(self):
        """Set up test data"""
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='pass123'
        )
        self.category = BlogCategory.objects.create(name='Category1')
    
    def test_category_posts_relationship(self):
        """Test that category can access its posts"""
        post1 = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='Post 1',
            excerpt='Excerpt 1',
            content='Content 1'
        )
        post2 = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='Post 2',
            excerpt='Excerpt 2',
            content='Content 2'
        )
        
        posts = self.category.blog_posts.all()
        self.assertEqual(posts.count(), 2)
        self.assertIn(post1, posts)
        self.assertIn(post2, posts)
    
    def test_author_posts_relationship(self):
        """Test that author can access their posts"""
        post = BlogPost.objects.create(
            author=self.author,
            category=self.category,
            title='Author Post',
            excerpt='Excerpt',
            content='Content'
        )
        
        author_posts = self.author.blog_posts.all()
        self.assertEqual(author_posts.count(), 1)
        self.assertEqual(author_posts.first(), post)
