// Amazon KDP Book Catalog - Main JavaScript

// Load bestsellers data and render books
async function loadBestsellers() {
    try {
        const response = await fetch('/data/bestsellers.json');
        const bestsellers = await response.json();
        renderBestsellers(bestsellers);
    } catch (error) {
        console.error('Error loading bestsellers:', error);
    }
}

// Render bestsellers in grid
function renderBestsellers(bestsellers) {
    const grids = document.querySelectorAll('#bestsellers-grid');
    
    grids.forEach(grid => {
        grid.innerHTML = '';
        
        bestsellers.forEach(book => {
            const bookCard = createBookCard(book);
            grid.appendChild(bookCard);
        });
    });
}

// Create book card element
function createBookCard(book) {
    const card = document.createElement('div');
    card.className = 'book-card';
    
    card.innerHTML = `
        <img src="${book.image_url}" alt="${book.title}" class="book-card-image">
        <h3>${book.title}</h3>
        <a href="${book.amazon_link}" class="btn btn-amazon" target="_blank" rel="noopener">Buy on Amazon</a>
    `;
    
    return card;
}

// Sticky buy button functionality
function initStickyBuyButton() {
    const stickyBuy = document.getElementById('stickyBuy');
    if (!stickyBuy) return;
    
    let lastScrollY = window.scrollY;
    let ticking = false;
    
    function updateStickyButton() {
        const scrollY = window.scrollY;
        const heroSection = document.querySelector('.book-hero');
        
        if (heroSection) {
            const heroBottom = heroSection.offsetTop + heroSection.offsetHeight;
            
            // Show sticky button when scrolled past hero section
            if (scrollY > heroBottom + 100) {
                stickyBuy.classList.add('show');
            } else {
                stickyBuy.classList.remove('show');
            }
        }
        
        lastScrollY = scrollY;
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            window.requestAnimationFrame(updateStickyButton);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add hover effects to book cards
function initBookCardEffects() {
    const bookCards = document.querySelectorAll('.book-card');
    
    bookCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-4px) scale(1)';
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadBestsellers();
    initStickyBuyButton();
    initSmoothScrolling();
    initBookCardEffects();
});

// Handle page visibility changes for performance
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden, pause any animations or heavy operations
        console.log('Page hidden - pausing operations');
    } else {
        // Page is visible again, resume operations
        console.log('Page visible - resuming operations');
    }
});

// Add loading states for images
function initImageLoading() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.classList.add('loaded');
        });
        
        img.addEventListener('error', function() {
            this.classList.add('error');
            // You could add a placeholder image here
            console.warn('Image failed to load:', this.src);
        });
    });
}

// Initialize image loading after DOM is ready
document.addEventListener('DOMContentLoaded', initImageLoading);

// Utility function to debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced scroll performance with debouncing
const optimizedScroll = debounce(function() {
    // Add any scroll-based optimizations here
}, 100);

window.addEventListener('scroll', optimizedScroll);

// Add keyboard navigation support
function initKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        // Press 'Escape' to close sticky buy button if it's showing
        if (e.key === 'Escape') {
            const stickyBuy = document.getElementById('stickyBuy');
            if (stickyBuy && stickyBuy.classList.contains('show')) {
                stickyBuy.classList.remove('show');
            }
        }
        
        // Press '/' to focus search (if you add search functionality)
        if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
            const searchInput = document.querySelector('#search-input');
            if (searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', initKeyboardNavigation);

// Performance monitoring
function logPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.fetchStart, 'ms');
        });
    }
}

logPerformance();
