/**
 * THÈME PREMIUM - INTERACTIONS JAVASCRIPT
 * Effets visuels premium et interactions sensuel
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ================================================
    // EFFET DE RÉVÉLATION AU SCROLL
    // ================================================
    function setupScrollReveal() {
        const revealElements = document.querySelectorAll('.reveal');
        
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        revealElements.forEach(el => {
            revealObserver.observe(el);
        });
    }

    // ================================================
    // EFFET DE LUMIÈRE QUI SUIT LA SOURIS
    // ================================================
    function setupMouseLight() {
        const mouseLightElements = document.querySelectorAll('.mouse-light');
        
        mouseLightElements.forEach(element => {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = ((e.clientX - rect.left) / rect.width) * 100;
                const y = ((e.clientY - rect.top) / rect.height) * 100;
                
                element.style.setProperty('--mouse-x', x + '%');
                element.style.setProperty('--mouse-y', y + '%');
            });
        });
    }

    // ================================================
    // ANIMATION D'ENTRÉE PROGRESSIVE POUR LES CARTES
    // ================================================
    function setupStaggeredAnimation() {
        const cards = document.querySelectorAll('.card, .hover-card');
        
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('animate-slide-in-bottom');
        });
    }

    // ================================================
    // EFFET DE PARTICULES FLOTTANTES
    // ================================================
    function createFloatingParticles() {
        const heroSection = document.querySelector('.hero-section');
        if (!heroSection) return;

        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'floating-particles';
        heroSection.appendChild(particlesContainer);

        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 3 + 's';
            particle.style.animationDuration = (3 + Math.random() * 2) + 's';
            particlesContainer.appendChild(particle);
        }
    }

    // ================================================
    // EFFET DE TYPING POUR LES TITRES
    // ================================================
    function setupTypingEffect() {
        const typingElements = document.querySelectorAll('.typing-effect');
        
        typingElements.forEach(element => {
            const text = element.textContent;
            element.textContent = '';
            element.style.width = '0';
            
            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    element.style.width = ((i + 1) / text.length * 100) + '%';
                    i++;
                    setTimeout(typeWriter, 100);
                }
            };
            
            // Démarrer l'effet après un délai
            setTimeout(typeWriter, 1000);
        });
    }

    // ================================================
    // SMOOTH SCROLL PREMIUM
    // ================================================
    function setupSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ================================================
    // EFFET DE CLIGNOTEMENT POUR LES NOTIFICATIONS
    // ================================================
    function setupNotificationEffects() {
        const alerts = document.querySelectorAll('.alert');
        
        alerts.forEach(alert => {
            alert.classList.add('bounce-in');
            
            // Ajouter un effet de clignotement pour les alertes importantes
            if (alert.classList.contains('alert-danger') || alert.classList.contains('alert-warning')) {
                alert.classList.add('notification-blink');
                
                // Arrêter le clignotement après 3 secondes
                setTimeout(() => {
                    alert.classList.remove('notification-blink');
                }, 3000);
            }
        });
    }

    // ================================================
    // EFFET PARALLAXE POUR LE HERO
    // ================================================
    function setupParallax() {
        const heroSection = document.querySelector('.hero-section');
        if (!heroSection) return;

        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }

    // ================================================
    // AMÉLIORATION DES BOUTONS AVEC ONDULATION
    // ================================================
    function setupButtonRipple() {
        const buttons = document.querySelectorAll('.btn');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    // ================================================
    // NAVBAR TRANSPARENTE AU SCROLL
    // ================================================
    function setupNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                navbar.style.background = 'rgba(10, 10, 10, 0.98)';
                navbar.style.backdropFilter = 'blur(25px)';
            } else {
                navbar.style.background = 'rgba(10, 10, 10, 0.95)';
                navbar.style.backdropFilter = 'blur(20px)';
            }
        });
    }

    // ================================================
    // ANIMATION DES STATISTIQUES
    // ================================================
    function setupCounterAnimation() {
        const counters = document.querySelectorAll('[data-count]');
        
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.getAttribute('data-count'));
                    const duration = 2000; // 2 secondes
                    const step = target / (duration / 16); // 60 FPS
                    let current = 0;
                    
                    const timer = setInterval(() => {
                        current += step;
                        if (current >= target) {
                            current = target;
                            clearInterval(timer);
                        }
                        counter.textContent = Math.floor(current);
                    }, 16);
                    
                    counterObserver.unobserve(counter);
                }
            });
        });

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }

    // ================================================
    // GESTION DES TOOLTIPS PREMIUM
    // ================================================
    function setupPremiumTooltips() {
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        
        tooltipElements.forEach(element => {
            new bootstrap.Tooltip(element, {
                customClass: 'premium-tooltip',
                placement: 'top',
                trigger: 'hover focus'
            });
        });
    }

    // ================================================
    // EFFET DE CHARGEMENT PREMIUM
    // ================================================
    function setupLoadingEffects() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function() {
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="bi bi-arrow-clockwise animate-rotate me-2"></i>Chargement...';
                    submitBtn.disabled = true;
                    submitBtn.classList.add('animate-loading');
                }
            });
        });
    }

    // ================================================
    // GESTIONNAIRE D'IMAGES AVEC LAZY LOADING
    // ================================================
    function setupImageEffects() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.getAttribute('data-src');
                    img.classList.add('animate-fadeInUp');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ================================================
    // INITIALISATION DE TOUS LES EFFETS
    // ================================================
    function initializePremiumTheme() {
        setupScrollReveal();
        setupMouseLight();
        setupStaggeredAnimation();
        createFloatingParticles();
        setupTypingEffect();
        setupSmoothScroll();
        setupNotificationEffects();
        setupParallax();
        setupButtonRipple();
        setupNavbarScroll();
        setupCounterAnimation();
        setupPremiumTooltips();
        setupLoadingEffects();
        setupImageEffects();
        
        console.log('🌟 Thème Premium initialisé avec succès !');
    }

    // Démarrer l'initialisation
    initializePremiumTheme();
    
    // ================================================
    // CSS DYNAMIQUE POUR LES EFFETS RIPPLE
    // ================================================
    const rippleStyles = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .premium-tooltip {
            background: rgba(26, 26, 26, 0.95) !important;
            border: 1px solid rgba(220, 38, 38, 0.3) !important;
            border-radius: 8px !important;
            backdrop-filter: blur(20px);
        }
        
        .premium-tooltip .tooltip-inner {
            background: transparent !important;
            color: #ffffff !important;
            font-weight: 500;
            padding: 8px 12px;
        }
        
        .premium-tooltip .tooltip-arrow::before {
            border-top-color: rgba(26, 26, 26, 0.95) !important;
        }
    `;
    
    // Injecter les styles CSS dynamiques
    const styleSheet = document.createElement('style');
    styleSheet.textContent = rippleStyles;
    document.head.appendChild(styleSheet);
    
    // ================================================
    // GESTION DES ERREURS ET PERFORMANCE
    // ================================================
    window.addEventListener('error', function(e) {
        console.warn('Erreur dans le thème premium:', e.message);
    });
    
    // Optimisation des performances pour les appareils mobiles
    if (window.innerWidth <= 768) {
        // Désactiver certains effets sur mobile
        document.documentElement.style.setProperty('--transition-slow', '0.2s');
        document.documentElement.style.setProperty('--transition-medium', '0.15s');
    }
});
