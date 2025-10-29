/**
 * Fix for Unfold Admin Action Button with Alpine.js
 * Directly updates Alpine.js reactive state and forces button visibility
 */
(function () {
    'use strict';

    console.log('🔧 Action button fix loaded (Alpine.js v3 compatible)');

    function initActionButton() {
        console.log('🔍 Searching for action elements...');

        // Find the action select
        const actionSelect = document.querySelector('select[name="action"]');
        
        if (!actionSelect) {
            console.warn('⚠️ Action select not found. Retrying...');
            setTimeout(initActionButton, 500);
            return;
        }

        console.log('✅ Action select found:', actionSelect);

        // Find the button
        const actionButton = document.querySelector('button[name="index"]');
        
        if (!actionButton) {
            console.error('❌ Action button not found');
            return;
        }

        console.log('✅ Action button found:', actionButton);

        // Find the parent container with Alpine.js x-data
        const alpineContainer = actionSelect.closest('[x-data]');
        
        if (alpineContainer) {
            console.log('✅ Alpine.js container found:', alpineContainer);
        }

        function updateButtonVisibility() {
            const selectedAction = actionSelect.value;

            console.log('🔄 Action changed to:', selectedAction);

            if (selectedAction && selectedAction !== '' && selectedAction !== '---------') {
                
                // Method 1: Update Alpine.js using Alpine's public API (v3+)
                if (alpineContainer) {
                    try {
                        // Try Alpine.js v3 method - set the component data directly
                        if (window.Alpine && Alpine.raw) {
                            const data = Alpine.raw(alpineContainer);
                            if (data) {
                                data.action = selectedAction;
                                console.log('✅ Alpine.js v3 data updated');
                            }
                        }
                        
                        // Try accessing _x_dataStack (Alpine.js internal)
                        if (alpineContainer._x_dataStack && alpineContainer._x_dataStack[0]) {
                            alpineContainer._x_dataStack[0].action = selectedAction;
                            console.log('✅ Alpine.js _x_dataStack updated');
                        }
                        
                        // Try using __x (Alpine.js v3 internal)
                        if (alpineContainer.__x) {
                            alpineContainer.__x.$data.action = selectedAction;
                            console.log('✅ Alpine.js __x data updated');
                        }
                    } catch (e) {
                        console.warn('⚠️ Could not update Alpine.js state:', e.message);
                    }
                }

                // Method 2: Completely remove x-show and force visibility
                console.log('🔧 Forcing button visibility with CSS...');
                
                // Remove Alpine.js directives
                actionButton.removeAttribute('x-show');
                actionButton.removeAttribute('x-cloak');
                actionButton.removeAttribute('x-bind:style');
                
                // Force visibility with inline styles (highest priority)
                actionButton.style.cssText = 'display: flex !important; visibility: visible !important; opacity: 1 !important;';
                
                // Remove hidden classes
                actionButton.classList.remove('hidden');
                
                console.log('✅ Button forced visible');
            } else {
                // Hide the button when no action is selected
                actionButton.style.display = 'none';
                console.log('ℹ️ Button hidden (no action selected)');
            }
        }

        // Listen for changes on the action select
        actionSelect.addEventListener('change', function(e) {
            console.log('📢 Select change event fired');
            updateButtonVisibility();
        });
        
        actionSelect.addEventListener('input', function(e) {
            console.log('📢 Select input event fired');
            updateButtonVisibility();
        });

        // Trigger on any clicks in the select
        actionSelect.addEventListener('click', function() {
            setTimeout(updateButtonVisibility, 50);
        });

        // Initial check
        setTimeout(updateButtonVisibility, 100);
        setTimeout(updateButtonVisibility, 500);

        // Ultra-aggressive polling - check every 500ms
        setInterval(function() {
            const currentAction = actionSelect.value;
            if (currentAction && currentAction !== '' && currentAction !== '---------') {
                // Check if button is still hidden
                const computedStyle = window.getComputedStyle(actionButton);
                const isHidden = computedStyle.display === 'none' || 
                                computedStyle.visibility === 'hidden' || 
                                computedStyle.opacity === '0';
                
                if (isHidden) {
                    console.log('🔄 Button hidden detected in polling, forcing visible...');
                    updateButtonVisibility();
                }
            }
        }, 500);

        // Watch for any attribute or style changes on the button
        const observer = new MutationObserver(function(mutations) {
            const currentAction = actionSelect.value;
            if (currentAction && currentAction !== '' && currentAction !== '---------') {
                for (let mutation of mutations) {
                    if (mutation.type === 'attributes') {
                        const computedStyle = window.getComputedStyle(actionButton);
                        if (computedStyle.display === 'none') {
                            console.log('🔄 Button was hidden by mutation, re-forcing visible...');
                            setTimeout(updateButtonVisibility, 10);
                            break;
                        }
                    }
                }
            }
        });

        observer.observe(actionButton, {
            attributes: true,
            attributeFilter: ['style', 'class', 'x-show', 'x-cloak']
        });

        // Also watch the parent container for changes
        if (alpineContainer) {
            const containerObserver = new MutationObserver(function() {
                const currentAction = actionSelect.value;
                if (currentAction && currentAction !== '' && currentAction !== '---------') {
                    setTimeout(updateButtonVisibility, 10);
                }
            });
            
            containerObserver.observe(alpineContainer, {
                attributes: true,
                subtree: true
            });
        }

        console.log('✅ Action button fix fully initialized');
        
        // Force one more check after everything is set up
        setTimeout(updateButtonVisibility, 1000);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initActionButton);
    } else {
        initActionButton();
    }

    // Multiple initialization attempts for different loading scenarios
    setTimeout(initActionButton, 100);
    setTimeout(initActionButton, 500);
    setTimeout(initActionButton, 1000);
    setTimeout(initActionButton, 2000);

    console.log('🎯 Script fully loaded and scheduled');
})();
