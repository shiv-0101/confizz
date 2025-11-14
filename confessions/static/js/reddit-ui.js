// Reddit-like UI JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Smooth animations on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    // Observe all reddit-post elements
    document.querySelectorAll('.reddit-post').forEach(post => {
        post.style.opacity = '0';
        post.style.transform = 'translateY(10px)';
        post.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        observer.observe(post);
    });

    // Add hover effects
    document.querySelectorAll('.reddit-post').forEach(post => {
        post.addEventListener('mouseenter', function() {
            this.style.borderColor = 'var(--primary-color)';
        });
        post.addEventListener('mouseleave', function() {
            this.style.borderColor = 'var(--border-color)';
        });
    });

    // Vote animations
    document.querySelectorAll('.upvote-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            this.style.color = 'var(--upvote-color)';
            this.style.transform = 'scale(1.2)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 200);
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const textareas = this.querySelectorAll('textarea[required]');
            textareas.forEach(textarea => {
                if (textarea.value.trim().length === 0) {
                    e.preventDefault();
                    textarea.style.borderColor = 'var(--error-color)';
                    textarea.style.boxShadow = '0 0 0 2px rgba(239, 68, 68, 0.1)';
                    setTimeout(() => {
                        textarea.style.borderColor = 'var(--border-color)';
                        textarea.style.boxShadow = '';
                    }, 2000);
                }
            });
        });
    });

    // Ripple effect on buttons
    document.querySelectorAll('.reddit-btn, .reddit-post-action').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.animation = 'ripple 0.6s ease-out';
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            ripple.style.left = e.clientX - rect.left - 10 + 'px';
            ripple.style.top = e.clientY - rect.top - 10 + 'px';
        });
    });

    // Add ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Sidebar active link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.reddit-sidebar-nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    console.log('Reddit UI initialized successfully!');
});

// Utility function for formatting numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num;
}

// Utility function for relative time
function getRelativeTime(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    let interval = seconds / 31536000;

    if (interval > 1) {
        return Math.floor(interval) + ' years ago';
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        return Math.floor(interval) + ' months ago';
    }
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + ' days ago';
    }
    interval = seconds / 3600;
    if (interval > 1) {
        return Math.floor(interval) + ' hours ago';
    }
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + ' minutes ago';
    }
    return Math.floor(seconds) + ' seconds ago';
}
