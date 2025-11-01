/**
 * Django Admin Action Button Fix
 * Makes action button always visible and properly handles all actions including delete
 * Compatible with Django's default admin and Unfold theme
 */
(function () {
    'use strict';

    console.log('🔧 Admin action button fix loaded');

    function initActionButton() {
        // Find the action select dropdown
        const actionSelect = document.querySelector('select[name="action"]');

        if (!actionSelect) {
            console.warn('⚠️ Action select not found. Retrying...');
            setTimeout(initActionButton, 500);
            return;
        }

        console.log('✅ Action select found');

        // Find the action button (Go button) - Unfold uses different selectors
        const actionButton = document.querySelector('button[name="index"]') || 
                           document.querySelector('button[type="submit"][name="index"]') ||
                           document.querySelector('.actions button[type="submit"]') ||
                           document.querySelector('button[title="Run the selected action"]');

        if (!actionButton) {
            console.warn('⚠️ Action button not found');
            return;
        }

        console.log('✅ Action button found:', actionButton);

        // Remove Alpine.js attributes that might hide the button
        actionButton.removeAttribute('x-show');
        actionButton.removeAttribute('x-cloak');
        actionButton.removeAttribute('x-bind:style');

        // Force button to be visible - Use !important via setProperty for Unfold
        actionButton.style.setProperty('display', 'inline-flex', 'important');
        actionButton.style.setProperty('visibility', 'visible', 'important');
        actionButton.style.setProperty('opacity', '1', 'important');
        
        // Also remove any inline display:none that Alpine.js might set
        if (actionButton.hasAttribute('style')) {
            const currentStyle = actionButton.getAttribute('style');
            const newStyle = currentStyle.replace(/display\s*:\s*none\s*;?/gi, '');
            actionButton.setAttribute('style', newStyle);
        }
        
        console.log('✅ Button set to visible - Unfold theme');

        // Function to update button state based on selected action
        function updateButtonState() {
            const selectedAction = actionSelect.value;
            const selectedRows = document.querySelectorAll('input[name="_selected_action"]:checked').length;

            // Enable button if an action is selected
            if (selectedAction && selectedAction !== '' && selectedAction !== '---------') {
                // Always enable the button - let Django handle validation on submit
                actionButton.disabled = false;
                actionButton.style.opacity = '1';
                actionButton.style.cursor = 'pointer';
                actionButton.style.pointerEvents = 'auto';
                
                if (selectedAction === 'delete_selected' && selectedRows === 0) {
                    console.log('ℹ️ Delete action selected but no items checked - Django will show error');
                } else {
                    console.log('✅ Button enabled for action:', selectedAction);
                }
            } else {
                // Only disable button if no action selected
                actionButton.disabled = true;
                actionButton.style.opacity = '0.5';
                actionButton.style.cursor = 'not-allowed';
                console.log('ℹ️ Button disabled (no action selected)');
            }
        }

        // Listen for action dropdown changes
        actionSelect.addEventListener('change', function () {
            console.log('📢 Action changed to:', this.value);
            updateButtonState();
        });

        // Listen for checkbox changes (for delete action)
        document.addEventListener('change', function (e) {
            if (e.target && e.target.name === '_selected_action') {
                console.log('📢 Selection changed');
                updateButtonState();
            }
        });

        // Listen for "select all" checkbox
        const selectAllCheckbox = document.querySelector('input#action-toggle');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function () {
                console.log('📢 Select all toggled');
                setTimeout(updateButtonState, 100); // Small delay to let checkboxes update
            });
        }

        // Initial state
        updateButtonState();

        // Keep button visible even if Alpine.js tries to hide it (Unfold theme)
        const forceButtonVisible = () => {
            if (actionButton.style.display === 'none' || actionButton.style.display === '') {
                actionButton.style.setProperty('display', 'inline-flex', 'important');
                actionButton.style.setProperty('visibility', 'visible', 'important');
                actionButton.style.setProperty('opacity', '1', 'important');
                actionButton.removeAttribute('x-show');
                console.log('🔄 Button re-shown (Alpine.js tried to hide it)');
            }
        };

        // Watch for Alpine.js trying to hide the button
        const observer = new MutationObserver(() => {
            forceButtonVisible();
        });

        observer.observe(actionButton, {
            attributes: true,
            attributeFilter: ['style', 'x-show', 'class']
        });

        // Also check periodically (backup)
        setInterval(forceButtonVisible, 500);

        console.log('👁️ Button visibility watcher activated');

        // Allow the form to submit - Django will handle validation
        const actionForm = document.querySelector('#changelist-form');
        if (actionForm) {
            actionForm.addEventListener('submit', function(e) {
                const selectedAction = actionSelect.value;
                console.log('📤 Form submitting with action:', selectedAction);
                // Let Django handle the form submission and validation
                // Don't prevent default - allow normal form submission
            });
        }

        console.log('✅ Admin action button fix initialized successfully');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initActionButton);
    } else {
        initActionButton();
    }

    // Retry for late-loading content
    setTimeout(initActionButton, 1000);

    console.log('🎯 Admin action script loaded');
})();
