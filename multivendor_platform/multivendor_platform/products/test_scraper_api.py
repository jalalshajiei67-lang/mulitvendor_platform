"""
Simple API endpoint to test scraper functionality
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
import requests
from .scraper import WordPressScraper

@api_view(['POST'])
@permission_classes([IsAdminUser])
def test_scraper_connection(request):
    """
    Test if the scraper can connect to external websites
    
    POST /api/test-scraper/
    {
        "url": "https://example.com/product/test"
    }
    """
    test_url = request.data.get('url')
    
    if not test_url:
        return Response({
            'success': False,
            'error': 'URL is required'
        }, status=400)
    
    results = {
        'url': test_url,
        'basic_connection': False,
        'scraper_connection': False,
        'data_extraction': False,
        'errors': [],
        'warnings': []
    }
    
    # Test 1: Basic HTTP connection
    try:
        response = requests.get(test_url, timeout=10, verify=False)
        results['basic_connection'] = True
        results['status_code'] = response.status_code
    except requests.exceptions.SSLError as e:
        results['errors'].append(f'SSL Error: {str(e)}')
    except requests.exceptions.ConnectionError as e:
        results['errors'].append(f'Connection Error: {str(e)}')
    except requests.exceptions.Timeout as e:
        results['errors'].append(f'Timeout Error: {str(e)}')
    except Exception as e:
        results['errors'].append(f'Unexpected Error: {str(e)}')
    
    # Test 2: Scraper fetch
    if results['basic_connection']:
        try:
            scraper = WordPressScraper(test_url, verify_ssl=False, use_proxy=False)
            scraper.fetch_page()
            results['scraper_connection'] = True
        except Exception as e:
            results['errors'].append(f'Scraper Fetch Error: {str(e)}')
    
    # Test 3: Data extraction
    if results['scraper_connection']:
        try:
            data = scraper.scrape()
            results['data_extraction'] = True
            results['extracted_data'] = {
                'name': data.get('name', 'N/A')[:100],
                'price': str(data.get('price', 0)),
                'images_count': len(data.get('images', [])),
                'has_description': bool(data.get('description'))
            }
        except Exception as e:
            results['errors'].append(f'Data Extraction Error: {str(e)}')
    
    # Overall success
    results['success'] = (
        results['basic_connection'] and 
        results['scraper_connection'] and 
        results['data_extraction']
    )
    
    return Response(results)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def test_network_access(request):
    """
    Test basic network access from the server
    
    GET /api/test-network/
    """
    results = {
        'tests': []
    }
    
    # Test various endpoints
    test_urls = [
        ('Google', 'https://www.google.com'),
        ('Example', 'https://example.com'),
        ('GitHub', 'https://github.com'),
    ]
    
    for name, url in test_urls:
        try:
            response = requests.get(url, timeout=5, verify=False)
            results['tests'].append({
                'name': name,
                'url': url,
                'success': True,
                'status_code': response.status_code
            })
        except Exception as e:
            results['tests'].append({
                'name': name,
                'url': url,
                'success': False,
                'error': str(e)
            })
    
    results['can_access_internet'] = any(t['success'] for t in results['tests'])
    
    return Response(results)

