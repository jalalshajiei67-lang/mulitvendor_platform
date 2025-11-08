"""
Universal Product Scraper - Works with ANY e-commerce platform
Supports: WooCommerce, Shopify, Magento, Custom sites, and more
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.utils.text import slugify
import re
import json
from urllib.parse import urljoin, urlparse
import logging
import time
import random
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from fake_useragent import UserAgent
import unicodedata



logger = logging.getLogger(__name__)





class CircuitBreaker:
    """Circuit breaker to prevent cascading failures"""
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            
            raise e


# Now your existing UniversalProductScraper class
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
    
    def __init__(self, url, verify_ssl=True, use_proxy=False, max_retries=3):
        self.url = url
        self.soup = None
        self.response = None
        self.verify_ssl = verify_ssl
        self.use_proxy = use_proxy
        self.max_retries = max_retries
        self.platform = None  # Will be detected: woocommerce, shopify, custom, etc.
        
        # Initialize user agent rotator
        self.ua = UserAgent()
        
        # Create a robust session
        self.session = self._create_session()
        
        # Add circuit breaker
        self.circuit_breaker = CircuitBreaker()

    def _create_session(self):
        """Create a robust session with retry strategy"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def _get_rotated_headers(self):
        """Get headers with rotated user agent"""
        try:
            user_agent = self.ua.random
        except:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        
        return {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'fa-IR,fa;q=0.9,en-US,en;q=0.8,ar;q=0.7',  # Persian first for Persian sites
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }

    def fetch_page_with_selenium(self):
        """Fallback method using Selenium for JavaScript-heavy pages"""
        try:
            # Only try Selenium if selenium is available
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
            except ImportError:
                logger.warning("Selenium not available, skipping Selenium fallback")
                return False
            
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            headers = self._get_rotated_headers()
            chrome_options.add_argument(f'user-agent={headers["User-Agent"]}')
            # Set Persian language preference
            chrome_options.add_argument('--lang=fa-IR')
            chrome_options.add_experimental_option('prefs', {
                'intl.accept_languages': 'fa-IR,fa,en-US,en'
            })
            
            driver = None
            try:
                driver = webdriver.Chrome(options=chrome_options)
                driver.set_page_load_timeout(30)
                driver.get(self.url)
                
                # Wait for page to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Get page source
                html = driver.page_source
                self.soup = BeautifulSoup(html, 'html.parser')
                
                # Detect platform
                self._detect_platform()
                
                # Validate page
                if not self._validate_page():
                    return False
                
                logger.info(f"Successfully fetched page with Selenium: {self.url}")
                return True
            finally:
                if driver:
                    driver.quit()
        except Exception as e:
            logger.warning(f"Selenium fetch failed: {str(e)}")
            return False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((
            requests.exceptions.RequestException,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError
        ))
    )
    def fetch_page(self):
        """
        Fetch the HTML content with robust error handling
        """
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 2.0))
        
        if not self.verify_ssl:
            logger.warning(f"SSL verification disabled for {self.url}")
        
        try:
            headers = self._get_rotated_headers()
            
            proxies = None if self.use_proxy else {'http': None, 'https': None}
            
            self.response = self.session.get(
                self.url, 
                headers=headers, 
                timeout=30, 
                verify=self.verify_ssl,
                proxies=proxies,
                allow_redirects=True
            )
            self.response.raise_for_status()
            
            # Enhanced encoding handling for Persian/Arabic sites
            self._handle_persian_encoding()
            
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
            logger.error(f"Error fetching page {self.url}: {str(e)}")
            raise Exception(f"Failed to fetch page: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while fetching page {self.url}: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    def _handle_persian_encoding(self):
        """
        Enhanced encoding handling for Persian/Arabic content
        """
        if not self.response:
            return
        
        # Try to detect encoding from various sources
        encodings_to_try = []
        
        # 1. Check Content-Type header
        content_type = self.response.headers.get('Content-Type', '')
        if 'charset=' in content_type:
            charset = content_type.split('charset=')[1].split(';')[0].strip().lower()
            if charset:
                encodings_to_try.append(charset)
        
        # 2. Try apparent encoding
        if self.response.apparent_encoding:
            encodings_to_try.append(self.response.apparent_encoding.lower())
        
        # 3. Try common Persian/Arabic encodings
        persian_encodings = ['utf-8', 'utf-8-sig', 'windows-1256', 'iso-8859-6', 'cp1256']
        for enc in persian_encodings:
            if enc not in encodings_to_try:
                encodings_to_try.append(enc)
        
        # Try each encoding
        for encoding in encodings_to_try:
            try:
                self.response.encoding = encoding
                # Verify it works by checking if text contains valid characters
                if self.response.text and len(self.response.text) > 0:
                    # Check for Persian/Arabic characters
                    sample = self.response.text[:500]
                    if any('\u0600' <= char <= '\u06FF' for char in sample):  # Persian/Arabic range
                        logger.info(f"Successfully decoded Persian content with {encoding}")
                        return
            except (UnicodeDecodeError, LookupError):
                continue
        
        # Fallback to apparent encoding if nothing worked
        if self.response.apparent_encoding:
            self.response.encoding = self.response.apparent_encoding
            logger.warning(f"Using fallback encoding: {self.response.apparent_encoding}")

    def _convert_persian_numbers(self, text):
        """
        Convert Persian/Arabic numerals to English numerals
        """
        if not text:
            return text
        
        # Persian/Arabic to English number mapping
        persian_to_english = {
            '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
            '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
            '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
            '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
        }
        
        result = str(text)
        for persian_num, english_num in persian_to_english.items():
            result = result.replace(persian_num, english_num)
        
        return result

    def _clean_persian_text(self, text):
        """
        Clean Persian text - normalize, remove extra spaces, fix common issues
        """
        if not text:
            return text
        
        # Convert to string
        text = str(text)
        
        # Normalize Unicode (NFC normalization)
        text = unicodedata.normalize('NFC', text)
        
        # Remove zero-width characters
        text = text.replace('\u200c', ' ')  # Zero-width non-joiner
        text = text.replace('\u200d', '')   # Zero-width joiner
        text = text.replace('\u200e', '')    # Left-to-right mark
        text = text.replace('\u200f', '')    # Right-to-left mark
        
        # Fix common Persian encoding issues
        text = text.replace('ك', 'ک')  # Arabic kaf to Persian kaf
        text = text.replace('ي', 'ی')  # Arabic yeh to Persian yeh
        text = text.replace('ة', 'ه')  # Arabic teh marbuta to heh
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()

    def _is_persian_content(self, text):
        """
        Detect if text contains Persian/Arabic characters
        """
        if not text:
            return False
        
        # Check for Persian/Arabic character ranges
        persian_chars = sum(1 for char in str(text) if '\u0600' <= char <= '\u06FF')
        total_chars = len([c for c in str(text) if c.isalpha()])
        
        if total_chars == 0:
            return False
        
        # If more than 30% Persian/Arabic characters, consider it Persian
        return (persian_chars / total_chars) > 0.3 if total_chars > 0 else False

    def _extract_persian_price(self, price_text):
        """
        Extract price from Persian-formatted text
        Handles: Persian numbers, currency symbols, commas
        """
        if not price_text:
            return None
        
        # Convert Persian numbers to English
        price_text = self._convert_persian_numbers(price_text)
        
        # Remove common Persian currency words and symbols
        persian_currency = [
            'تومان', 'ريال', 'ریال', 'هزار', 'میلیون', 'میلیارد',
            'ت.', 'ر.', 'قیمت', 'مبلغ', 'قیمت:', 'مبلغ:'
        ]
        for currency in persian_currency:
            price_text = price_text.replace(currency, '')
        
        # Remove currency symbols
        currency_symbols = ['$', '€', '£', '¥', '₹', '₽', '₪', 'ریال']
        for symbol in currency_symbols:
            price_text = price_text.replace(symbol, '')
        
        # Remove all non-numeric except decimal point and comma
        price_text = re.sub(r'[^\d.,]', '', price_text)
        
        # Handle comma as thousand separator (Persian format)
        if ',' in price_text:
            # Remove commas if they're thousand separators
            parts = price_text.split(',')
            if len(parts) == 2 and len(parts[1]) == 3:
                # Likely thousand separator
                price_text = price_text.replace(',', '')
            elif len(parts) > 2:
                # Multiple commas, likely thousand separators
                price_text = price_text.replace(',', '')
        
        try:
            price = float(price_text.replace(',', ''))
            if price > 0 and price < self.MAX_PRICE_VALUE:
                return price
        except ValueError:
            pass
        
        return None

    def _clean_persian_title(self, title):
        """
        Clean Persian product title - remove site names, separators, etc.
        """
        if not title:
            return title
        
        title = self._clean_persian_text(title)
        
        # Remove common Persian site name suffixes
        persian_suffixes = [
            r'\s*[-–—]\s*(دانا|کد|نگر|سایت|فروشگاه|خرید|آنلاین|محصول).*$',
            r'\s*[-–—]\s*(site|shop|store|online).*$',
            r'\s*\|\s*.*$',  # Remove everything after |
            r'\s*-\s*(خانه|صفحه اصلی).*$',  # Remove "خانه" or "صفحه اصلی"
        ]
        
        for pattern in persian_suffixes:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        
        # Remove common separators and keep first part
        title = re.split(r'[|\-–—•]', title)[0].strip()
        
        # Remove extra whitespace
        title = ' '.join(title.split())
        
        return title.strip()







    
    def _detect_platform(self):
        """
        Detect the e-commerce platform
        """
        html_text = str(self.soup).lower()
        
        # Check for WooCommerce
        if 'woocommerce' in html_text or self.soup.find(class_=lambda x: x and 'woocommerce' in x.lower()):
            self.platform = 'woocommerce'
            return
        
        # Check for WordPress (including page builders)
        wordpress_indicators = [
            'wp-content' in html_text,
            '/wp-includes/' in html_text,
            '/wp-content/themes/' in html_text,
            'wordpress' in html_text,
            self.soup.find('meta', {'name': lambda x: x and 'generator' in x.lower()}) and 
                'wordpress' in str(self.soup.find('meta', {'name': lambda x: x and 'generator' in x.lower()})).lower(),
            # Page builder indicators
            'elementor' in html_text,
            'divi' in html_text,
            'beaver-builder' in html_text,
            'visual-composer' in html_text,
            'siteorigin' in html_text,
        ]
        
        if any(wordpress_indicators):
            self.platform = 'wordpress'
            logger.info("Platform detected as: wordpress (may use page builder)")
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
            logger.warning("Page appears to be 404")
            return False
        
        if len(page_text) < self.MIN_PAGE_LENGTH:
            logger.warning("Page has very little content")
        
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
            
            # Strategy 2.5: Title tag (especially useful for WordPress/page builders)
            # Check this early for WordPress pages as it's often reliable
            if self.platform == 'wordpress':
                title_tag = self.soup.find('title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    # Use Persian-aware title cleaning
                    title = self._clean_persian_title(title)
                    if title and len(title) > 3:
                        logger.info(f"Found product name from title tag: {title[:50]}")
                        return self._clean_persian_text(title)
            
            # Strategy 3: Platform-specific selectors
            if self.platform == 'woocommerce':
                selectors = ['h1.product_title', 'h1.entry-title', '.product-title h1']
            elif self.platform == 'wordpress':
                # WordPress/page builder title selectors
                selectors = [
                    'h1.entry-title',
                    'h1.page-title',
                    'article h1',
                    '.entry-header h1',
                    '[class*="elementor"] h1',
                    'h1[class*="title"]',
                    'h1.product-title',
                    'h1[class*="product"]',
                ]
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
                            # Clean Persian text if detected
                            if self._is_persian_content(title):
                                title = self._clean_persian_text(title)
                                title = self._clean_persian_title(title)
                            logger.info(f"Found product name using '{selector}': {title[:50]}")
                            return title
                except:
                    continue
            
            # Strategy 4: Any H1 tag
            h1 = self.soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)
                if title and len(title) > 2:
                    # Clean Persian text if detected
                    if self._is_persian_content(title):
                        title = self._clean_persian_text(title)
                        title = self._clean_persian_title(title)
                    logger.info(f"Found product name from h1: {title[:50]}")
                    return title
            
            # Strategy 5: Page title (last resort)
            title_tag = self.soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                # Use Persian-aware title cleaning
                title = self._clean_persian_title(title)
                if title and len(title) > 3:
                    logger.info("Using page title as product name")
                    return self._clean_persian_text(title)
            
            # If nothing found
            logger.warning("Product name not found, using default")
            return "Untitled Product"
            
        except Exception as e:
            logger.error(f"Error extracting product name: {str(e)}")
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
                elif self.platform == 'wordpress':
                    # WordPress/page builder selectors (including Persian-specific)
                    selectors = [
                        'article .entry-content',
                        '.entry-content',
                        '.post-content',
                        '.content-area',
                        '[class*="elementor"] [class*="text"]',
                        '[class*="elementor"] [class*="content"]',
                        '.et_pb_section',
                        'div[class*="content"]',
                        '[itemprop="description"]',
                        '.product-description',
                        '.description',
                        # Persian-specific selectors
                        '[class*="توضیحات"]',
                        '[class*="شرح"]',
                        '[class*="محصول"]',
                    ]
                elif self.platform == 'shopify':
                    selectors = [
                        '.product-description',
                        '.product__description',
                        '[itemprop="description"]',
                    ]
                else:
                    # Generic selectors (including Persian-specific)
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
                        # Persian-specific selectors
                        '[class*="توضیحات"]',
                        '[class*="شرح"]',
                        '[class*="محصول"]',
                        '[id*="توضیحات"]',
                    ]
                
                for selector in selectors:
                    try:
                        element = self.soup.select_one(selector)
                        if element:
                            # Check if it has meaningful content
                            text_content = element.get_text(strip=True)
                            if len(text_content) > 30:
                                # Make sure it's not in header/footer/nav
                                if not element.find_parent(['header', 'footer', 'nav']):
                                    # Clean Persian text if detected
                                    if self._is_persian_content(text_content):
                                        # Clean the text before processing
                                        text_content = self._clean_persian_text(text_content)
                                    description_html = self._clean_description_html(element)
                                    logger.info(f"Found description using '{selector}' ({len(text_content)} chars)")
                                    break
                    except:
                        continue
            
            # Strategy 4: For WordPress/page builder pages, try to find main content
            if (not description_html or len(description_html) < 100) or self.platform == 'wordpress':
                logger.info("Trying to find main content block (WordPress/page builder)")
                main_content = self._find_main_content()
                if main_content and len(main_content) > len(description_html or ""):
                    description_html = main_content
            
            if description_html and len(description_html.strip()) > 20:
                return description_html
            else:
                logger.warning("No description found")
                return "No description available"
                
        except Exception as e:
            logger.warning(f"Error extracting description: {str(e)}")
            return "No description available"
    
    def _find_main_content(self):
        """
        Find the main content block (largest meaningful text section)
        Excludes header, footer, navigation, sidebars
        Works with WordPress page builders (Elementor, Divi, etc.)
        """
        try:
            # First, remove common unwanted sections
            unwanted_selectors = [
                'header', 'footer', 'nav',
                '[class*="header"]', '[class*="footer"]', '[class*="nav"]',
                '[class*="menu"]', '[class*="sidebar"]',
                '[id*="header"]', '[id*="footer"]', '[id*="nav"]',
                '[id*="menu"]', '[id*="sidebar"]',
                '.header', '.footer', '.navigation', '.nav',
                '.menu', '.sidebar', '.widget',
            ]
            
            # Create a copy of soup to avoid modifying original
            from bs4 import BeautifulSoup
            soup_copy = BeautifulSoup(str(self.soup), 'html.parser')
            
            # Remove unwanted sections
            for selector in unwanted_selectors:
                try:
                    for element in soup_copy.select(selector):
                        element.decompose()
                except:
                    continue
            
            # Look for common WordPress/main content containers
            content_selectors = [
                # WordPress common
                'article',
                'main',
                '[role="main"]',
                '#main',
                '.main-content',
                '.site-main',
                # Page builders
                '.elementor-element',
                '.elementor-widget',
                '.et_pb_section',
                '.vc_row',
                '.fl-row',
                # Generic
                '[class*="content"]',
                '[class*="product"]',
                '[class*="entry"]',
                '[id*="content"]',
                '[id*="product"]',
            ]
            
            best_content = None
            max_length = 0
            
            # Try specific selectors first
            for selector in content_selectors:
                try:
                    containers = soup_copy.select(selector)
                    for container in containers:
                        # Skip if it's in unwanted area
                        if container.find_parent(['header', 'footer', 'nav']):
                            continue
                        
                        text = container.get_text(strip=True)
                        # Must have decent length and not be too long (likely not main content)
                        if self.MIN_DESCRIPTION_LENGTH < len(text) < 50000:
                            # Check it doesn't look like navigation/menu
                            links = container.find_all('a')
                            if len(links) < len(text) / 50:  # Not too many links (nav indicator)
                                if len(text) > max_length:
                                    max_length = len(text)
                                    best_content = container
                except:
                    continue
            
            # If no specific container found, look for largest div that's not in header/footer
            if not best_content or max_length < 100:
                all_divs = soup_copy.find_all('div')
                for div in all_divs:
                    # Skip if in unwanted areas
                    if div.find_parent(['header', 'footer', 'nav', 'aside']):
                        continue
                    
                    # Skip if has navigation-like classes
                    div_classes = ' '.join(div.get('class', [])).lower()
                    if any(word in div_classes for word in ['nav', 'menu', 'header', 'footer', 'sidebar', 'widget']):
                        continue
                    
                    text = div.get_text(strip=True)
                    if self.MIN_DESCRIPTION_LENGTH < len(text) < 50000:
                        links = div.find_all('a')
                        if len(links) < len(text) / 50:
                            if len(text) > max_length:
                                max_length = len(text)
                                best_content = div
            
            # If still nothing, try body content minus header/footer
            if not best_content or max_length < 100:
                body = soup_copy.find('body')
                if body:
                    # Remove header/footer from body
                    for unwanted in body.find_all(['header', 'footer', 'nav', 'aside']):
                        unwanted.decompose()
                    
                    text = body.get_text(strip=True)
                    if len(text) > max_length and len(text) < 50000:
                        best_content = body
                        max_length = len(text)
            
            if best_content and max_length >= self.MIN_DESCRIPTION_LENGTH:
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
            if self.platform == 'woocommerce':
                price_selectors = [
                    'p.price .woocommerce-Price-amount',
                    '.price .amount',
                    'span.price',
                    '.woocommerce-Price-amount',
                ]
            elif self.platform == 'wordpress':
                # WordPress/page builder price selectors
                price_selectors = [
                    '.price',
                    'span.price',
                    '.product-price',
                    '[class*="price"]',
                    '[itemprop="price"]',
                    '.amount',
                    # Persian sites
                    '[class*="قیمت"]',
                    '[class*="مبلغ"]',
                ]
            else:
                price_selectors = [
                    # Shopify
                    '.product-price',
                    '.price-item',
                    'span.money',
                    # Generic
                    '[itemprop="price"]',
                    'span[class*="price"]',
                    'div[class*="price"]',
                    '.product-price-value',
                    '.price',
                ]
            
            for selector in price_selectors:
                elements = self.soup.select(selector)
                for element in elements:
                    price_text = element.get_text(strip=True)
                    
                    # Try Persian price extraction first (handles Persian numbers)
                    if self._is_persian_content(price_text):
                        persian_price = self._extract_persian_price(price_text)
                        if persian_price:
                            logger.info(f"Found price (Persian format): {persian_price}")
                            return persian_price
                    
                    # Fallback to standard extraction
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
            
            # Strategy 4: Extract ALL images from main content area (for WordPress/page builders)
            if len(images) < 2 or self.platform == 'wordpress':
                logger.info("Searching for images in main content area")
                # Find main content area first
                main_content = None
                if self.platform == 'wordpress':
                    # Look for WordPress main content
                    for selector in ['article', 'main', '.entry-content', '.content-area', '[role="main"]']:
                        main_content = self.soup.select_one(selector)
                        if main_content:
                            break
                
                # Search area to use
                search_area = main_content if main_content else self.soup
                
                # Exclude images from header/footer/nav
                all_imgs = search_area.find_all('img')
                for img in all_imgs:
                    # Skip if image is in header/footer/nav
                    if img.find_parent(['header', 'footer', 'nav']):
                        continue
                    
                    # Get image URL
                    img_url = (
                        img.get('data-large_image') or
                        img.get('data-lazy-src') or
                        img.get('data-src') or
                        img.get('src')
                    )
                    
                    if img_url:
                        # Skip placeholders
                        if 'placeholder' in img_url.lower() or 'data:image' in img_url or 'blank' in img_url.lower():
                            continue
                        
                        # Make absolute URL
                        img_url = urljoin(self.url, img_url)
                        
                        # Skip duplicates and very small images (likely icons)
                        if img_url not in seen_urls:
                            # Skip icon-sized images
                            width = img.get('width')
                            height = img.get('height')
                            if width and height:
                                try:
                                    if int(width) < 50 or int(height) < 50:
                                        continue
                                except:
                                    pass
                            
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
        Main scraping method with circuit breaker
        """
        try:
            return self.circuit_breaker.call(self._scrape_internal)
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            raise

    def _scrape_internal(self):
        """
        Enhanced internal scraping method with better error handling and data validation
        """
        start_time = time.time()
        
        try:
            # Step 1: Fetch the page with multiple fallback strategies
            fetch_success = False
            fetch_method = None
            
            # Strategy 1: Try regular requests (fastest)
            try:
                logger.info(f"Attempting to fetch page with requests: {self.url}")
                self.fetch_page()
                fetch_success = True
                fetch_method = "requests"
            except Exception as e:
                logger.warning(f"Regular fetch failed: {str(e)}")
            
            # Strategy 2: Try Selenium fallback if requests failed
            if not fetch_success:
                logger.info("Attempting fallback with Selenium for JavaScript-heavy pages")
                try:
                    if self.fetch_page_with_selenium():
                        fetch_success = True
                        fetch_method = "selenium"
                    else:
                        raise Exception("Selenium fetch returned False")
                except Exception as e:
                    logger.error(f"Selenium fallback also failed: {str(e)}")
                    raise Exception("All fetch methods failed. Unable to retrieve page content.")
            
            if not fetch_success:
                raise Exception("Failed to fetch page with all available methods")
            
            logger.info(f"Successfully fetched page using {fetch_method} method")
            
            # Step 2: Extract product data with validation
            extraction_start = time.time()
            
            # Extract name with quality check
            name = self.extract_product_name()
            if not name or name == "Untitled Product":
                logger.warning("Could not extract valid product name, using default")
            
            # Extract description with length validation
            description = self.extract_description()
            if not description or description == "No description available":
                logger.warning("Could not extract product description")
            elif len(description) < self.MIN_DESCRIPTION_LENGTH:
                logger.warning(f"Description is only {len(description)} characters")
            
            # Extract price with validation
            price = self.extract_price()
            if price <= 0:
                logger.warning("Could not extract valid price or price is zero")
            elif price >= self.MAX_PRICE_VALUE:
                logger.warning(f"Extracted price ({price}) seems unusually high")
            
            # Extract images with count validation
            images = self.extract_images()
            if not images or len(images) == 0:
                logger.warning("No product images found")
            elif len(images) > self.MAX_PRODUCT_IMAGES:
                images = images[:self.MAX_PRODUCT_IMAGES]
                logger.warning(f"Found {len(images)} images, limiting to {self.MAX_PRODUCT_IMAGES}")
            
            # Extract categories (if available)
            categories = []
            try:
                # Try to extract categories if method exists
                if hasattr(self, 'extract_categories'):
                    categories = self.extract_categories()
            except Exception as e:
                logger.debug(f"Could not extract categories: {str(e)}")
            
            extraction_time = time.time() - extraction_start
            logger.info(f"Data extraction completed in {extraction_time:.2f}s")
            
            # Step 3: Build comprehensive data structure
            data = {
                'name': name,
                'description': description,
                'price': float(price) if price else 0.0,
                'images': images,
                'categories': categories if categories else [],
                'source_url': self.url,
                'platform': self.platform,
                'fetch_method': fetch_method,
                'extraction_time': round(extraction_time, 2),
                'platform_detected': self.platform,
                'timestamp': time.time(),
            }
            
            # Step 4: Validate and log results
            total_time = time.time() - start_time
            logger.info(f"Scraping completed in {total_time:.2f}s")
            
            return data
            
        except Exception as e:
            total_time = time.time() - start_time
            logger.error(f"Fatal error during scraping after {total_time:.2f}s: {str(e)}")
            raise

    def _assess_data_quality(self, name, description, price, images):
        """
        Assess the quality of scraped data
        Returns a quality score (0.0 to 1.0) and details
        """
        score = 0.0
        issues = []
        
        # Name quality (20% weight)
        if name and name != "Untitled Product" and len(name) > 3:
            score += 0.2
        else:
            issues.append("Missing or invalid product name")
        
        # Description quality (30% weight)
        if description and description != "No description available":
            desc_length = len(description.strip())
            if desc_length >= 100:
                score += 0.3
            elif desc_length >= self.MIN_DESCRIPTION_LENGTH:
                score += 0.2
                issues.append("Description is short")
            else:
                issues.append("Description is very short or missing")
        else:
            issues.append("Missing description")
        
        # Price quality (20% weight)
        if price and price > 0 and price < self.MAX_PRICE_VALUE:
            score += 0.2
        else:
            issues.append("Missing or invalid price")
        
        # Images quality (20% weight)
        if images and len(images) > 0:
            if len(images) >= 3:
                score += 0.2
            elif len(images) >= 1:
                score += 0.15
                issues.append("Few images found")
        else:
            issues.append("No images found")
        
        # Platform detection (10% weight)
        if self.platform and self.platform != 'custom':
            score += 0.1
        else:
            score += 0.05
            issues.append("Platform not clearly detected")
        
        return {
            'score': round(score, 2),
            'percentage': round(score * 100, 1),
            'issues': issues,
            'has_name': bool(name and name != "Untitled Product"),
            'has_description': bool(description and description != "No description available"),
            'has_price': bool(price and price > 0),
            'image_count': len(images) if images else 0,
            'platform_detected': bool(self.platform),
        }








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

