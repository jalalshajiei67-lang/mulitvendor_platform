/**
 * Price Field Formatter - Adds thousand separators while typing
 * Formats: 123456789 -> 123,456,789
 * No decimals allowed
 */

(function() {
    'use strict';

    // Check if jQuery is available (either as $ or django.jQuery)
    var $ = window.django && window.django.jQuery ? window.django.jQuery : window.jQuery;
    
    if (!$) {
        console.error('jQuery not found. Price formatter cannot run.');
        return;
    }

    function formatPrice(value) {
        // Remove all non-digit characters
        var cleanValue = value.replace(/\D/g, '');
        
        // Add thousand separators
        if (cleanValue) {
            return cleanValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        }
        return '';
    }

    function getNumericValue(formattedValue) {
        // Remove commas to get numeric value for form submission
        return formattedValue.replace(/,/g, '');
    }

    $(document).ready(function() {
        // Find the price field by ID (Django admin generates id_price)
        var $priceField = $('#id_price');
        
        if ($priceField.length) {
            // Remove maxlength restriction if exists
            $priceField.removeAttr('maxlength');
            
            // Set input type to text to allow formatting
            $priceField.attr('type', 'text');
            
            // Format on input (while typing)
            $priceField.on('input', function() {
                var cursorPosition = this.selectionStart;
                var value = $(this).val();
                var numericValue = getNumericValue(value);
                
                // Format the value
                var formattedValue = formatPrice(numericValue);
                
                // Update the field value
                $(this).val(formattedValue);
                
                // Restore cursor position (adjust for added commas)
                var newCursorPosition = cursorPosition;
                var commasBeforeCursor = (value.substring(0, cursorPosition).match(/,/g) || []).length;
                var commasAfterFormat = (formattedValue.substring(0, cursorPosition).match(/,/g) || []).length;
                newCursorPosition = cursorPosition + (commasAfterFormat - commasBeforeCursor);
                
                this.setSelectionRange(newCursorPosition, newCursorPosition);
            });
            
            // Format on paste
            $priceField.on('paste', function(e) {
                var $this = $(this);
                setTimeout(function() {
                    var value = $this.val();
                    var numericValue = getNumericValue(value);
                    var formattedValue = formatPrice(numericValue);
                    $this.val(formattedValue);
                }, 10);
            });
            
            // Before form submission, remove commas from value
            $priceField.closest('form').on('submit', function() {
                var numericValue = getNumericValue($priceField.val());
                $priceField.val(numericValue);
            });
            
            // Format existing value on page load
            if ($priceField.val()) {
                var existingValue = $priceField.val().toString();
                // Remove all non-digit characters (commas, dots, etc.)
                var numericValue = existingValue.replace(/\D/g, '');
                if (numericValue) {
                    var formattedValue = formatPrice(numericValue);
                    $priceField.val(formattedValue);
                }
            }
        }
    });

})();

