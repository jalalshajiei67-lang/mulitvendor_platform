// TinyMCE custom image picker - opens file picker directly and uploads image
(function() {
  'use strict';
  
  // Custom file picker callback for images
  window.tinymceImageFilePicker = function(callback, value, meta) {
    // Only handle image file type
    if (meta.filetype !== 'image') {
      return;
    }
    
    // Create file input element
    var input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');
    input.style.display = 'none';
    
    // Handle file selection
    input.onchange = function() {
      var file = this.files[0];
      
      if (!file) {
        return;
      }
      
      // Validate file type
      if (!file.type.match('image.*')) {
        alert('لطفاً یک فایل تصویری انتخاب کنید');
        return;
      }
      
      // Validate file size (5MB max)
      if (file.size > 5 * 1024 * 1024) {
        alert('حجم فایل نباید بیشتر از 5 مگابایت باشد');
        return;
      }
      
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
      
      // Show loading indicator (optional)
      var loadingMsg = 'در حال آپلود تصویر...';
      
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
              // Success - call callback with image URL
              callback(response.location, {
                alt: file.name,
                title: file.name
              });
            } else if (response.error) {
              alert('خطا: ' + response.error);
            }
          } catch (e) {
            alert('خطا در پردازش پاسخ سرور');
          }
        } else {
          try {
            var errorResponse = JSON.parse(xhr.responseText);
            alert('خطا: ' + (errorResponse.error || 'آپلود تصویر ناموفق بود'));
          } catch (e) {
            alert('خطا در آپلود تصویر');
          }
        }
        
        // Remove input element
        document.body.removeChild(input);
      };
      
      xhr.onerror = function() {
        alert('خطا در ارتباط با سرور');
        document.body.removeChild(input);
      };
      
      // Send request
      xhr.send(formData);
    };
    
    // Trigger file picker
    document.body.appendChild(input);
    input.click();
  };
  
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

