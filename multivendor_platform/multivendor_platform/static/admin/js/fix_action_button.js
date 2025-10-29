/**
 * Fix for Unfold admin action button not showing
 * This ensures the "Run" button appears when an action is selected
 */
(function () {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function () {
        // Find the action select element
        const actionSelect = document.querySelector('select[name="action"]');
        const runButton = document.querySelector('button[name="index"]');

        if (!actionSelect || !runButton) {
            return; // Elements not found, exit
        }

        // Function to show/hide the run button
        function updateButtonVisibility() {
            const selectedAction = actionSelect.value;

            if (selectedAction && selectedAction !== '') {
                // Show the button
                runButton.style.display = 'flex';
                runButton.removeAttribute('x-show');
            } else {
                // Hide the button
                runButton.style.display = 'none';
            }
        }

        // Listen for changes on the action select
        actionSelect.addEventListener('change', updateButtonVisibility);

        // Also check on page load in case an action is pre-selected
        updateButtonVisibility();

        // Handle "select all" functionality
        const selectAllCheckbox = document.getElementById('action-toggle');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function () {
                // When select all is toggled, recheck button visibility
                setTimeout(updateButtonVisibility, 100);
            });
        }
    });
})();

