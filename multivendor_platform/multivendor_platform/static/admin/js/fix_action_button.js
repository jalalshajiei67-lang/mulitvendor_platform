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

        // Find the action button (Go button)
        const actionButton = document.querySelector('button[name="index"]') || 
                           document.querySelector('button[type="submit"][name="index"]') ||
                           document.querySelector('.actions button[type="submit"]');

        if (!actionButton) {
            console.warn('⚠️ Action button not found');
            return;
        }

        console.log('✅ Action button found');

        // Remove Alpine.js attributes that might hide the button
        actionButton.removeAttribute('x-show');
        actionButton.removeAttribute('x-cloak');
        actionButton.removeAttribute('x-bind:style');

        // Force button to be visible
        actionButton.style.display = 'inline-flex';
        actionButton.style.visibility = 'visible';
        
        console.log('✅ Button set to visible');

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
