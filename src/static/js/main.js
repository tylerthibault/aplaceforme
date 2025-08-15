(function(){
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (!prefersReduced && 'IntersectionObserver' in window) {
    // Enhanced scroll animations with staggered reveals
    const io = new IntersectionObserver(entries => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          // Add small delay for staggered effect
          setTimeout(() => {
            entry.target.classList.add('reveal');
          }, index * 100);
          io.unobserve(entry.target);
        }
      });
    }, { 
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    // Observe all animation elements
    document.querySelectorAll('.animate-on-scroll').forEach(el => io.observe(el));
    
    // Add subtle parallax effect to hero background
    const heroBackground = document.querySelector('.hero-bg');
    if (heroBackground) {
      window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.3;
        heroBackground.style.transform = `translateY(${rate}px)`;
      });
    }
  }
  
  // Enhanced form interactions
  const inputs = document.querySelectorAll('input, textarea');
  inputs.forEach(input => {
    const handleFocus = () => {
      input.parentElement?.classList.add('focused');
    };
    
    const handleBlur = () => {
      if (!input.value) {
        input.parentElement?.classList.remove('focused');
      }
    };
    
    input.addEventListener('focus', handleFocus);
    input.addEventListener('blur', handleBlur);
    
    // Check if input has value on load
    if (input.value) {
      input.parentElement?.classList.add('focused');
    }
  });
  
  // Add hover effects to cards
  const cards = document.querySelectorAll('.glass');
  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-4px)';
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0)';
    });
  });
})();
