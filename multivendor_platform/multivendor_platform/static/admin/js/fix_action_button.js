/**
 * Simple Action Button Fix - Enable/Disable Approach
 * Makes button always visible and enables/disables based on action selection
 * No Alpine.js interaction = no race conditions
 */
(function () {
    'use strict';

    console.log('🔧 Simple action button fix loaded');

    function initActionButton() {
        // Find the action select
        const actionSelect = document.querySelector('select[name="action"]');

        if (!actionSelect) {
            console.warn('⚠️ Action select not found. Retrying...');
            setTimeout(initActionButton, 500);
            return;
        }

        console.log('✅ Action select found');

        // Find the button
        const actionButton = document.querySelector('button[name="index"]');

        if (!actionButton) {
            console.error('❌ Action button not found');
            return;
        }

        console.log('✅ Action button found');

        // STEP 1: Remove ALL Alpine.js attributes permanently
        actionButton.removeAttribute('x-show');
        actionButton.removeAttribute('x-cloak');
        actionButton.removeAttribute('x-bind:style');

        console.log('✅ Alpine.js attributes removed');

        // STEP 2: Make button always visible
        actionButton.style.display = 'flex';
        actionButton.style.visibility = 'visible';

        console.log('✅ Button set to always visible');

        // STEP 3: Function to enable/disable button based on selection
        function updateButtonState() {
            const selectedAction = actionSelect.value;

            if (selectedAction && selectedAction !== '' && selectedAction !== '---------') {
                // Enable button
                actionButton.disabled = false;
                actionButton.style.opacity = '1';
                actionButton.style.cursor = 'pointer';
                actionButton.style.pointerEvents = 'auto';
                actionButton.classList.remove('disabled');

                console.log('✅ Button enabled for action:', selectedAction);
            } else {
                // Disable button
                actionButton.disabled = true;
                actionButton.style.opacity = '0.5';
                actionButton.style.cursor = 'not-allowed';
                actionButton.style.pointerEvents = 'none';
                actionButton.classList.add('disabled');

                console.log('ℹ️ Button disabled (no action selected)');
            }
        }

        // STEP 4: Listen for select changes
        actionSelect.addEventListener('change', function () {
            console.log('📢 Action changed');
            updateButtonState();
        });

        actionSelect.addEventListener('input', function () {
            updateButtonState();
        });

        // STEP 5: Initial state
        updateButtonState();

        console.log('✅ Simple action button fix initialized successfully');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initActionButton);
    } else {
        initActionButton();
    }

    // Single retry for late-loading content
    setTimeout(initActionButton, 1000);

    console.log('🎯 Script loaded');
})();
