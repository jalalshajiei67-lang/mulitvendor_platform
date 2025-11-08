// Admin JavaScript for multiple image uploads
document.addEventListener('DOMContentLoaded', function () {
    const multipleImagesInput = document.querySelector('input[name="multiple_images"]');

    if (multipleImagesInput) {
        // Add visual feedback for multiple file selection
        multipleImagesInput.addEventListener('change', function (e) {
            const files = e.target.files;
            const fileCount = files.length;

            // Create or update file count display
            let countDisplay = document.querySelector('.file-count-display');
            if (!countDisplay) {
                countDisplay = document.createElement('div');
                countDisplay.className = 'file-count-display';
                countDisplay.style.cssText = 'margin-top: 10px; padding: 10px; background: #e8f5e8; border: 1px solid #28a745; border-radius: 5px; font-size: 14px; font-weight: bold;';
                multipleImagesInput.parentNode.appendChild(countDisplay);
            }

            if (fileCount > 0) {
                countDisplay.innerHTML = `✅ Selected ${fileCount} image(s) ready for upload`;
                countDisplay.style.color = '#155724';
                countDisplay.style.backgroundColor = '#d4edda';
                countDisplay.style.borderColor = '#c3e6cb';

                // Show file names
                let fileList = document.querySelector('.file-list-display');
                if (!fileList) {
                    fileList = document.createElement('div');
                    fileList.className = 'file-list-display';
                    fileList.style.cssText = 'margin-top: 5px; padding: 5px; background: #f8f9fa; border-radius: 3px; font-size: 12px; max-height: 100px; overflow-y: auto;';
                    countDisplay.appendChild(fileList);
                }

                let fileNames = [];
                for (let i = 0; i < Math.min(files.length, 5); i++) {
                    fileNames.push(`• ${files[i].name}`);
                }
                if (files.length > 5) {
                    fileNames.push(`... and ${files.length - 5} more`);
                }
                fileList.innerHTML = fileNames.join('<br>');
            } else {
                countDisplay.innerHTML = '';
            }
        });

        // Add drag and drop functionality
        const formRow = multipleImagesInput.closest('.form-row');
        if (formRow) {
            formRow.style.border = '2px dashed #007cba';
            formRow.style.padding = '20px';
            formRow.style.borderRadius = '8px';
            formRow.style.textAlign = 'center';
            formRow.style.backgroundColor = '#f8f9fa';
            formRow.style.position = 'relative';
            formRow.style.cursor = 'pointer';

            // Add drag and drop text
            let dragText = document.createElement('div');
            dragText.innerHTML = '📁 Drag & drop multiple images here or click to select';
            dragText.style.cssText = 'color: #6c757d; font-size: 14px; margin-top: 10px;';
            formRow.appendChild(dragText);

            formRow.addEventListener('dragover', function (e) {
                e.preventDefault();
                formRow.style.borderColor = '#28a745';
                formRow.style.backgroundColor = '#e8f5e8';
                dragText.innerHTML = '📁 Drop images here!';
                dragText.style.color = '#155724';
            });

            formRow.addEventListener('dragleave', function (e) {
                e.preventDefault();
                formRow.style.borderColor = '#007cba';
                formRow.style.backgroundColor = '#f8f9fa';
                dragText.innerHTML = '📁 Drag & drop multiple images here or click to select';
                dragText.style.color = '#6c757d';
            });

            formRow.addEventListener('drop', function (e) {
                e.preventDefault();
                formRow.style.borderColor = '#007cba';
                formRow.style.backgroundColor = '#f8f9fa';
                dragText.innerHTML = '📁 Drag & drop multiple images here or click to select';
                dragText.style.color = '#6c757d';

                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    // Filter only image files
                    const imageFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
                    if (imageFiles.length > 0) {
                        // Create a new FileList-like object
                        const dt = new DataTransfer();
                        imageFiles.forEach(file => dt.items.add(file));
                        multipleImagesInput.files = dt.files;
                        multipleImagesInput.dispatchEvent(new Event('change'));
                    }
                }
            });

            // Add click handler to make the entire area clickable
            formRow.addEventListener('click', function (e) {
                if (e.target === formRow || e.target === dragText) {
                    multipleImagesInput.click();
                }
            });
        }
    }
});