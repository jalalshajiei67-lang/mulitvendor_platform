"""
Robust Error Handling System for Product Scraper
"""
import logging
import traceback
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)


class ErrorCategory(Enum):
    """Categories of scraping errors"""
    NETWORK = "network"
    SSL_CERTIFICATE = "ssl_certificate"
    HTTP_ERROR = "http_error"
    PARSING = "parsing"
    DATA_VALIDATION = "data_validation"
    IMAGE_DOWNLOAD = "image_download"
    DATABASE = "database"
    TIMEOUT = "timeout"
    PERMISSION = "permission"
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"  # Minor issues, scraping can continue
    MEDIUM = "medium"  # Some data missing but product can be created
    HIGH = "high"  # Critical error, cannot create product
    CRITICAL = "critical"  # System-level error


class ScraperError:
    """
    Structured error information
    """
    def __init__(
        self,
        category: ErrorCategory,
        severity: ErrorSeverity,
        message: str,
        details: Optional[str] = None,
        recoverable: bool = True,
        retry_recommended: bool = True,
        suggested_action: Optional[str] = None
    ):
        self.category = category
        self.severity = severity
        self.message = message
        self.details = details
        self.recoverable = recoverable
        self.retry_recommended = retry_recommended
        self.suggested_action = suggested_action
        self.timestamp = datetime.now()
        self.traceback = traceback.format_exc() if details is None else None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for storage"""
        return {
            'category': self.category.value,
            'severity': self.severity.value,
            'message': self.message,
            'details': self.details,
            'recoverable': self.recoverable,
            'retry_recommended': self.retry_recommended,
            'suggested_action': self.suggested_action,
            'timestamp': self.timestamp.isoformat(),
            'traceback': self.traceback
        }
    
    def get_user_friendly_message(self) -> str:
        """Get a user-friendly error message"""
        msg = f"[{self.severity.value.upper()}] {self.message}"
        if self.suggested_action:
            msg += f"\n💡 Suggestion: {self.suggested_action}"
        return msg


class ErrorHandler:
    """
    Centralized error handling for the scraper
    """
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def add_error(self, error: ScraperError):
        """Add an error to the error log"""
        self.errors.append(error)
        
        # Log to Django logger
        log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(error.severity, logging.ERROR)
        
        logger.log(
            log_level,
            f"{error.category.value}: {error.message}",
            extra={'details': error.details}
        )
    
    def add_warning(self, message: str, details: Optional[str] = None):
        """Add a warning (non-critical issue)"""
        self.warnings.append({
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        logger.warning(f"Warning: {message}", extra={'details': details})
    
    def has_critical_errors(self) -> bool:
        """Check if there are any critical errors"""
        return any(
            error.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
            for error in self.errors
        )
    
    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return len(self.errors) > 0
    
    def get_summary(self) -> str:
        """Get a summary of all errors and warnings"""
        if not self.errors and not self.warnings:
            return "No errors or warnings"
        
        summary = []
        
        if self.errors:
            summary.append(f"Errors: {len(self.errors)}")
            for error in self.errors:
                summary.append(f"  • {error.get_user_friendly_message()}")
        
        if self.warnings:
            summary.append(f"Warnings: {len(self.warnings)}")
            for warning in self.warnings[:5]:  # Limit to 5 warnings
                summary.append(f"  • {warning['message']}")
        
        return "\n".join(summary)
    
    def get_primary_error(self) -> Optional[ScraperError]:
        """Get the most severe error"""
        if not self.errors:
            return None
        
        # Sort by severity
        severity_order = {
            ErrorSeverity.CRITICAL: 0,
            ErrorSeverity.HIGH: 1,
            ErrorSeverity.MEDIUM: 2,
            ErrorSeverity.LOW: 3
        }
        
        return min(self.errors, key=lambda e: severity_order[e.severity])
    
    def should_retry(self) -> bool:
        """Determine if the operation should be retried"""
        if not self.errors:
            return False
        
        primary_error = self.get_primary_error()
        return primary_error.retry_recommended if primary_error else False
    
    def get_error_report(self) -> Dict[str, Any]:
        """Get a complete error report"""
        return {
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'has_critical_errors': self.has_critical_errors(),
            'should_retry': self.should_retry(),
            'summary': self.get_summary(),
            'errors': [error.to_dict() for error in self.errors],
            'warnings': self.warnings
        }


def handle_network_error(exception: Exception, url: str) -> ScraperError:
    """Handle network-related errors"""
    import requests
    
    error_msg = str(exception).lower()
    
    if isinstance(exception, requests.exceptions.SSLError):
        return ScraperError(
            category=ErrorCategory.SSL_CERTIFICATE,
            severity=ErrorSeverity.MEDIUM,
            message="SSL Certificate verification failed",
            details=str(exception),
            recoverable=True,
            retry_recommended=True,
            suggested_action="The scraper will automatically retry without SSL verification. If this persists, the website may have security issues."
        )
    
    elif isinstance(exception, requests.exceptions.Timeout):
        return ScraperError(
            category=ErrorCategory.TIMEOUT,
            severity=ErrorSeverity.MEDIUM,
            message="Request timed out (>30 seconds)",
            details=str(exception),
            recoverable=True,
            retry_recommended=True,
            suggested_action="The website is responding slowly. Wait a few minutes and retry. The website might be experiencing high traffic or issues."
        )
    
    elif isinstance(exception, requests.exceptions.ConnectionError):
        if 'getaddrinfo failed' in error_msg or 'nodename' in error_msg:
            return ScraperError(
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.HIGH,
                message=f"Cannot resolve domain name: {url}",
                details=str(exception),
                recoverable=True,
                retry_recommended=True,
                suggested_action="Check the URL spelling. If correct, check your internet connection or DNS settings."
            )
        elif 'connection refused' in error_msg:
            return ScraperError(
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.HIGH,
                message="Connection refused by the website",
                details=str(exception),
                recoverable=True,
                retry_recommended=True,
                suggested_action="The website may be down or blocking automated requests. Try again later or use a different network."
            )
        else:
            return ScraperError(
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.HIGH,
                message="Network connection error",
                details=str(exception),
                recoverable=True,
                retry_recommended=True,
                suggested_action="Check your internet connection. If connected, the website might be blocking requests or temporarily unavailable."
            )
    
    elif isinstance(exception, requests.exceptions.HTTPError):
        status_code = exception.response.status_code if hasattr(exception, 'response') else None
        
        if status_code == 403:
            return ScraperError(
                category=ErrorCategory.PERMISSION,
                severity=ErrorSeverity.HIGH,
                message="Access Forbidden (403): Website is blocking automated requests",
                details=str(exception),
                recoverable=False,
                retry_recommended=False,
                suggested_action="The website has anti-bot protection. Consider: 1) Getting permission from the site owner, 2) Using their API if available, or 3) Manually creating the product."
            )
        elif status_code == 404:
            return ScraperError(
                category=ErrorCategory.HTTP_ERROR,
                severity=ErrorSeverity.HIGH,
                message="Page Not Found (404): URL doesn't exist",
                details=str(exception),
                recoverable=False,
                retry_recommended=False,
                suggested_action="Check that the URL is correct. The product page may have been moved or deleted."
            )
        elif status_code == 500:
            return ScraperError(
                category=ErrorCategory.HTTP_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message="Server Error (500): Website is having issues",
                details=str(exception),
                recoverable=True,
                retry_recommended=True,
                suggested_action="The website is experiencing technical difficulties. Wait a few minutes and try again."
            )
        else:
            return ScraperError(
                category=ErrorCategory.HTTP_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"HTTP Error {status_code}",
                details=str(exception),
                recoverable=True,
                retry_recommended=True,
                suggested_action=f"The website returned an error. Status code: {status_code}. Try again later."
            )
    
    else:
        return ScraperError(
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.HIGH,
            message="Unknown network error",
            details=str(exception),
            recoverable=True,
            retry_recommended=True,
            suggested_action="An unexpected network error occurred. Check your internet connection and try again."
        )


def handle_parsing_error(exception: Exception, context: str) -> ScraperError:
    """Handle HTML parsing errors"""
    return ScraperError(
        category=ErrorCategory.PARSING,
        severity=ErrorSeverity.MEDIUM,
        message=f"Failed to parse {context}",
        details=str(exception),
        recoverable=True,
        retry_recommended=False,
        suggested_action=f"The webpage structure doesn't match expected format for {context}. The product will be created with default values. Review and edit manually."
    )


def handle_image_error(exception: Exception, image_url: str, image_index: int) -> ScraperError:
    """Handle image download errors"""
    return ScraperError(
        category=ErrorCategory.IMAGE_DOWNLOAD,
        severity=ErrorSeverity.LOW,
        message=f"Failed to download image #{image_index}",
        details=f"URL: {image_url}\nError: {str(exception)}",
        recoverable=True,
        retry_recommended=False,
        suggested_action="Some images couldn't be downloaded. The product will be created with available images. You can manually upload missing images later."
    )


def handle_validation_error(field: str, value: Any, reason: str) -> ScraperError:
    """Handle data validation errors"""
    return ScraperError(
        category=ErrorCategory.DATA_VALIDATION,
        severity=ErrorSeverity.LOW,
        message=f"Invalid data for {field}",
        details=f"Value: {value}\nReason: {reason}",
        recoverable=True,
        retry_recommended=False,
        suggested_action=f"The {field} data is invalid or missing. Default value will be used. Review and correct manually after creation."
    )


def handle_database_error(exception: Exception, operation: str) -> ScraperError:
    """Handle database operation errors"""
    return ScraperError(
        category=ErrorCategory.DATABASE,
        severity=ErrorSeverity.CRITICAL,
        message=f"Database error during {operation}",
        details=str(exception),
        recoverable=False,
        retry_recommended=True,
        suggested_action="A database error occurred. Check the Django logs. This might be a system issue requiring administrator attention."
    )

