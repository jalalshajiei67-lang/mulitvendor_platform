/**
 * Fix for Unfold Admin Action Button with Alpine.js
 * Forces the button to show by updating Alpine.js state
 */
(function () {
    'use strict';

    console.log('🔧 Action button fix loaded (Alpine.js compatible)');

    function initActionButton() {
        console.log('🔍 Searching for action elements...');

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

        // Find the parent container with Alpine.js x-data
        const alpineContainer = actionSelect.closest('[x-data]');
        
        if (alpineContainer) {
            console.log('✅ Alpine.js container found');
        }

        function updateButtonVisibility() {
            const selectedAction = actionSelect.value;

            console.log('🔄 Action changed:', selectedAction);

            if (selectedAction && selectedAction !== '' && selectedAction !== '---------') {
                // Method 1: Update Alpine.js state directly
                if (alpineContainer && typeof Alpine !== 'undefined') {
                    try {
                        Alpine.store(alpineContainer).action = selectedAction;
                        console.log('✅ Alpine.js state updated');
                    } catch (e) {
                        // Alpine store might not work, try direct property
                        if (alpineContainer._x_dataStack && alpineContainer._x_dataStack[0]) {
                            alpineContainer._x_dataStack[0].action = selectedAction;
                            console.log('✅ Alpine.js data stack updated');
                        }
                    }
                }

                // Method 2: Force CSS visibility (override everything)
                actionButton.style.setProperty('display', 'flex', 'important');
                actionButton.style.setProperty('visibility', 'visible', 'important');
                actionButton.style.setProperty('opacity', '1', 'important');
                actionButton.removeAttribute('x-cloak');
                actionButton.classList.remove('hidden');

                // Method 3: Remove the x-show attribute temporarily
                const xShowValue = actionButton.getAttribute('x-show');
                if (xShowValue) {
                    actionButton.removeAttribute('x-show');
                    // Re-add it after a moment to keep Alpine.js happy
                    setTimeout(() => {
                        actionButton.setAttribute('x-show', xShowValue);
                        // But keep forcing visibility
                        actionButton.style.setProperty('display', 'flex', 'important');
                    }, 100);
                }

                console.log('✅ Button forced visible');
            } else {
                actionButton.style.display = 'none';
                console.log('ℹ️ Button hidden (no action selected)');
            }
        }

        // Listen for changes
        actionSelect.addEventListener('change', updateButtonVisibility);
        actionSelect.addEventListener('input', updateButtonVisibility);

        // Initial check
        setTimeout(updateButtonVisibility, 100);

        // Aggressive polling - check every second
        setInterval(function() {
            const currentAction = actionSelect.value;
            if (currentAction && currentAction !== '' && currentAction !== '---------') {
                const computedStyle = window.getComputedStyle(actionButton);
                if (computedStyle.display === 'none') {
                    console.log('🔄 Button hidden detected, forcing visible...');
                    updateButtonVisibility();
                }
            }
        }, 1000);

        // Watch for Alpine.js mutations
        const observer = new MutationObserver(function(mutations) {
            for (let mutation of mutations) {
                if (mutation.attributeName === 'style' && mutation.target === actionButton) {
                    const currentAction = actionSelect.value;
                    if (currentAction && currentAction !== '' && currentAction !== '---------') {
                        if (actionButton.style.display === 'none' || actionButton.style.display === '') {
                            console.log('🔄 Alpine.js tried to hide button, forcing visible...');
                            setTimeout(updateButtonVisibility, 10);
                        }
                    }
                }
            }
        });

        observer.observe(actionButton, {
            attributes: true,
            attributeFilter: ['style', 'class']
        });

        console.log('✅ Action button fix initialized');
    }

    // Initialize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initActionButton);
    } else {
        initActionButton();
    }

    // Multiple retry attempts
    setTimeout(initActionButton, 500);
    setTimeout(initActionButton, 1500);
    setTimeout(initActionButton, 3000);

    console.log('🎯 Script fully loaded');
})();
