"""
Universal Product Scraper - Works with ANY e-commerce platform
Supports: WooCommerce, Shopify, Magento, Custom sites, and more
"""
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.utils.text import slugify
import re
import json
from urllib.parse import urljoin, urlparse
import logging
from .scraper_error_handler import (
    ErrorHandler, ErrorCategory, ErrorSeverity, ScraperError,
    handle_network_error, handle_parsing_error
)

logger = logging.getLogger(__name__)


class UniversalProductScraper:
    """
    Universal scraper that works with any e-commerce platform
    """
    
    # Configuration constants
    MIN_PAGE_LENGTH = 200
    MIN_DESCRIPTION_LENGTH = 30
    MAX_PRICE_VALUE = 999999999
    MAX_PRODUCT_IMAGES = 20
    IMAGE_DOWNLOAD_TIMEOUT = 30
    
    def __init__(self, url, verify_ssl=True, use_proxy=False):
        self.url = url
        self.soup = None
        self.response = None
        self.verify_ssl = verify_ssl
        self.use_proxy = use_proxy
        self.error_handler = ErrorHandler()
        self.platform = None  # Will be detected: woocommerce, shopify, custom, etc.
        
    def fetch_page(self):
        """
        Fetch the HTML content with robust error handling
        """
        if not self.verify_ssl:
            # Log warning but don't suppress globally
            logger.warning(f"SSL verification disabled for {self.url}")
            self.error_handler.add_warning(
                "SSL verification disabled",
                "Connecting without SSL verification"
            )
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8,ar;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            }
            
            session = requests.Session()
            session.trust_env = self.use_proxy
            
            proxies = None if self.use_proxy else {'http': None, 'https': None}
            
            self.response = session.get(
                self.url, 
                headers=headers, 
                timeout=30, 
                verify=self.verify_ssl,
                proxies=proxies,
                allow_redirects=True
            )
            self.response.raise_for_status()
            
            # Handle encoding properly for Persian/Arabic sites
            if self.response.apparent_encoding:
                self.response.encoding = self.response.apparent_encoding
            
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            
            # Detect platform
            self._detect_platform()
            
            # Basic validation
            if not self._validate_page():
                raise Exception("Page does not appear to be a valid product page")
            
            logger.info(f"Successfully fetched page: {self.url} (Platform: {self.platform})")
            return True
            
        except (requests.exceptions.SSLError, requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            error = handle_network_error(e, self.url)
            self.error_handler.add_error(error)
            raise Exception(error.get_user_friendly_message())
        except Exception as e:
            error = ScraperError(
                category=ErrorCategory.UNKNOWN,
                severity=ErrorSeverity.CRITICAL,
                message="Unexpected error while fetching page",
                details=str(e),
                recoverable=True,
                retry_recommended=True,
                suggested_action="Try again. If it persists, check the URL."
            )
            self.error_handler.add_error(error)
            raise Exception(error.get_user_friendly_message())
    
    def _detect_platform(self):
        """
        Detect the e-commerce platform
        """
        html_text = str(self.soup).lower()
        
        # Check for WooCommerce
        if 'woocommerce' in html_text or self.soup.find(class_=lambda x: x and 'woocommerce' in x.lower()):
            self.platform = 'woocommerce'
            return
        
        # Check for Shopify
        if 'shopify' in html_text or self.soup.find('meta', {'name': 'shopify'}):
            self.platform = 'shopify'
            return
        
        # Check for Magento
        if 'magento' in html_text or self.soup.find('body', class_=lambda x: x and 'magento' in x.lower()):
            self.platform = 'magento'
            return
        
        # Check for PrestaShop
        if 'prestashop' in html_text:
            self.platform = 'prestashop'
            return
        
        # Check for OpenCart
        if 'opencart' in html_text:
            self.platform = 'opencart'
            return
        
        # Default to custom
        self.platform = 'custom'
        logger.info(f"Platform detected as: {self.platform}")
    
    def _validate_page(self):
        """
        Basic validation that this is a real page
        """
        if not self.soup.find('html'):
            return False
        
        # Check for error pages
        page_text = self.soup.get_text().lower()
        
        if '404' in page_text and 'not found' in page_text:
            self.error_handler.add_error(ScraperError(
                category=ErrorCategory.HTTP_ERROR,
                severity=ErrorSeverity.HIGH,
                message="404 Page Not Found",
                details="Page content indicates product doesn't exist",
                recoverable=False,
                retry_recommended=False,
                suggested_action="Check if URL is correct or product still exists"
            ))
            return False
        
        if len(page_text) < self.MIN_PAGE_LENGTH:
            self.error_handler.add_warning("Page has very little content", "Might not be a valid product page")
        
        return True
    
    def extract_product_name(self):
        """
        Universal product name extraction with multiple strategies
        """
        try:
            # Strategy 1: Schema.org structured data (most reliable)
            schema_name = self._extract_from_schema('name')
            if schema_name:
                logger.info(f"Found product name from schema: {schema_name[:50]}")
                return schema_name
            
            # Strategy 2: Open Graph meta tags
            og_title = self.soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                title = og_title['content'].strip()
                if title and len(title) > 3:
                    logger.info(f"Found product name from og:title: {title[:50]}")
                    return title
            
            # Strategy 3: Platform-specific selectors
            if self.platform == 'woocommerce':
                selectors = ['h1.product_title', 'h1.entry-title', '.product-title h1']
            elif self.platform == 'shopify':
                selectors = ['h1.product-title', 'h1.product__title', '.product-single__title']
            elif self.platform == 'magento':
                selectors = ['h1.page-title', 'h1.product-name', '.product-info-main h1']
            else:
                # Generic selectors for custom sites
                selectors = [
                    'h1[class*="product"]',
                    'h1[class*="title"]',
                    'h1[id*="product"]',
                    '.product-name',
                    '.product-title',
                    '[itemprop="name"]',
                ]
            
            for selector in selectors:
                try:
                    element = self.soup.select_one(selector)
                    if element:
                        title = element.get_text(strip=True)
                        if title and len(title) > 2:
                            logger.info(f"Found product name using '{selector}': {title[:50]}")
                            return title
                except:
                    continue
            
            # Strategy 4: Any H1 tag
            h1 = self.soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)
                if title and len(title) > 2:
                    logger.info(f"Found product name from h1: {title[:50]}")
                    return title
            
            # Strategy 5: Page title (last resort)
            title_tag = self.soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                # Clean up title (remove site name)
                title = re.split(r'[|\-–—]', title)[0].strip()
                if title and len(title) > 3:
                    self.error_handler.add_warning(
                        "Product name from page title",
                        "Using page title as product name"
                    )
                    return title
            
            # If nothing found
            self.error_handler.add_warning(
                "Product name not found",
                "Using default name"
            )
            return "Untitled Product"
            
        except Exception as e:
            error = handle_parsing_error(e, "product name")
            self.error_handler.add_error(error)
            return "Untitled Product"
    
    def extract_description(self):
        """
        Universal description extraction
        """
        try:
            description_html = None
            
            # Strategy 1: Schema.org
            schema_desc = self._extract_from_schema('description')
            if schema_desc and len(schema_desc) > 50:
                description_html = f"<p>{schema_desc}</p>"
            
            # Strategy 2: Open Graph
            if not description_html:
                og_desc = self.soup.find('meta', property='og:description')
                if og_desc and og_desc.get('content'):
                    desc = og_desc['content'].strip()
                    if len(desc) > 30:
                        description_html = f"<p>{desc}</p>"
            
            # Strategy 3: Platform-specific selectors
            if not description_html:
                if self.platform == 'woocommerce':
                    selectors = [
                        '#tab-description',
                        '.woocommerce-Tabs-panel--description',
                        '.woocommerce-product-details__short-description',
                        'div[itemprop="description"]',
                    ]
                elif self.platform == 'shopify':
                    selectors = [
                        '.product-description',
                        '.product__description',
                        '[itemprop="description"]',
                    ]
                else:
                    # Generic selectors
                    selectors = [
                        '[itemprop="description"]',
                        '.product-description',
                        '.description',
                        '#description',
                        '.product-details',
                        '.product-content',
                        'div[class*="description"]',
                        'div[class*="product-detail"]',
                        'div[class*="product-info"]',
                    ]
                
                for selector in selectors:
                    try:
                        element = self.soup.select_one(selector)
                        if element:
                            # Check if it has meaningful content
                            text_content = element.get_text(strip=True)
                            if len(text_content) > 30:
                                description_html = self._clean_description_html(element)
                                logger.info(f"Found description using '{selector}' ({len(text_content)} chars)")
                                break
                    except:
                        continue
            
            # Strategy 4: Look for largest text block
            if not description_html or len(description_html) < 100:
                logger.info("Trying to find largest content block")
                description_html = self._find_main_content()
            
            if description_html and len(description_html.strip()) > 20:
                return description_html
            else:
                self.error_handler.add_warning(
                    "No description found",
                    "Could not extract product description"
                )
                return "No description available"
                
        except Exception as e:
            error = handle_parsing_error(e, "description")
            self.error_handler.add_error(error)
            return "No description available"
    
    def _find_main_content(self):
        """
        Find the main content block (largest meaningful text section)
        """
        try:
            # Look for common content containers
            content_containers = self.soup.find_all(
                ['article', 'main', 'div'],
                class_=lambda x: x and any(
                    keyword in x.lower() 
                    for keyword in ['content', 'product', 'detail', 'info', 'description']
                )
            )
            
            best_content = None
            max_length = 0
            
            for container in content_containers[:20]:  # Check first 20
                text = container.get_text(strip=True)
                # Must have decent length and not be navigation/menu
                if len(text) > max_length and len(text) < 10000:
                    # Check it's not navigation
                    if not container.find_parent(['nav', 'header', 'footer']):
                        max_length = len(text)
                        best_content = container
            
            if best_content:
                cleaned = self._clean_description_html(best_content)
                logger.info(f"Found main content block ({max_length} chars)")
                return cleaned
            
            return ""
            
        except Exception as e:
            logger.warning(f"Error finding main content: {str(e)}")
            return ""
    
    def _clean_description_html(self, element):
        """
        Clean HTML - remove scripts, styles, links
        """
        # Create a proper copy of the BeautifulSoup element
        from bs4 import BeautifulSoup
        element_copy = BeautifulSoup(str(element), 'html.parser')
        
        # Remove unwanted tags
        for tag in element_copy.find_all(['script', 'style', 'noscript', 'iframe', 'nav', 'header', 'footer']):
            tag.decompose()
        
        # Remove links but keep text
        for link in element_copy.find_all('a'):
            link.replace_with(link.get_text())
        
        # Fix images
        for img in element_copy.find_all('img'):
            real_src = img.get('data-lazy-src') or img.get('data-src') or img.get('src')
            if real_src:
                img['src'] = real_src
            for attr in ['data-lazy-src', 'data-src', 'srcset', 'loading']:
                if img.get(attr):
                    del img[attr]
            img['style'] = 'max-width:100%;height:auto;margin:15px auto;display:block;'
        
        # Style tables
        for table in element_copy.find_all('table'):
            table['style'] = 'width:100%;border-collapse:collapse;margin:20px 0;'
            table['border'] = '1'
            for th in table.find_all('th'):
                th['style'] = 'background:#667eea;color:white;padding:12px;border:1px solid #ddd;'
            for td in table.find_all('td'):
                td['style'] = 'padding:12px;border:1px solid #ddd;background:#fafafa;'
        
        # Remove empty elements
        for tag in element_copy.find_all(['p', 'div', 'span']):
            if not tag.get_text(strip=True) and not tag.find(['img', 'table']):
                tag.decompose()
        
        html = str(element_copy)
        
        # Remove data attributes
        html = re.sub(r'data-[a-z-]+="[^"]*"', '', html)
        
        return html
    
    def extract_price(self):
        """
        Universal price extraction
        """
        try:
            # Strategy 1: Schema.org
            schema_price = self._extract_from_schema('price')
            if schema_price:
                try:
                    return float(re.sub(r'[^\d.]', '', str(schema_price)))
                except:
                    pass
            
            # Strategy 2: Look for price in meta tags
            price_meta = self.soup.find('meta', property='product:price:amount')
            if price_meta and price_meta.get('content'):
                try:
                    return float(price_meta['content'])
                except:
                    pass
            
            # Strategy 3: Platform-specific and generic selectors
            price_selectors = [
                # WooCommerce
                'p.price .woocommerce-Price-amount',
                '.price .amount',
                'span.price',
                # Shopify
                '.product-price',
                '.price-item',
                'span.money',
                # Generic
                '[itemprop="price"]',
                'span[class*="price"]',
                'div[class*="price"]',
                '.product-price-value',
                # Persian sites
                '.price',
                '[class*="قیمت"]',
            ]
            
            for selector in price_selectors:
                elements = self.soup.select(selector)
                for element in elements:
                    price_text = element.get_text(strip=True)
                    # Extract numbers - remove all non-numeric except decimal point
                    price_text_clean = re.sub(r'[^\d.]', '', price_text)
                    if price_text_clean:
                        try:
                            price = float(price_text_clean)
                            if price > 0 and price < self.MAX_PRICE_VALUE:  # Sanity check
                                logger.info(f"Found price: {price}")
                                return price
                        except:
                            continue
            
            logger.info("No price found, defaulting to 0")
            return 0.00
            
        except Exception as e:
            logger.warning(f"Error extracting price: {str(e)}")
            return 0.00
    
    def extract_images(self):
        """
        Universal image extraction
        """
        images = []
        seen_urls = set()
        
        try:
            # Strategy 1: Schema.org
            schema_image = self._extract_from_schema('image')
            if schema_image:
                if isinstance(schema_image, list):
                    images.extend(schema_image)
                else:
                    images.append(schema_image)
            
            # Strategy 2: Open Graph
            og_image = self.soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                img_url = urljoin(self.url, og_image['content'])
                if img_url not in seen_urls:
                    images.append(img_url)
                    seen_urls.add(img_url)
            
            # Strategy 3: Look for product images with various selectors
            image_selectors = [
                # WooCommerce
                '.woocommerce-product-gallery__image img',
                '.woocommerce-product-gallery img',
                # Shopify
                '.product__media img',
                '.product-single__photo img',
                # Magento
                '.product-image-container img',
                '.gallery-placeholder img',
                # Generic
                '[class*="product"] img[class*="image"]',
                '[class*="product"] img[class*="photo"]',
                '[class*="gallery"] img',
                '.product-images img',
                '.product-gallery img',
                '[itemprop="image"]',
                'img[class*="product"]',
            ]
            
            for selector in image_selectors:
                imgs = self.soup.select(selector)
                for img in imgs:
                    img_url = (
                        img.get('data-large_image') or
                        img.get('data-src') or
                        img.get('data-lazy-src') or
                        img.get('src')
                    )
                    if img_url:
                        # Skip placeholders and tiny images
                        if 'placeholder' in img_url.lower() or 'data:image' in img_url:
                            continue
                        
                        # Make absolute URL
                        img_url = urljoin(self.url, img_url)
                        
                        # Skip duplicates
                        if img_url not in seen_urls:
                            images.append(img_url)
                            seen_urls.add(img_url)
                            
                        # Limit to prevent too many images
                        if len(images) >= self.MAX_PRODUCT_IMAGES:
                            break
                
                if len(images) >= 5:  # If we found enough, stop searching
                    break
            
            # Strategy 4: If still no images, get ANY images from main content
            if len(images) < 2:
                logger.info("Searching for any product images in page")
                all_imgs = self.soup.find_all('img')
                for img in all_imgs:
                    img_url = img.get('src') or img.get('data-src')
                    if img_url and 'product' in img_url.lower():
                        img_url = urljoin(self.url, img_url)
                        if img_url not in seen_urls and 'placeholder' not in img_url.lower():
                            images.append(img_url)
                            seen_urls.add(img_url)
                            if len(images) >= self.MAX_PRODUCT_IMAGES:
                                break
            
            logger.info(f"Found {len(images)} product images")
            return images[:self.MAX_PRODUCT_IMAGES]
            
        except Exception as e:
            logger.warning(f"Error extracting images: {str(e)}")
            return images
    
    def _extract_from_schema(self, field):
        """
        Extract data from Schema.org JSON-LD structured data
        """
        try:
            # Find all script tags with JSON-LD
            scripts = self.soup.find_all('script', type='application/ld+json')
            
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    
                    # Handle arrays
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and '@type' in item:
                                if item['@type'] in ['Product', 'ProductModel']:
                                    if field in item:
                                        return item[field]
                    
                    # Handle single object
                    elif isinstance(data, dict):
                        if '@type' in data and data['@type'] in ['Product', 'ProductModel']:
                            if field in data:
                                return data[field]
                        
                        # Check nested objects
                        if '@graph' in data:
                            for item in data['@graph']:
                                if isinstance(item, dict) and item.get('@type') in ['Product', 'ProductModel']:
                                    if field in item:
                                        return item[field]
                except:
                    continue
            
            return None
            
        except Exception as e:
            logger.debug(f"Error extracting schema data: {str(e)}")
            return None
    
    def scrape(self):
        """
        Main scraping method
        """
        try:
            self.fetch_page()
            
            data = {
                'name': self.extract_product_name(),
                'description': self.extract_description(),
                'price': self.extract_price(),
                'images': self.extract_images(),
                'categories': [],
                'source_url': self.url,
                'platform': self.platform,
                'scraping_metadata': {
                    'errors': self.error_handler.get_error_report(),
                    'warnings_count': len(self.error_handler.warnings),
                    'has_critical_errors': self.error_handler.has_critical_errors(),
                    'should_retry': self.error_handler.should_retry(),
                    'summary': self.error_handler.get_summary(),
                    'platform_detected': self.platform,
                }
            }
            
            if self.error_handler.has_errors() or self.error_handler.warnings:
                logger.warning(f"Scraping completed with issues:\n{self.error_handler.get_summary()}")
            else:
                logger.info(f"Scraping completed successfully for {self.url}")
            
            return data
            
        except Exception as e:
            logger.error(f"Fatal error during scraping: {str(e)}")
            raise


# Keep the old download_image and create_product functions for compatibility
def download_image(image_url):
    """
    Download image from URL
    """
    IMAGE_DOWNLOAD_TIMEOUT = 30
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        session = requests.Session()
        session.trust_env = False
        proxies = {'http': None, 'https': None}
        
        try:
            response = session.get(image_url, headers=headers, timeout=IMAGE_DOWNLOAD_TIMEOUT, stream=True, verify=True, proxies=proxies)
            response.raise_for_status()
        except requests.exceptions.SSLError:
            # Retry without SSL verification but don't suppress warnings globally
            logger.warning(f"SSL error downloading image {image_url}, retrying without verification")
            response = session.get(image_url, headers=headers, timeout=IMAGE_DOWNLOAD_TIMEOUT, stream=True, verify=False, proxies=proxies)
            response.raise_for_status()
        
        filename = image_url.split('/')[-1].split('?')[0]
        if not filename or '.' not in filename:
            content_type = response.headers.get('content-type', '')
            ext = 'jpg'
            if 'png' in content_type:
                ext = 'png'
            elif 'webp' in content_type:
                ext = 'webp'
            filename = f'product_image.{ext}'
        
        content = ContentFile(response.content)
        return content, filename
    
    except Exception as e:
        logger.error(f"Error downloading image {image_url}: {str(e)}")
        return None, None


def create_product_from_scraped_data(scraped_data, vendor, supplier=None):
    """
    Create Product from scraped data with transaction safety
    """
    from .models import Product, ProductImage
    from django.db import transaction, IntegrityError
    import random
    import time
    
    MAX_PRODUCT_IMAGES = 20
    
    try:
        base_slug = slugify(scraped_data['name'])
        random_number = random.randint(10000, 99999)
        unique_slug = f"{base_slug}-{random_number}"
        
        collision_count = 0
        while Product.objects.filter(slug=unique_slug).exists():
            random_number = random.randint(10000, 99999)
            unique_slug = f"{base_slug}-{random_number}"
            collision_count += 1
            if collision_count > 10:
                unique_slug = f"{base_slug}-{int(time.time())}-{random.randint(100, 999)}"
                break
        
        logger.info(f"Generated unique slug: {unique_slug}")
        
        product = Product(
            vendor=vendor,
            supplier=supplier,
            name=scraped_data['name'],
            slug=unique_slug,
            description=scraped_data['description'],
            price=scraped_data['price'],
            stock=0,
            is_active=False,
        )
        
        # Use atomic transaction to prevent race conditions
        try:
            with transaction.atomic():
                product.save()
        except IntegrityError:
            # Slug collision detected during save - use timestamp-based slug
            unique_slug = f"{base_slug}-{int(time.time())}-{random.randint(100, 999)}"
            product.slug = unique_slug
            product.save()
        
        images = scraped_data.get('images', [])
        for i, img_url in enumerate(images[:MAX_PRODUCT_IMAGES]):
            content, filename = download_image(img_url)
            if content and filename:
                product_image = ProductImage(
                    product=product,
                    is_primary=(i == 0),
                    sort_order=i
                )
                product_image.image.save(filename, content, save=True)
        
        return product, None
    
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return None, str(e)

