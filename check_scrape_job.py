"""
Script to check failed scraping jobs
Run with: python manage.py shell < check_scrape_job.py
Or: python manage.py shell, then copy-paste this code
"""

from products.models import ProductScrapeJob
import json

# Get all failed jobs
failed_jobs = ProductScrapeJob.objects.filter(status='failed')

print(f"\n{'='*80}")
print(f"Found {failed_jobs.count()} failed scraping job(s)")
print(f"{'='*80}\n")

for job in failed_jobs:
    print(f"\n{'─'*80}")
    print(f"Job ID: {job.id}")
    print(f"URL: {job.url}")
    print(f"Status: {job.status}")
    print(f"Created: {job.created_at}")
    print(f"Processed: {job.processed_at}")
    print(f"Retry Count: {job.retry_count}")
    
    # Primary error message
    if job.error_message:
        print(f"\n❌ Error Message:")
        print(f"   {job.error_message}")
    
    # Detailed error information
    if job.error_details:
        print(f"\n📋 Detailed Error Information:")
        try:
            if isinstance(job.error_details, str):
                error_data = json.loads(job.error_details)
            else:
                error_data = job.error_details
            
            if isinstance(error_data, dict):
                # Structured error data
                errors = error_data.get('errors', [])
                warnings = error_data.get('warnings', [])
                summary = error_data.get('summary', '')
                platform = error_data.get('platform_detected', 'Unknown')
                should_retry = error_data.get('should_retry', False)
                
                print(f"   Platform: {platform}")
                print(f"   Should Retry: {should_retry}")
                
                if summary:
                    print(f"   Summary: {summary}")
                
                if errors:
                    print(f"\n   Errors ({len(errors)}):")
                    for i, error in enumerate(errors, 1):
                        print(f"      {i}. [{error.get('severity', 'unknown').upper()}] {error.get('category', 'unknown')}")
                        print(f"         Message: {error.get('message', 'N/A')}")
                        if error.get('details'):
                            print(f"         Details: {error.get('details')[:200]}")
                        if error.get('suggested_action'):
                            print(f"         💡 Suggestion: {error.get('suggested_action')}")
                
                if warnings:
                    print(f"\n   Warnings ({len(warnings)}):")
                    for i, warning in enumerate(warnings, 1):
                        if isinstance(warning, dict):
                            print(f"      {i}. {warning.get('title', 'Warning')}: {warning.get('message', 'N/A')}")
                        else:
                            print(f"      {i}. {warning}")
            else:
                # Raw error data
                print(f"   {json.dumps(error_data, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"   Error parsing details: {str(e)}")
            print(f"   Raw: {job.error_details}")
    
    # Scraped data (if any was collected before failure)
    if job.scraped_data:
        print(f"\n📊 Scraped Data Available:")
        metadata = job.scraped_data.get('scraping_metadata', {})
        if metadata:
            print(f"   Quality Score: {metadata.get('data_quality', {}).get('percentage', 'N/A')}%")
            print(f"   Platform: {metadata.get('platform_detected', 'Unknown')}")
            print(f"   Warnings: {metadata.get('warnings_count', 0)}")
    
    print(f"\n{'─'*80}")

# Get a specific job by ID
def check_job(job_id):
    """Check a specific job by ID"""
    try:
        job = ProductScrapeJob.objects.get(id=job_id)
        print(f"\n{'='*80}")
        print(f"Job #{job.id} Details")
        print(f"{'='*80}")
        print(f"URL: {job.url}")
        print(f"Status: {job.status}")
        print(f"Error: {job.error_message}")
        if job.error_details:
            print(f"\nError Details:")
            print(json.dumps(job.error_details, indent=2, ensure_ascii=False))
        return job
    except ProductScrapeJob.DoesNotExist:
        print(f"Job #{job_id} not found")
        return None

# Example usage:
# check_job(123)  # Check job with ID 123



