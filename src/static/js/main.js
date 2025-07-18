/**
 * Main JavaScript file for A Place For Me
 * Handles global functionality and component initialization
 */

// Global app object
window.APlaceForMe = {
    components: {},
    utils: {},
    config: {
        breakpoints: {
            mobile: 480,
            tablet: 768,
            desktop: 1024
        }
    }
};

/**
 * Utility functions
 */
APlaceForMe.utils = {
    // Debounce function for performance optimization
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    // Throttle function for scroll events
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    },
    
    // Check if element is in viewport
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },
    
    // Get current breakpoint
    getCurrentBreakpoint: function() {
        const width = window.innerWidth;
        if (width <= APlaceForMe.config.breakpoints.mobile) return 'mobile';
        if (width <= APlaceForMe.config.breakpoints.tablet) return 'tablet';
        return 'desktop';
    }
};

/**
 * Base component class
 */
class BaseComponent {
    constructor(element, options = {}) {
        this.element = element;
        this.options = { ...this.defaults, ...options };
        this.init();
    }
    
    get defaults() {
        return {};
    }
    
    init() {
        // Override in child classes
    }
    
    destroy() {
        // Override in child classes for cleanup
    }
}

/**
 * Flash Message Handler
 */
class FlashMessages extends BaseComponent {
    get defaults() {
        return {
            autoHide: true,
            hideDelay: 5000,
            animationDuration: 300
        };
    }
    
    init() {
        this.messages = document.querySelectorAll('.flash-message');
        this.setupMessages();
    }
    
    setupMessages() {
        this.messages.forEach(message => {
            this.setupMessage(message);
        });
    }
    
    setupMessage(message) {
        // Add close button if not present
        if (!message.querySelector('.flash-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'flash-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.setAttribute('aria-label', 'Close message');
            message.appendChild(closeBtn);
            
            closeBtn.addEventListener('click', () => {
                this.hideMessage(message);
            });
        }
        
        // Auto-hide if enabled
        if (this.options.autoHide) {
            setTimeout(() => {
                this.hideMessage(message);
            }, this.options.hideDelay);
        }
        
        // Show message with animation
        setTimeout(() => {
            message.classList.add('show');
        }, 100);
    }
    
    hideMessage(message) {
        message.classList.add('hiding');
        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, this.options.animationDuration);
    }
}

/**
 * Navigation Handler
 */
class Navigation extends BaseComponent {
    init() {
        this.nav = document.querySelector('.main-nav');
        this.mobileToggle = document.querySelector('.mobile-nav-toggle');
        this.navLinks = document.querySelectorAll('.nav-link');
        
        if (this.nav) {
            this.setupMobileToggle();
            this.setupScrollBehavior();
            this.setupActiveLinks();
        }
    }
    
    setupMobileToggle() {
        if (this.mobileToggle) {
            this.mobileToggle.addEventListener('click', () => {
                this.nav.classList.toggle('nav-open');
                this.mobileToggle.classList.toggle('active');
            });
        }
    }
    
    setupScrollBehavior() {
        let lastScrollY = window.scrollY;
        
        const handleScroll = APlaceForMe.utils.throttle(() => {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                this.nav.classList.add('nav-scrolled');
            } else {
                this.nav.classList.remove('nav-scrolled');
            }
            
            // Hide nav on scroll down, show on scroll up
            if (currentScrollY > lastScrollY && currentScrollY > 200) {
                this.nav.classList.add('nav-hidden');
            } else {
                this.nav.classList.remove('nav-hidden');
            }
            
            lastScrollY = currentScrollY;
        }, 10);
        
        window.addEventListener('scroll', handleScroll, { passive: true });
    }
    
    setupActiveLinks() {
        // Add active class to current page link
        const currentPath = window.location.pathname;
        this.navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }
}

/**
 * Form Enhancement
 */
class FormEnhancer extends BaseComponent {
    init() {
        this.forms = document.querySelectorAll('form');
        this.setupForms();
    }
    
    setupForms() {
        this.forms.forEach(form => {
            this.enhanceForm(form);
        });
    }
    
    enhanceForm(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            this.enhanceInput(input);
        });
        
        // Add form validation
        form.addEventListener('submit', (e) => {
            if (!this.validateForm(form)) {
                e.preventDefault();
            }
        });
    }
    
    enhanceInput(input) {
        // Add floating label effect
        const wrapper = input.closest('.form-group');
        if (wrapper) {
            input.addEventListener('focus', () => {
                wrapper.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                if (!input.value) {
                    wrapper.classList.remove('focused');
                }
            });
            
            // Check initial state
            if (input.value) {
                wrapper.classList.add('focused');
            }
        }
    }
    
    validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('[required]');
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showError(input, 'This field is required');
                isValid = false;
            } else {
                this.clearError(input);
            }
        });
        
        return isValid;
    }
    
    showError(input, message) {
        const wrapper = input.closest('.form-group');
        if (wrapper) {
            wrapper.classList.add('error');
            
            let errorElement = wrapper.querySelector('.error-message');
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'error-message';
                wrapper.appendChild(errorElement);
            }
            errorElement.textContent = message;
        }
    }
    
    clearError(input) {
        const wrapper = input.closest('.form-group');
        if (wrapper) {
            wrapper.classList.remove('error');
            const errorElement = wrapper.querySelector('.error-message');
            if (errorElement) {
                errorElement.remove();
            }
        }
    }
}

/**
 * Loading States
 */
class LoadingManager {
    static show(element = document.body) {
        element.classList.add('loading');
    }
    
    static hide(element = document.body) {
        element.classList.remove('loading');
    }
    
    static showSpinner(container) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = '<div class="spinner"></div>';
        container.appendChild(spinner);
        return spinner;
    }
    
    static hideSpinner(spinner) {
        if (spinner && spinner.parentNode) {
            spinner.parentNode.removeChild(spinner);
        }
    }
}

/**
 * Initialize all components when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize core components
    new FlashMessages();
    new Navigation();
    new FormEnhancer();
    
    // Add loading states to buttons
    document.querySelectorAll('button[type="submit"], .btn-loading').forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                this.classList.add('loading');
                this.disabled = true;
            }
        });
    });
    
    // Handle external links
    document.querySelectorAll('a[href^="http"]:not([href*="' + window.location.hostname + '"])').forEach(link => {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Expose components globally
APlaceForMe.components = {
    BaseComponent,
    FlashMessages,
    Navigation,
    FormEnhancer,
    LoadingManager
};

// Handle page visibility for performance
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Pause any heavy animations or processes
        document.body.classList.add('page-hidden');
    } else {
        // Resume animations
        document.body.classList.remove('page-hidden');
    }
});

// Global error handling
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    // Could send to error reporting service
});

// Ensure parallax hero is loaded
if (document.querySelector('.parallax-hero')) {
    const script = document.createElement('script');
    script.src = '/static/js/parallax-hero.js';
    script.async = true;
    document.head.appendChild(script);
}
