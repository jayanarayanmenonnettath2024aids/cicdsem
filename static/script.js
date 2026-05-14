/* 
   Student Management System - JavaScript
   Enhanced interactivity and form validation
*/

// ==================== DOCUMENT READY ====================
// Execute code when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded and DOM content parsed');
    
    // Initialize tooltip functionality (if tooltips exist)
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Log application information
    logApplicationInfo();
});

// ==================== TOOLTIP FUNCTIONALITY ====================
/**
 * Initialize tooltip functionality
 * Shows helpful information on hover
 */
function initializeTooltips() {
    // Get all elements with title attribute
    const tooltips = document.querySelectorAll('[title]');
    
    tooltips.forEach(element => {
        // Add hover event listeners
        element.addEventListener('mouseenter', function(e) {
            // You could add custom tooltip logic here
            console.log('Tooltip hover: ' + this.title);
        });
    });
}

// ==================== FORM VALIDATION ====================
/**
 * Initialize form validation for all forms
 */
function initializeFormValidation() {
    // Get all forms on the page
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Add submit event listener
        form.addEventListener('submit', function(e) {
            // Validate form before submission
            if (!validateForm(this)) {
                e.preventDefault(); // Prevent form submission
            }
        });
        
        // Add input event listeners for real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                validateField(this);
            });
        });
    });
}

/**
 * Validate entire form
 * @param {HTMLFormElement} form - The form to validate
 * @returns {boolean} - True if form is valid, false otherwise
 */
function validateForm(form) {
    console.log('Validating form: ' + form.id);
    
    // Get all required fields
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    // Check each required field
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Validate a single field
 * @param {HTMLElement} field - The field to validate
 * @returns {boolean} - True if field is valid, false otherwise
 */
function validateField(field) {
    const value = field.value.trim();
    
    // Check if field is required and empty
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    // Validate email fields
    if (field.type === 'email' && value) {
        if (!isValidEmail(value)) {
            showFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }
    
    // Validate minimum length
    if (field.hasAttribute('minlength')) {
        const minLength = parseInt(field.getAttribute('minlength'));
        if (value.length < minLength && value.length > 0) {
            showFieldError(field, `Minimum ${minLength} characters required`);
            return false;
        }
    }
    
    // Clear error if field is now valid
    clearFieldError(field);
    return true;
}

/**
 * Check if email is valid
 * @param {string} email - The email to validate
 * @returns {boolean} - True if email is valid
 */
function isValidEmail(email) {
    // Basic email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Show error message for a field
 * @param {HTMLElement} field - The field with error
 * @param {string} message - Error message to display
 */
function showFieldError(field, message) {
    // Remove existing error (if any)
    clearFieldError(field);
    
    // Add error class to field
    field.classList.add('error');
    field.style.borderColor = '#e74c3c';
    
    // Create and show error message
    const errorElement = document.createElement('small');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    errorElement.style.color = '#e74c3c';
    
    // Insert error message after field
    field.parentNode.insertBefore(errorElement, field.nextSibling);
    
    console.warn('Field error: ' + message);
}

/**
 * Clear error message for a field
 * @param {HTMLElement} field - The field to clear error from
 */
function clearFieldError(field) {
    // Remove error class
    field.classList.remove('error');
    field.style.borderColor = '';
    
    // Remove error message element
    const errorElement = field.parentNode.querySelector('.error-message');
    if (errorElement) {
        errorElement.remove();
    }
}

// ==================== DELETE CONFIRMATION ====================
/**
 * Show confirmation dialog before deleting
 * This is handled by inline onsubmit attributes but included for reference
 */
function confirmDelete() {
    return confirm('Are you sure you want to delete this student? This action cannot be undone.');
}

// ==================== STUDENT ROW INTERACTION ====================
/**
 * Handle student row click - show details
 */
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.student-row');
    
    rows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f0f0f0';
            this.style.cursor = 'pointer';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
});

// ==================== API FUNCTIONS ====================
/**
 * Fetch all students via API
 * @returns {Promise} - Promise resolving to students array
 */
async function getAllStudents() {
    try {
        const response = await fetch('/api/students');
        
        if (!response.ok) {
            throw new Error('Failed to fetch students');
        }
        
        const data = await response.json();
        console.log('Students fetched successfully:', data);
        return data.data;
        
    } catch (error) {
        console.error('Error fetching students:', error);
        return [];
    }
}

/**
 * Fetch single student via API
 * @param {number} studentId - The ID of the student
 * @returns {Promise} - Promise resolving to student object
 */
async function getStudent(studentId) {
    try {
        const response = await fetch(`/api/students/${studentId}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch student');
        }
        
        const data = await response.json();
        console.log('Student fetched successfully:', data);
        return data.data;
        
    } catch (error) {
        console.error('Error fetching student:', error);
        return null;
    }
}

// ==================== UTILITY FUNCTIONS ====================
/**
 * Log application information
 */
function logApplicationInfo() {
    console.log('%c=== Student Management System ===', 'color: #3498db; font-size: 14px; font-weight: bold');
    console.log('Application: Cloud-Based Student Management System');
    console.log('Version: 1.0.0');
    console.log('Built with: Python, Flask, HTML5, CSS3, JavaScript');
    console.log('DevOps Demo: AWS CodeBuild, CodePipeline, GitHub Actions');
}

/**
 * Format date to readable format
 * @param {string} dateString - ISO date string
 * @returns {string} - Formatted date string
 */
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Show loading spinner
 * @param {boolean} show - Whether to show or hide spinner
 */
function showLoadingSpinner(show) {
    if (show) {
        document.body.style.opacity = '0.6';
        console.log('Loading...');
    } else {
        document.body.style.opacity = '1';
        console.log('Loading complete');
    }
}

/**
 * Show notification/toast message
 * @param {string} message - Message to display
 * @param {string} type - Type: 'success', 'error', 'info'
 * @param {number} duration - Duration in milliseconds
 */
function showNotification(message, type = 'info', duration = 3000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after duration
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// ==================== KEYBOARD SHORTCUTS ====================
/**
 * Handle keyboard shortcuts
 */
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + S: Save (prevent default browser save)
    if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        console.log('Save shortcut triggered');
        // Could submit form here if needed
    }
    
    // Escape: Close/Cancel
    if (event.key === 'Escape') {
        console.log('Escape key pressed');
        // Could clear form or close modal here
    }
});

// ==================== PERFORMANCE MONITORING ====================
/**
 * Log page performance metrics
 */
window.addEventListener('load', function() {
    // Get performance data
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    
    console.log('Page Performance Metrics:');
    console.log('Total Load Time: ' + pageLoadTime + 'ms');
    console.log('DOM Interactive: ' + (perfData.domInteractive - perfData.navigationStart) + 'ms');
    console.log('DOM Content Loaded: ' + (perfData.domContentLoadedEventEnd - perfData.navigationStart) + 'ms');
});

// ==================== ERROR HANDLING ====================
/**
 * Global error handler
 */
window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', event.error);
    // Could send to error tracking service here
});

/**
 * Handle unhandled promise rejections
 */
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled Promise Rejection:', event.reason);
    // Could send to error tracking service here
});

// ==================== ANIMATIONS ====================
/**
 * Add CSS animations (included in stylesheet via keyframes)
 */
const animationStyles = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;

// Inject animation styles
const styleSheet = document.createElement('style');
styleSheet.textContent = animationStyles;
document.head.appendChild(styleSheet);

console.log('JavaScript initialized successfully');
