"""
Product scraper for WordPress/WooCommerce sites
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
    handle_network_error, handle_parsing_error, handle_image_error,
    handle_validation_error, handle_database_error
)

logger = logging.getLogger(__name__)


class WordPressScraper:
    """
    Scraper for WordPress/WooCommerce product pages with robust error handling
    """
    
    def __init__(self, url, verify_ssl=True, use_proxy=False):
        self.url = url
        self.soup = None
        self.response = None
        self.verify_ssl = verify_ssl  # Option to disable SSL verification for problematic sites
        self.use_proxy = use_proxy  # Option to disable proxy for connections
        self.error_handler = ErrorHandler()  # Initialize error handler
        
    def fetch_page(self):
        """
        Fetch the HTML content of the page with robust error handling
        """
        # Disable SSL warnings if SSL verification is off
        if not self.verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.error_handler.add_warning(
                "SSL verification disabled",
                "Connecting without SSL certificate verification due to certificate issues"
            )
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            
            # Configure proxy settings - completely disable proxy when use_proxy=False
            session = requests.Session()
            session.trust_env = self.use_proxy  # Don't trust environment proxy settings when bypassing
            
            if not self.use_proxy:
                # Set NO_PROXY to bypass system proxy completely
                proxies = {'http': None, 'https': None}
            else:
                proxies = None  # Use system proxy
            
            self.response = session.get(
                self.url, 
                headers=headers, 
                timeout=30, 
                verify=self.verify_ssl,
                proxies=proxies
            )
            self.response.raise_for_status()
            
            # Validate response is HTML
            if not self._validate_html_response():
                raise Exception("Response is not valid HTML. The URL might be incorrect or the page might be down.")
            
            # Use response.text to handle encoding properly, especially for Persian/Farsi sites
            self.response.encoding = self.response.apparent_encoding
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            
            # Validate the HTML content
            if not self._validate_page_content():
                raise Exception("Page does not appear to be a valid product page. Check if the URL is correct.")
            
            logger.info(f"Successfully fetched and validated page: {self.url}")
            return True
        except (requests.exceptions.SSLError, requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            # Use error handler for network errors
            error = handle_network_error(e, self.url)
            self.error_handler.add_error(error)
            raise Exception(error.get_user_friendly_message())
        except Exception as e:
            # Handle unexpected errors
            error = ScraperError(
                category=ErrorCategory.UNKNOWN,
                severity=ErrorSeverity.CRITICAL,
                message="Unexpected error while fetching page",
                details=str(e),
                recoverable=True,
                retry_recommended=True,
                suggested_action="An unexpected error occurred. Try again. If the problem persists, contact support."
            )
            self.error_handler.add_error(error)
            raise Exception(error.get_user_friendly_message())
    
    def _validate_html_response(self):
        """
        Validate that the response is actually HTML and not an error/JSON/empty response
        """
        try:
            # Check Content-Type header
            content_type = self.response.headers.get('Content-Type', '').lower()
            
            # Should be HTML, not JSON or other types
            if 'application/json' in content_type:
                self.error_handler.add_error(ScraperError(
                    category=ErrorCategory.HTTP_ERROR,
                    severity=ErrorSeverity.HIGH,
                    message="Response is JSON, not HTML",
                    details=f"Content-Type: {content_type}",
                    recoverable=False,
                    retry_recommended=False,
                    suggested_action="The URL appears to be an API endpoint, not a product page. Check the URL."
                ))
                return False
            
            if 'text/html' not in content_type and 'text/' in content_type:
                self.error_handler.add_warning(
                    f"Unexpected Content-Type: {content_type}",
                    "Expected text/html but got different content type"
                )
            
            # Check response has content
            if not self.response.text or len(self.response.text.strip()) < 100:
                self.error_handler.add_error(ScraperError(
                    category=ErrorCategory.HTTP_ERROR,
                    severity=ErrorSeverity.HIGH,
                    message="Response is empty or too short",
                    details=f"Content length: {len(self.response.text)} bytes",
                    recoverable=False,
                    retry_recommended=True,
                    suggested_action="The page returned empty content. The website might be down or the URL is incorrect."
                ))
                return False
            
            # Check for common error indicators in response
            response_lower = self.response.text[:1000].lower()
            
            # Check for redirect to login
            if 'wp-login' in response_lower or 'signin' in response_lower:
                if 'password' in response_lower and 'username' in response_lower:
                    self.error_handler.add_error(ScraperError(
                        category=ErrorCategory.PERMISSION,
                        severity=ErrorSeverity.HIGH,
                        message="Page requires authentication",
                        details="Redirected to login page",
                        recoverable=False,
                        retry_recommended=False,
                        suggested_action="This product page requires login. The scraper cannot access password-protected content."
                    ))
                    return False
            
            # Check for maintenance mode
            if 'maintenance' in response_lower or 'coming soon' in response_lower:
                self.error_handler.add_error(ScraperError(
                    category=ErrorCategory.HTTP_ERROR,
                    severity=ErrorSeverity.MEDIUM,
                    message="Website is in maintenance mode",
                    details="Page shows maintenance or coming soon message",
                    recoverable=True,
                    retry_recommended=True,
                    suggested_action="The website is temporarily unavailable. Try again later."
                ))
                return False
            
            logger.info("HTML response validation passed")
            return True
            
        except Exception as e:
            logger.warning(f"HTML validation failed: {str(e)}")
            # Don't fail on validation errors, just log
            return True
    
    def _validate_page_content(self):
        """
        Validate that the page contains valid HTML structure and looks like a product page
        """
        try:
            # Check for basic HTML structure
            if not self.soup.find('html'):
                self.error_handler.add_error(ScraperError(
                    category=ErrorCategory.PARSING,
                    severity=ErrorSeverity.HIGH,
                    message="No HTML tag found",
                    details="Response does not contain valid HTML structure",
                    recoverable=False,
                    retry_recommended=False,
                    suggested_action="The page is not valid HTML. The URL might be incorrect."
                ))
                return False
            
            # Check for title tag (all valid pages should have one)
            title = self.soup.find('title')
            if not title or not title.get_text(strip=True):
                self.error_handler.add_warning(
                    "No title tag found",
                    "Page has no title, might not be a valid product page"
                )
            
            # Check for common error page indicators
            page_text_lower = self.soup.get_text().lower()
            
            # Check for 404 error
            if '404' in page_text_lower and ('not found' in page_text_lower or 'page not found' in page_text_lower):
                self.error_handler.add_error(ScraperError(
                    category=ErrorCategory.HTTP_ERROR,
                    severity=ErrorSeverity.HIGH,
                    message="Page shows 404 error",
                    details="Page content indicates 'Page Not Found'",
                    recoverable=False,
                    retry_recommended=False,
                    suggested_action="The product page doesn't exist. Check if the URL is correct or if the product has been removed."
                ))
                return False
            
            # Check for 500/503 errors
            if any(err in page_text_lower for err in ['500 internal server error', '503 service unavailable', 'server error']):
                self.error_handler.add_error(ScraperError(
                    category=ErrorCategory.HTTP_ERROR,
                    severity=ErrorSeverity.MEDIUM,
                    message="Server error detected in page content",
                    details="Page shows internal server error",
                    recoverable=True,
                    retry_recommended=True,
                    suggested_action="The website is experiencing technical issues. Try again later."
                ))
                return False
            
            # Check for access denied / forbidden
            if 'access denied' in page_text_lower or 'forbidden' in page_text_lower:
                if len(page_text_lower) < 500:  # Short error pages
                    self.error_handler.add_error(ScraperError(
                        category=ErrorCategory.PERMISSION,
                        severity=ErrorSeverity.HIGH,
                        message="Access denied by website",
                        details="Page shows access denied message",
                        recoverable=False,
                        retry_recommended=False,
                        suggested_action="The website is blocking access to this page. It might have anti-bot protection."
                    ))
                    return False
            
            # Check if page has reasonable content length
            page_text = self.soup.get_text(strip=True)
            if len(page_text) < 200:
                self.error_handler.add_warning(
                    "Page has very little content",
                    f"Only {len(page_text)} characters found. This might not be a valid product page."
                )
            
            # Check for product-related indicators (optional - don't fail if missing)
            product_indicators = [
                self.soup.find(class_=lambda x: x and 'product' in x.lower()),
                self.soup.find(class_=lambda x: x and 'woocommerce' in x.lower()),
                self.soup.find(attrs={'itemtype': lambda x: x and 'product' in x.lower()}),
                self.soup.find('h1'),  # At least should have an h1
            ]
            
            if not any(product_indicators):
                self.error_handler.add_warning(
                    "No obvious product page indicators found",
                    "Page structure doesn't match typical WordPress/WooCommerce product pages"
                )
            
            logger.info("Page content validation passed")
            return True
            
        except Exception as e:
            logger.warning(f"Content validation error: {str(e)}")
            # Don't fail on validation errors, just log
            return True
    
    def extract_product_name(self):
        """
        Extract product name/title from the page
        """
        try:
            # Try multiple selectors for product title
            selectors = [
                'h1.product_title',  # WooCommerce default
                'h1.entry-title',    # Common WordPress
                '.product-title h1',
                'h1[itemprop="name"]',
                '.product_title',
                'h1.product-name',
                'h1',  # Fallback to first h1
            ]
            
            for selector in selectors:
                try:
                    element = self.soup.select_one(selector)
                    if element:
                        title = element.get_text(strip=True)
                        if title:
                            logger.info(f"Found product name using selector '{selector}': {title[:50]}...")
                            return title
                except Exception as e:
                    continue
            
            # Last resort: try page title
            title_tag = self.soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True).split('|')[0].split('-')[0].strip()
                self.error_handler.add_warning(
                    "Product name extracted from page title",
                    "Could not find product name in standard locations, used page title instead"
                )
                return title
            
            # If all fails, return default
            self.error_handler.add_warning(
                "Product name not found",
                "Using default product name. Please update manually."
            )
            return "Untitled Product"
        
        except Exception as e:
            error = handle_parsing_error(e, "product name")
            self.error_handler.add_error(error)
            return "Untitled Product"
    
    def extract_description(self):
        """
        Extract product description - CLEAN TEXT without HTML noise
        """
        try:
            descriptions = {
                'short': '',
                'long': ''
            }
            
            # Try to find WooCommerce short description
            short_desc_selectors = [
                '.woocommerce-product-details__short-description',
                '.product-short-description',
                'div[itemprop="description"]',
                '.short-description',
            ]
            
            for selector in short_desc_selectors:
                element = self.soup.select_one(selector)
                if element:
                    descriptions['short'] = element.get_text(strip=True)
                    break
            
            # Try to find full description
            long_desc_selectors = [
                '#tab-description',
                '.woocommerce-Tabs-panel--description',
                '.product-description',
                'div[itemprop="description"]',
                '.description',
                '.entry-content',
            ]
            
            description_element = None
            for selector in long_desc_selectors:
                element = self.soup.select_one(selector)
                if element:
                    description_element = element
                    break
            
            if description_element:
                # Clean up the description HTML
                cleaned_html = self._clean_description_html(description_element)
                descriptions['long'] = cleaned_html
            
            # Return the best available description
            if descriptions['long']:
                return descriptions['long']
            elif descriptions['short']:
                return descriptions['short']
            else:
                self.error_handler.add_warning(
                    "No description found",
                    "Product description could not be extracted"
                )
                return "No description available"
                
        except Exception as e:
            error = handle_parsing_error(e, "product description")
            self.error_handler.add_error(error)
            return "No description available"
    
    def _clean_description_html(self, element):
        """
        Clean HTML description - remove lazy-loading, noscript, hyperlinks, and add table styling
        """
        from copy import copy
        element_copy = copy(element)
        
        # Remove noscript tags
        for noscript in element_copy.find_all('noscript'):
            noscript.decompose()
        
        # Remove script tags (like aparat video embeds)
        for script in element_copy.find_all('script'):
            script.decompose()
        
        # Remove iframe embeds
        for iframe in element_copy.find_all('iframe'):
            iframe.decompose()
        
        # Remove div with IDs containing numbers (usually embed containers)
        for div in element_copy.find_all('div', id=True):
            if div.get('id') and div.get('id').isdigit():
                div.decompose()
        
        # Remove ALL hyperlinks - convert <a> tags to plain text
        for link in element_copy.find_all('a'):
            # Keep the text but remove the link
            link_text = link.get_text()
            link.replace_with(link_text)
        
        # Style tables properly
        for table in element_copy.find_all('table'):
            # Add styling attributes
            table['style'] = (
                'width: 100%; '
                'border-collapse: collapse; '
                'margin: 20px 0; '
                'background: #fff; '
                'box-shadow: 0 1px 3px rgba(0,0,0,0.1);'
            )
            table['border'] = '1'
            table['cellpadding'] = '10'
            table['cellspacing'] = '0'
            
            # Style table headers
            for th in table.find_all('th'):
                th['style'] = (
                    'background: #667eea; '
                    'color: white; '
                    'padding: 12px; '
                    'text-align: left; '
                    'font-weight: 600; '
                    'border: 1px solid #ddd;'
                )
            
            # Style table cells
            for td in table.find_all('td'):
                td['style'] = (
                    'padding: 12px; '
                    'border: 1px solid #ddd; '
                    'background: #fafafa;'
                )
            
            # Style table rows for alternating colors
            for i, tr in enumerate(table.find_all('tr')):
                if i % 2 == 0:
                    for td in tr.find_all('td'):
                        td['style'] = td.get('style', '') + ' background: #fff;'
                else:
                    for td in tr.find_all('td'):
                        td['style'] = td.get('style', '') + ' background: #f8f9fa;'
        
        # Remove lazy-loading placeholders and fix image sources
        for img in element_copy.find_all('img'):
            # Get the real image source
            real_src = img.get('data-lazy-src') or img.get('data-src') or img.get('src')
            
            if real_src and real_src.startswith('data:image'):
                # This is a placeholder, use data-lazy-src
                real_src = img.get('data-lazy-src') or img.get('data-src')
            
            if real_src:
                img['src'] = real_src
            
            # Remove lazy-loading attributes
            for attr in ['data-lazy-src', 'data-lazy-srcset', 'data-lazy-sizes', 'data-src', 'data-srcset']:
                if img.get(attr):
                    del img[attr]
            
            # Clean up unnecessary attributes
            for attr in ['srcset', 'sizes', 'loading']:
                if img.get(attr):
                    del img[attr]
            
            # Add styling to images for better display
            img['style'] = (
                'max-width: 100%; '
                'height: auto; '
                'display: block; '
                'margin: 15px auto; '
                'border-radius: 4px;'
            )
        
        # Remove empty paragraphs
        for p in element_copy.find_all('p'):
            if not p.get_text(strip=True) and not p.find('img') and not p.find('table'):
                p.decompose()
        
        # Remove empty headings
        for heading in element_copy.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if not heading.get_text(strip=True):
                heading.decompose()
        
        # Remove empty divs
        for div in element_copy.find_all('div'):
            if not div.get_text(strip=True) and not div.find(['img', 'table', 'script']):
                div.decompose()
        
        # Get the cleaned HTML
        cleaned_html = str(element_copy)
        
        # Additional cleanup - remove data attributes
        import re
        cleaned_html = re.sub(r'data-[a-z-]+="[^"]*"', '', cleaned_html)
        
        return cleaned_html
    
    def extract_price(self):
        """
        Extract product price
        """
        price_selectors = [
            'p.price .woocommerce-Price-amount',
            '.price .amount',
            'span.price',
            'span[itemprop="price"]',
            '.product-price',
            'bdi',
            '.woocommerce-Price-amount',
        ]
        
        for selector in price_selectors:
            element = self.soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # Extract numbers from price (remove currency symbols)
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                if price_match:
                    try:
                        return float(price_match.group())
                    except ValueError:
                        pass
        
        return 0.00
    
    def extract_images(self):
        """
        Extract product images (main image and gallery)
        """
        images = []
        
        # Try WooCommerce gallery
        gallery_selectors = [
            '.woocommerce-product-gallery__image img',
            '.product-images img',
            '.product-gallery img',
            'div.images img',
            '.woocommerce-product-gallery img',
        ]
        
        for selector in gallery_selectors:
            gallery_images = self.soup.select(selector)
            if gallery_images:
                for img in gallery_images:
                    # Get the highest quality image
                    img_url = (
                        img.get('data-large_image') or 
                        img.get('data-src') or 
                        img.get('src')
                    )
                    if img_url:
                        # Make absolute URL
                        img_url = urljoin(self.url, img_url)
                        if img_url not in images:
                            images.append(img_url)
                break
        
        # If no gallery found, try to find main product image
        if not images:
            main_image_selectors = [
                'img.wp-post-image',
                '.product-image img',
                'img[itemprop="image"]',
                '.featured-image img',
            ]
            
            for selector in main_image_selectors:
                img = self.soup.select_one(selector)
                if img:
                    img_url = img.get('data-src') or img.get('src')
                    if img_url:
                        img_url = urljoin(self.url, img_url)
                        images.append(img_url)
                    break
        
        return images
    
    def extract_categories(self):
        """
        Extract product categories/tags
        """
        categories = []
        
        # Try to find WooCommerce categories
        category_selectors = [
            '.posted_in a',  # WooCommerce category links
            '.product_meta a[rel="tag"]',
            '.product-categories a',
            'span.posted_in a',
        ]
        
        for selector in category_selectors:
            category_links = self.soup.select(selector)
            if category_links:
                for link in category_links:
                    cat_name = link.get_text(strip=True)
                    if cat_name and cat_name not in categories:
                        categories.append(cat_name)
        
        # Also try meta keywords
        meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            keywords = [k.strip() for k in meta_keywords['content'].split(',')]
            categories.extend(keywords[:3])  # Add first 3 keywords
        
        return list(set(categories))  # Remove duplicates
    
    def scrape(self):
        """
        Main scraping method - returns all product data with error information
        """
        try:
            self.fetch_page()
            
            # Extract all data with individual error handling
            data = {
                'name': self.extract_product_name(),
                'description': self.extract_description(),
                'price': self.extract_price(),
                'images': self.extract_images(),
                'categories': self.extract_categories(),
                'source_url': self.url,
                # Include error/warning information
                'scraping_metadata': {
                    'errors': self.error_handler.get_error_report(),
                    'warnings_count': len(self.error_handler.warnings),
                    'has_critical_errors': self.error_handler.has_critical_errors(),
                    'should_retry': self.error_handler.should_retry(),
                    'summary': self.error_handler.get_summary()
                }
            }
            
            # Log summary
            if self.error_handler.has_errors() or self.error_handler.warnings:
                logger.warning(f"Scraping completed with issues:\n{self.error_handler.get_summary()}")
            else:
                logger.info(f"Scraping completed successfully for {self.url}")
            
            return data
            
        except Exception as e:
            # If fetch_page fails, we can't continue
            logger.error(f"Fatal error during scraping: {str(e)}")
            raise


def download_image(image_url):
    """
    Download image from URL and return as ContentFile
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Try with SSL verification first, bypassing proxy completely
        session = requests.Session()
        session.trust_env = False  # Don't use environment proxy
        proxies = {'http': None, 'https': None}
        
        try:
            response = session.get(image_url, headers=headers, timeout=30, stream=True, verify=True, proxies=proxies)
            response.raise_for_status()
        except requests.exceptions.SSLError:
            # If SSL fails, try without verification
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = session.get(image_url, headers=headers, timeout=30, stream=True, verify=False, proxies=proxies)
            response.raise_for_status()
        except Exception as e:
            # If proxy bypass fails, try with system proxy
            if 'proxy' in str(e).lower():
                try:
                    session.trust_env = True
                    response = session.get(image_url, headers=headers, timeout=30, stream=True, verify=False)
                    response.raise_for_status()
                except:
                    raise e  # Re-raise original error
            else:
                raise
        
        # Get filename from URL
        filename = image_url.split('/')[-1].split('?')[0]
        if not filename or '.' not in filename:
            # Try to get extension from content-type
            content_type = response.headers.get('content-type', '')
            ext = 'jpg'
            if 'png' in content_type:
                ext = 'png'
            elif 'jpeg' in content_type or 'jpg' in content_type:
                ext = 'jpg'
            elif 'gif' in content_type:
                ext = 'gif'
            elif 'webp' in content_type:
                ext = 'webp'
            filename = f'product_image.{ext}'
        
        # Create ContentFile
        content = ContentFile(response.content)
        return content, filename
    
    except Exception as e:
        logger.error(f"Error downloading image {image_url}: {str(e)}")
        return None, None


