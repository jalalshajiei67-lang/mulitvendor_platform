// admin/js/tiptap-init.js
// Initialize Tiptap editors in Django admin

(function() {
    'use strict';
    
    // Function to load Tiptap files dynamically
    function loadTiptapScripts(callback) {
        const scripts = [
            'admin/js/tiptap/core.js',
            'admin/js/tiptap/starter_kit.js',
            'admin/js/tiptap/extension_image.js',
            'admin/js/tiptap/extension_link.js',
            'admin/js/tiptap/extension_table.js',
            'admin/js/tiptap/extension_table_row.js',
            'admin/js/tiptap/extension_table_cell.js',
            'admin/js/tiptap/extension_table_header.js',
        ];
        
        let loaded = 0;
        let failed = 0;
        
        scripts.forEach((src, index) => {
            const script = document.createElement('script');
            script.src = '/' + src;
            script.onload = () => {
                loaded++;
                if (loaded + failed === scripts.length) {
                    if (loaded > 0) {
                        callback(true);
                    } else {
                        callback(false);
                    }
                }
            };
            script.onerror = () => {
                failed++;
                if (loaded + failed === scripts.length) {
                    if (loaded > 0) {
                        callback(true);
                    } else {
                        callback(false);
                    }
                }
            };
            document.head.appendChild(script);
        });
    }
    
    // Wait for Tiptap to be loaded
    function initTiptapEditor(editorId, fieldName) {
        // Check if Tiptap is available (check multiple possible global names)
        const hasTiptap = (
            (window['@tiptap/core'] && window['@tiptap/starter-kit']) ||
            (window.TiptapCore && window.TiptapStarterKit) ||
            (typeof window.Editor !== 'undefined') ||
            (window.TiptapModules && window.TiptapModules.Editor)
        );
        
        if (!hasTiptap) {
            // Try to load Tiptap files dynamically
            if (!window._tiptapLoading) {
                window._tiptapLoading = true;
                loadTiptapScripts(function(success) {
                    window._tiptapLoading = false;
                    if (success) {
                        // Retry initialization after a short delay
                        setTimeout(function() {
                            initTiptapEditor(editorId, fieldName);
                        }, 500);
                    } else {
                        // Show fallback message
                        showTiptapFallback(editorId);
                    }
                });
            } else {
                // Already loading, wait a bit more
                setTimeout(function() {
                    initTiptapEditor(editorId, fieldName);
                }, 200);
            }
            return;
        }
        
        const textarea = document.getElementById(editorId);
        if (!textarea) {
            console.warn('Textarea not found:', editorId);
            return;
        }
        
        const editorContainer = document.getElementById(editorId + '_editor');
        if (!editorContainer) {
            console.warn('Editor container not found:', editorId + '_editor');
            return;
        }
        
        const toolbarContainer = document.getElementById(editorId + '_toolbar');
        if (!toolbarContainer) {
            console.warn('Toolbar container not found:', editorId + '_toolbar');
            return;
        }
        
        // Hide the textarea
        textarea.style.display = 'none';
        
        // Create toolbar buttons
        const toolbar = document.createElement('div');
        toolbar.className = 'tiptap-toolbar-buttons';
        toolbar.innerHTML = `
            <button type="button" data-action="bold" title="Bold"><strong>B</strong></button>
            <button type="button" data-action="italic" title="Italic"><em>I</em></button>
            <button type="button" data-action="heading" data-level="1" title="Heading 1">H1</button>
            <button type="button" data-action="heading" data-level="2" title="Heading 2">H2</button>
            <button type="button" data-action="heading" data-level="3" title="Heading 3">H3</button>
            <button type="button" data-action="bulletList" title="Bullet List">• List</button>
            <button type="button" data-action="orderedList" title="Numbered List">1. List</button>
            <button type="button" data-action="link" title="Link">🔗</button>
            <button type="button" data-action="image" title="Image">🖼️</button>
            <button type="button" data-action="table" title="Table">⊞</button>
        `;
        toolbarContainer.appendChild(toolbar);
        
        // Initialize Tiptap editor
        try {
            // Wait a bit for modules to load
            let Editor, StarterKit, Image, Link, Table, TableRow, TableCell, TableHeader;
            
            // Try to get from TiptapModules (set by tiptap-loader.js)
            if (window.TiptapModules) {
                Editor = window.TiptapModules.Editor;
                StarterKit = window.TiptapModules.StarterKit;
                Image = window.TiptapModules.Image;
                Link = window.TiptapModules.Link;
                Table = window.TiptapModules.Table;
                TableRow = window.TiptapModules.TableRow;
                TableCell = window.TiptapModules.TableCell;
                TableHeader = window.TiptapModules.TableHeader;
            }
            
            // Fallback: Try direct global access
            if (!Editor && typeof window.Editor !== 'undefined') {
                Editor = window.Editor;
            }
            if (!StarterKit && typeof window.StarterKit !== 'undefined') {
                StarterKit = window.StarterKit;
            }
            
            // Fallback: Try namespaced access
            if (!Editor && window['@tiptap/core']) {
                const TiptapCore = window['@tiptap/core'];
                Editor = TiptapCore.Editor || (TiptapCore.default && TiptapCore.default.Editor);
            }
            if (!StarterKit && window['@tiptap/starter-kit']) {
                const TiptapStarterKit = window['@tiptap/starter-kit'];
                StarterKit = TiptapStarterKit.StarterKit || (TiptapStarterKit.default && TiptapStarterKit.default.StarterKit);
            }
            
            // Get extensions
            if (!Image && window['@tiptap/extension-image']) {
                const TiptapImage = window['@tiptap/extension-image'];
                Image = TiptapImage.Image || (TiptapImage.default && TiptapImage.default.Image);
            }
            if (!Link && window['@tiptap/extension-link']) {
                const TiptapLink = window['@tiptap/extension-link'];
                Link = TiptapLink.Link || (TiptapLink.default && TiptapLink.default.Link);
            }
            if (!Table && window['@tiptap/extension-table']) {
                const TiptapTable = window['@tiptap/extension-table'];
                Table = TiptapTable.Table || (TiptapTable.default && TiptapTable.default.Table);
            }
            if (!TableRow && window['@tiptap/extension-table-row']) {
                const TiptapTableRow = window['@tiptap/extension-table-row'];
                TableRow = TiptapTableRow.TableRow || (TiptapTableRow.default && TiptapTableRow.default.TableRow);
            }
            if (!TableCell && window['@tiptap/extension-table-cell']) {
                const TiptapTableCell = window['@tiptap/extension-table-cell'];
                TableCell = TiptapTableCell.TableCell || (TiptapTableCell.default && TiptapTableCell.default.TableCell);
            }
            if (!TableHeader && window['@tiptap/extension-table-header']) {
                const TiptapTableHeader = window['@tiptap/extension-table-header'];
                TableHeader = TiptapTableHeader.TableHeader || (TiptapTableHeader.default && TiptapTableHeader.default.TableHeader);
            }
            
            if (!Editor || !StarterKit) {
                throw new Error('Tiptap core libraries (Editor, StarterKit) not found. Please run: python manage.py copy_tiptap_static');
            }
            
            const extensions = [StarterKit];
            
            if (Image) {
                extensions.push(Image.configure({ inline: true, allowBase64: true }));
            }
            if (Link) {
                extensions.push(Link.configure({ openOnClick: false }));
            }
            if (Table && TableRow && TableCell && TableHeader) {
                extensions.push(Table.configure({ resizable: true }));
                extensions.push(TableRow);
                extensions.push(TableHeader);
                extensions.push(TableCell);
            }
            
            const editor = new Editor({
                element: editorContainer,
                extensions: extensions,
                content: textarea.value || '',
                onUpdate: ({ editor }) => {
                    textarea.value = editor.getHTML();
                },
                editorProps: {
                    attributes: {
                        class: 'tiptap-editor-content',
                        dir: 'rtl',
                        style: 'min-height: 300px; padding: 16px; border: 1px solid #ddd; border-radius: 4px;'
                    }
                }
            });
            
            // Store editor instance
            window['tiptap_' + editorId] = editor;
            
            // Toolbar button handlers
            toolbar.addEventListener('click', function(e) {
                const button = e.target.closest('button');
                if (!button) return;
                
                const action = button.getAttribute('data-action');
                const level = button.getAttribute('data-level');
                
                e.preventDefault();
                
                switch(action) {
                    case 'bold':
                        editor.chain().focus().toggleBold().run();
                        break;
                    case 'italic':
                        editor.chain().focus().toggleItalic().run();
                        break;
                    case 'heading':
                        if (level) {
                            editor.chain().focus().toggleHeading({ level: parseInt(level) }).run();
                        }
                        break;
                    case 'bulletList':
                        editor.chain().focus().toggleBulletList().run();
                        break;
                    case 'orderedList':
                        editor.chain().focus().toggleOrderedList().run();
                        break;
                    case 'link':
                        const url = prompt('Enter URL:');
                        if (url) {
                            editor.chain().focus().setLink({ href: url }).run();
                        }
                        break;
                    case 'image':
                        const imageUrl = prompt('Enter image URL:');
                        if (imageUrl) {
                            editor.chain().focus().setImage({ src: imageUrl }).run();
                        }
                        break;
                    case 'table':
                        editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run();
                        break;
                }
            });
            
            // Update active states
            editor.on('selectionUpdate', () => {
                toolbar.querySelectorAll('button').forEach(btn => {
                    const action = btn.getAttribute('data-action');
                    const level = btn.getAttribute('data-level');
                    
                    if (action === 'bold' && editor.isActive('bold')) {
                        btn.classList.add('active');
                    } else if (action === 'italic' && editor.isActive('italic')) {
                        btn.classList.add('active');
                    } else if (action === 'heading' && level && editor.isActive('heading', { level: parseInt(level) })) {
                        btn.classList.add('active');
                    } else {
                        btn.classList.remove('active');
                    }
                });
            });
            
        } catch (error) {
            console.error('Error initializing Tiptap editor:', error);
            console.error('Error details:', error.message, error.stack);
            showTiptapFallback(editorId);
        }
    }
    
    function showTiptapFallback(editorId) {
        const textarea = document.getElementById(editorId);
        const editorContainer = document.getElementById(editorId + '_editor');
        const toolbarContainer = document.getElementById(editorId + '_toolbar');
        
        if (textarea) {
            textarea.style.display = 'block';
        }
        if (editorContainer) {
            editorContainer.style.display = 'none';
        }
        if (toolbarContainer) {
            toolbarContainer.style.display = 'none';
        }
        
        // Show a message to the user
        if (textarea && !document.getElementById(editorId + '_fallback_msg')) {
            const errorMsg = document.createElement('div');
            errorMsg.id = editorId + '_fallback_msg';
            errorMsg.className = 'tiptap-error';
            errorMsg.style.cssText = 'padding: 10px; background: #fff3cd; border: 1px solid #ffc107; border-radius: 4px; margin-top: 10px; direction: rtl; text-align: right;';
            errorMsg.innerHTML = '<strong>⚠️ توجه:</strong> فایل‌های Tiptap یافت نشد. لطفاً دستور زیر را اجرا کنید:<br><code style="background: #f8f9fa; padding: 4px 8px; border-radius: 3px; font-family: monospace;">python manage.py copy_tiptap_static</code><br><small>در حال حاضر از فیلد متنی ساده استفاده می‌شود.</small>';
            if (textarea.parentNode) {
                textarea.parentNode.insertBefore(errorMsg, textarea.nextSibling);
            }
        }
    }
    
    // Make function globally available
    window.initTiptapEditor = initTiptapEditor;
    
    // Auto-initialize on page load
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.tiptap-editor-textarea').forEach(function(textarea) {
            const editorId = textarea.id;
            const fieldName = textarea.name;
            if (editorId && fieldName) {
                initTiptapEditor(editorId, fieldName);
            }
        });
    });
})();

