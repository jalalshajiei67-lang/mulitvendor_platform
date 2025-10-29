/**
 * Fix for Unfold admin action button not showing
 * This ensures the "Run" button appears when an action is selected
 * Compatible with both standard Django admin and Unfold theme
 */
(function () {
    'use strict';

    // Wait for DOM to be ready
    function initActionButton() {
        // Find the action select element (try multiple selectors for compatibility)
        const actionSelect = document.querySelector('select[name="action"]') ||
            document.querySelector('#action-select') ||
            document.querySelector('[name="action"]');

        // Find the run button (try multiple selectors)
        const runButton = document.querySelector('button[name="index"]') ||
            document.querySelector('button[type="submit"][name="index"]') ||
            document.querySelector('.actions button[type="submit"]') ||
            document.querySelector('button.action-submit');

        if (!actionSelect || !runButton) {
            console.log('Action button fix: Elements not found, retrying...');
            // Retry after a short delay in case elements load later
            setTimeout(initActionButton, 500);
            return;
        }

        console.log('Action button fix: Elements found, initializing...');

        // Function to show/hide the run button
        function updateButtonVisibility() {
            const selectedAction = actionSelect.value;

            if (selectedAction && selectedAction !== '' && selectedAction !== '---------') {
                // Show the button
                runButton.style.display = 'flex';
                runButton.style.visibility = 'visible';
                runButton.style.opacity = '1';
                runButton.removeAttribute('x-show');
                runButton.removeAttribute('hidden');
                runButton.classList.remove('hidden');
                console.log('Action button fix: Button shown for action:', selectedAction);
            } else {
                // Hide the button
                runButton.style.display = 'none';
                runButton.style.visibility = 'hidden';
                runButton.style.opacity = '0';
                console.log('Action button fix: Button hidden (no action selected)');
            }
        }

        // Listen for changes on the action select
        actionSelect.addEventListener('change', updateButtonVisibility);

        // Also listen for input events (for better responsiveness)
        actionSelect.addEventListener('input', updateButtonVisibility);

        // Also check on page load in case an action is pre-selected
        updateButtonVisibility();

        // Handle "select all" functionality
        const selectAllCheckbox = document.getElementById('action-toggle') ||
            document.querySelector('input[name="_all"]') ||
            document.querySelector('.action-select-all');

        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function () {
                // When select all is toggled, recheck button visibility
                setTimeout(updateButtonVisibility, 100);
            });
        }

        // Watch for any item selection changes
        const checkboxes = document.querySelectorAll('input[name="_selected_action"]');
        checkboxes.forEach(function (checkbox) {
            checkbox.addEventListener('change', function () {
                setTimeout(updateButtonVisibility, 50);
            });
        });

        // Use MutationObserver to watch for DOM changes (for dynamic content)
        const observer = new MutationObserver(function (mutations) {
            mutations.forEach(function (mutation) {
                if (mutation.type === 'attributes' &&
                    (mutation.attributeName === 'style' ||
                        mutation.attributeName === 'class' ||
                        mutation.attributeName === 'x-show')) {
                    // Re-apply our visibility logic if something else changed the button
                    setTimeout(updateButtonVisibility, 10);
                }
            });
        });

        // Start observing the button for attribute changes
        observer.observe(runButton, {
            attributes: true,
            attributeFilter: ['style', 'class', 'x-show', 'hidden']
        });

        console.log('Action button fix: Initialized successfully');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initActionButton);
    } else {
        // DOM is already ready
        initActionButton();
    }

    // Also try after a delay (for cases where content loads asynchronously)
    setTimeout(initActionButton, 1000);
})();

