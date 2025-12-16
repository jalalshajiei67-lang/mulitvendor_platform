// admin/js/tiptap-loader.js
// Simple loader for Tiptap ES modules in Django admin
// This creates a simple wrapper that can load Tiptap modules

(function() {
    'use strict';
    
    // Since Tiptap v3 uses ES modules and we're in a non-module context,
    // we'll create a simple solution that works with the copied files
    
    // This function will be called after all Tiptap scripts are loaded
    window.initTiptapModules = function() {
        // Check what's available in the global scope
        // Tiptap modules might expose themselves differently depending on build format
        
        const modules = {
            Editor: null,
            StarterKit: null,
            Image: null,
            Link: null,
            Table: null,
            TableRow: null,
            TableCell: null,
            TableHeader: null
        };
        
        // Try to find modules in various possible locations
        // UMD builds typically expose as window.ModuleName or window['@tiptap/package-name']
        
        // Check for direct global exports
        if (typeof window.Editor !== 'undefined') {
            modules.Editor = window.Editor;
        }
        if (typeof window.StarterKit !== 'undefined') {
            modules.StarterKit = window.StarterKit;
        }
        
        // Check for namespaced exports
        if (window['@tiptap/core']) {
            const core = window['@tiptap/core'];
            if (core.Editor) modules.Editor = core.Editor;
            if (core.default && core.default.Editor) modules.Editor = core.default.Editor;
        }
        
        if (window['@tiptap/starter-kit']) {
            const starterKit = window['@tiptap/starter-kit'];
            if (starterKit.StarterKit) modules.StarterKit = starterKit.StarterKit;
            if (starterKit.default && starterKit.default.StarterKit) modules.StarterKit = starterKit.default.StarterKit;
        }
        
        // Store modules globally for tiptap-init.js to use
        window.TiptapModules = modules;
        
        return modules;
    };
    
    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.initTiptapModules);
    } else {
        window.initTiptapModules();
    }
})();

