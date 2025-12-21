// TinyMCE custom image picker - supports multiple images with ALT tags
(function() {
  'use strict';
  
  // Custom file picker callback for images
  window.tinymceImageFilePicker = function(callback, value, meta) {
    // Only handle image file type
    if (meta.filetype !== 'image') {
      return;
    }
    
    // Create file input element with multiple selection
    var input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');
    input.setAttribute('multiple', 'multiple');
    input.style.display = 'none';
    
    // Handle file selection
    input.onchange = function() {
      var files = Array.from(this.files);
      
      if (files.length === 0) {
        document.body.removeChild(input);
        return;
      }
      
      // Validate all files
      var validFiles = [];
      for (var i = 0; i < files.length; i++) {
        var file = files[i];
        
        // Validate file type
        if (!file.type.match('image.*')) {
          alert('فایل ' + file.name + ' یک فایل تصویری معتبر نیست');
          continue;
        }
        
        // Validate file size (5MB max)
        if (file.size > 5 * 1024 * 1024) {
          alert('حجم فایل ' + file.name + ' بیشتر از 5 مگابایت است');
          continue;
        }
        
        validFiles.push(file);
      }
      
      if (validFiles.length === 0) {
        document.body.removeChild(input);
        return;
      }
      
      // If single file, use simple flow with ALT dialog
      if (validFiles.length === 1) {
        uploadSingleImage(validFiles[0], callback, input);
      } else {
        // Multiple files - show ALT tag dialog for each
        uploadMultipleImages(validFiles, callback, input);
      }
    };
    
    // Trigger file picker
    document.body.appendChild(input);
    input.click();
  };
  
  // Upload single image with ALT tag prompt
  function uploadSingleImage(file, callback, inputElement) {
    // Show ALT tag dialog
    var altText = prompt('متن جایگزین (ALT) برای تصویر را وارد کنید:', file.name.replace(/\.[^/.]+$/, ''));
    if (altText === null) {
      // User cancelled
      document.body.removeChild(inputElement);
      return;
    }
    
    // Upload file
    uploadFile(file, function(imageUrl) {
      if (imageUrl) {
        // Get TinyMCE active editor instance
        var editor = null;
        if (typeof tinymce !== 'undefined') {
          editor = tinymce.activeEditor;
          // Fallback to first editor if no active editor
          if (!editor) {
            var editors = tinymce.get();
            if (editors && editors.length > 0) {
              editor = editors[0];
            }
          }
        }
        
        if (editor) {
          // Close any open dialogs
          try {
            editor.windowManager.close();
          } catch (e) {
            // Dialog might not be open, ignore error
          }
          
          // Insert image directly with ALT tag
          var altValue = altText || file.name;
          var imageHtml = '<img src="' + imageUrl + '" alt="' + escapeHtml(altValue) + '" title="' + escapeHtml(altValue) + '" />';
          editor.insertContent(imageHtml);
        }
        
        // Also call callback for compatibility
        callback(imageUrl, {
          alt: altText || file.name,
          title: altText || file.name
        });
      }
      document.body.removeChild(inputElement);
    });
  }
  
  // Upload multiple images with ALT tag dialog
  function uploadMultipleImages(files, callback, inputElement) {
    var uploadedImages = [];
    var currentIndex = 0;
    var altTags = [];
    
    // Create dialog for ALT tags
    showAltTagsDialog(files, function(altValues) {
      if (!altValues) {
        // User cancelled
        document.body.removeChild(inputElement);
        return;
      }
      
      altTags = altValues;
      
      // Upload all images sequentially
      uploadNextImage();
    });
    
    function uploadNextImage() {
      if (currentIndex >= files.length) {
        // All images uploaded, insert them all
        insertMultipleImages(uploadedImages, altTags, callback);
        document.body.removeChild(inputElement);
        return;
      }
      
      var file = files[currentIndex];
      var altText = altTags[currentIndex] || file.name.replace(/\.[^/.]+$/, '');
      
      uploadFile(file, function(imageUrl) {
        if (imageUrl) {
          uploadedImages.push({
            url: imageUrl,
            alt: altText,
            title: altText
          });
        }
        currentIndex++;
        uploadNextImage();
      });
    }
  }
  
  // Show dialog for entering ALT tags for multiple images
  function showAltTagsDialog(files, callback) {
    // Create modal dialog
    var modal = document.createElement('div');
    modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 10000; display: flex; align-items: center; justify-content: center;';
    modal.setAttribute('dir', 'rtl');
    
    var dialog = document.createElement('div');
    dialog.style.cssText = 'background: white; padding: 20px; border-radius: 8px; max-width: 600px; max-height: 80vh; overflow-y: auto; width: 90%;';
    
    var title = document.createElement('h3');
    title.textContent = 'وارد کردن متن جایگزین (ALT) برای تصاویر';
    title.style.cssText = 'margin-top: 0; margin-bottom: 20px; font-family: Vazir, sans-serif;';
    dialog.appendChild(title);
    
    var form = document.createElement('form');
    
    // Create input for each image
    var inputs = [];
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      var fileName = file.name;
      
      var label = document.createElement('label');
      label.textContent = 'تصویر ' + (i + 1) + ': ' + fileName;
      label.style.cssText = 'display: block; margin-bottom: 5px; font-weight: bold; font-family: Vazir, sans-serif;';
      form.appendChild(label);
      
      var input = document.createElement('input');
      input.type = 'text';
      input.value = fileName.replace(/\.[^/.]+$/, '');
      input.style.cssText = 'width: 100%; padding: 8px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px; font-family: Vazir, sans-serif; box-sizing: border-box;';
      input.placeholder = 'متن جایگزین (ALT)';
      form.appendChild(input);
      inputs.push(input);
    }
    
    // Buttons
    var buttonContainer = document.createElement('div');
    buttonContainer.style.cssText = 'margin-top: 20px; text-align: left;';
    
    var submitBtn = document.createElement('button');
    submitBtn.type = 'button';
    submitBtn.textContent = 'تأیید و آپلود';
    submitBtn.style.cssText = 'background: #007cba; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-family: Vazir, sans-serif; margin-left: 10px;';
    submitBtn.onclick = function() {
      var altValues = inputs.map(function(input) {
        return input.value.trim() || input.placeholder;
      });
      document.body.removeChild(modal);
      callback(altValues);
    };
    
    var cancelBtn = document.createElement('button');
    cancelBtn.type = 'button';
    cancelBtn.textContent = 'انصراف';
    cancelBtn.style.cssText = 'background: #ccc; color: black; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-family: Vazir, sans-serif;';
    cancelBtn.onclick = function() {
      document.body.removeChild(modal);
      callback(null);
    };
    
    buttonContainer.appendChild(submitBtn);
    buttonContainer.appendChild(cancelBtn);
    form.appendChild(buttonContainer);
    dialog.appendChild(form);
    modal.appendChild(dialog);
    document.body.appendChild(modal);
    
    // Focus first input
    if (inputs.length > 0) {
      inputs[0].focus();
    }
  }
  
  // Upload a single file
  function uploadFile(file, onSuccess) {
    // Create FormData for upload
    var formData = new FormData();
    formData.append('file', file);
    
    // Get CSRF token
    var csrftoken = getCookie('csrftoken');
    if (!csrftoken) {
      // Try to get from meta tag
      var metaTag = document.querySelector('meta[name=csrf-token]');
      if (metaTag) {
        csrftoken = metaTag.getAttribute('content');
      }
    }
    
    // Upload file
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/tinymce/upload-image/', true);
    
    if (csrftoken) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }
    
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          var response = JSON.parse(xhr.responseText);
          if (response.location) {
            onSuccess(response.location);
          } else if (response.error) {
            alert('خطا: ' + response.error);
            onSuccess(null);
          }
        } catch (e) {
          alert('خطا در پردازش پاسخ سرور');
          onSuccess(null);
        }
      } else {
        try {
          var errorResponse = JSON.parse(xhr.responseText);
          alert('خطا: ' + (errorResponse.error || 'آپلود تصویر ناموفق بود'));
        } catch (e) {
          alert('خطا در آپلود تصویر');
        }
        onSuccess(null);
      }
    };
    
    xhr.onerror = function() {
      alert('خطا در ارتباط با سرور');
      onSuccess(null);
    };
    
    // Send request
    xhr.send(formData);
  }
  
  // Insert multiple images into editor
  function insertMultipleImages(images, altTags, callback) {
    if (images.length === 0) {
      return;
    }
    
    // Get TinyMCE active editor instance
    var editor = null;
    if (typeof tinymce !== 'undefined') {
      editor = tinymce.activeEditor;
      // Fallback to first editor if no active editor
      if (!editor) {
        var editors = tinymce.get();
        if (editors && editors.length > 0) {
          editor = editors[0];
        }
      }
    }
    
    if (!editor) {
      // Fallback: use callback for first image
      if (images.length > 0) {
        callback(images[0].url, {
          alt: images[0].alt,
          title: images[0].title
        });
      }
      return;
    }
    
    // Close any open dialogs first
    try {
      editor.windowManager.close();
    } catch (e) {
      // Dialog might not be open, ignore error
    }
    
    // Insert all images
    var imageHtml = '';
    for (var i = 0; i < images.length; i++) {
      var img = images[i];
      imageHtml += '<img src="' + img.url + '" alt="' + escapeHtml(img.alt) + '" title="' + escapeHtml(img.title) + '" />';
      if (i < images.length - 1) {
        imageHtml += '<br />';
      }
    }
    
    // Insert into editor
    editor.insertContent(imageHtml);
    
    // Also call callback with first image URL for compatibility
    if (images.length > 0) {
      callback(images[0].url, {
        alt: images[0].alt,
        title: images[0].title
      });
    }
  }
  
  // Escape HTML
  function escapeHtml(text) {
    var map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
  }
  
  // Helper function to get CSRF token from cookie
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
})();

