/**
 * Parallax Hero Section
 * Handles parallax scrolling effects and title animations
 */

class ParallaxHero {
    constructor() {
        this.hero = document.querySelector('.parallax-hero');
        this.layers = document.querySelectorAll('.parallax-layer');
        this.titleWords = document.querySelectorAll('.title-word');
        this.particles = document.querySelectorAll('.particle');
        
        this.isSupported = this.checkSupport();
        
        if (this.isSupported && this.hero) {
            this.init();
        }
    }
    
    checkSupport() {
        // Check for IntersectionObserver and requestAnimationFrame support
        return 'IntersectionObserver' in window && 'requestAnimationFrame' in window;
    }
    
    init() {
        this.setupIntersectionObserver();
        this.setupScrollListener();
        this.setupTitleAnimation();
        this.setupParticleAnimation();
        this.setupResizeListener();
        
        // Initial parallax position
        this.updateParallax();
    }
    
    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.startAnimations();
                }
            });
        }, options);
        
        this.observer.observe(this.hero);
    }
    
    setupScrollListener() {
        let ticking = false;
        
        const updateParallax = () => {
            this.updateParallax();
            ticking = false;
        };
        
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }, { passive: true });
    }
    
    updateParallax() {
        const scrolled = window.pageYOffset;
        const heroRect = this.hero.getBoundingClientRect();
        const heroTop = heroRect.top + scrolled;
        const heroHeight = heroRect.height;
        
        // Only apply parallax when hero is visible
        if (scrolled < heroTop + heroHeight && scrolled + window.innerHeight > heroTop) {
            this.layers.forEach(layer => {
                const speed = parseFloat(layer.dataset.speed) || 0.5;
                const yPos = -(scrolled - heroTop) * speed;
                
                // Use transform3d for better performance
                layer.style.transform = `translate3d(0, ${yPos}px, 0)`;
            });
            
            // Add subtle rotation to particles based on scroll
            this.particles.forEach((particle, index) => {
                const speed = 0.1 + (index * 0.02);
                const rotation = scrolled * speed;
                particle.style.transform = `rotate(${rotation}deg)`;
            });
        }
    }
    
    setupTitleAnimation() {
        // Enhanced title word animation with stagger effect
        this.titleWords.forEach((word, index) => {
            const customDelay = parseInt(word.dataset.delay) || 0;
            const baseDelay = 1500;
            const totalDelay = baseDelay + customDelay;
            
            setTimeout(() => {
                word.style.animationDelay = '0s';
                word.classList.add('animate');
                
                // Add hover effect after animation completes
                setTimeout(() => {
                    word.addEventListener('mouseenter', this.addTitleHoverEffect.bind(this, word));
                    word.addEventListener('mouseleave', this.removeTitleHoverEffect.bind(this, word));
                }, 1000);
            }, totalDelay);
        });
    }
    
    addTitleHoverEffect(word) {
        word.style.transform = 'translateY(-5px) scale(1.05)';
        word.style.filter = 'drop-shadow(0 10px 20px rgba(212, 175, 55, 0.5))';
        word.style.transition = 'all 0.3s ease';
    }
    
    removeTitleHoverEffect(word) {
        word.style.transform = 'translateY(0) scale(1)';
        word.style.filter = 'drop-shadow(0 5px 15px rgba(212, 175, 55, 0.3))';
    }
    
    setupParticleAnimation() {
        this.particles.forEach((particle, index) => {
            const delay = index * 1000;
            const duration = 8000 + (Math.random() * 4000); // Random duration between 8-12s
            
            this.animateParticle(particle, delay, duration);
        });
    }
    
    animateParticle(particle, delay, duration) {
        setTimeout(() => {
            particle.style.animationDuration = `${duration}ms`;
            particle.classList.add('animate');
            
            // Restart animation when it completes
            setTimeout(() => {
                particle.classList.remove('animate');
                this.animateParticle(particle, 0, duration);
            }, duration);
        }, delay);
    }
    
    setupResizeListener() {
        let resizeTimeout;
        
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.updateParallax();
            }, 150);
        });
    }
    
    startAnimations() {
        // Trigger any additional animations when hero comes into view
        this.hero.classList.add('in-view');
        
        // Enhanced particle effects
        setTimeout(() => {
            this.particles.forEach((particle, index) => {
                particle.style.opacity = '1';
                particle.style.animationPlayState = 'running';
            });
        }, 2000);
    }
    
    // Method to handle reduced motion preferences
    respectReducedMotion() {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        if (prefersReducedMotion.matches) {
            // Disable parallax and complex animations
            this.layers.forEach(layer => {
                layer.style.transform = 'none';
            });
            
            this.particles.forEach(particle => {
                particle.style.animation = 'none';
            });
        }
    }
}

// Enhanced scroll-to-element functionality
class SmoothScroll {
    constructor() {
        this.setupScrollButtons();
    }
    
    setupScrollButtons() {
        const scrollIndicator = document.querySelector('.scroll-indicator');
        const heroButtons = document.querySelectorAll('.hero-buttons a[href^="#"]');
        
        if (scrollIndicator) {
            scrollIndicator.addEventListener('click', () => {
                this.scrollToNextSection();
            });
        }
        
        heroButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = button.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    this.scrollToElement(targetElement);
                }
            });
        });
    }
    
    scrollToNextSection() {
        const hero = document.querySelector('.parallax-hero');
        const nextSection = hero.nextElementSibling;
        
        if (nextSection) {
            this.scrollToElement(nextSection);
        }
    }
    
    scrollToElement(element) {
        const offset = 80; // Account for any fixed headers
        const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
        const offsetPosition = elementPosition - offset;
        
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const parallaxHero = new ParallaxHero();
    const smoothScroll = new SmoothScroll();
    
    // Handle reduced motion preferences
    parallaxHero.respectReducedMotion();
    
    // Listen for changes in motion preferences
    const motionMediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    motionMediaQuery.addEventListener('change', () => {
        parallaxHero.respectReducedMotion();
    });
});

// Performance optimization: Pause animations when tab is not visible
document.addEventListener('visibilitychange', () => {
    const particles = document.querySelectorAll('.particle');
    const titleBehind = document.querySelector('.hero-title-behind');
    
    if (document.hidden) {
        // Pause animations
        particles.forEach(particle => {
            particle.style.animationPlayState = 'paused';
        });
        if (titleBehind) {
            titleBehind.style.animationPlayState = 'paused';
        }
    } else {
        // Resume animations
        particles.forEach(particle => {
            particle.style.animationPlayState = 'running';
        });
        if (titleBehind) {
            titleBehind.style.animationPlayState = 'running';
        }
    }
});
