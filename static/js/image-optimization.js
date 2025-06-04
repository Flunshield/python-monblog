/**
 * OPTIMISATION DES IMAGES - BLOG DJANGO
 * Script pour améliorer le chargement et l'affichage des images
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ================================================
    // OPTIMISATION DU CHARGEMENT DES IMAGES
    // ================================================
    function setupImageOptimization() {
        console.log('🖼️ Initialisation de l\'optimisation des images...');
        
        // Gestion du lazy loading pour les navigateurs qui ne le supportent pas nativement
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        
        if ('loading' in HTMLImageElement.prototype) {
            // Le navigateur supporte le lazy loading natif
            lazyImages.forEach(img => {
                img.addEventListener('load', function() {
                    this.classList.add('loaded');
                    console.log('✅ Image chargée:', this.src);
                });
                
                img.addEventListener('error', function() {
                    console.warn('❌ Erreur de chargement pour:', this.src);
                    handleImageError(this);
                });
            });
        } else {
            // Fallback avec Intersection Observer pour les anciens navigateurs
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                        console.log('✅ Image lazy-loaded:', img.src);
                    }
                });
            });
            
            lazyImages.forEach(img => imageObserver.observe(img));
        }

        // Gestion des erreurs d'images
        const allImages = document.querySelectorAll('img');
        allImages.forEach(img => {
            img.addEventListener('error', function() {
                handleImageError(this);
            });
        });

        // Animation de hover pour les images dans les cartes
        setupImageHoverEffects();
        
        console.log(`✅ ${allImages.length} images optimisées`);
    }

    // ================================================
    // GESTION DES ERREURS D'IMAGES
    // ================================================
    function handleImageError(img) {
        console.warn('❌ Erreur de chargement pour l\'image:', img.src);
        
        // Cache l'image défaillante
        img.style.display = 'none';
        
        // Crée un placeholder        const fallback = document.createElement('div');
        fallback.className = 'image-placeholder bg-secondary d-flex align-items-center justify-content-center';
        fallback.style.height = img.style.height || '200px';
        fallback.style.borderRadius = 'var(--border-radius, 8px)';
        fallback.innerHTML = '<i class="bi bi-image" style="font-size: 3rem;"></i>';
        
        // Insère le placeholder
        if (img.parentNode) {
            img.parentNode.insertBefore(fallback, img);
        }
    }

    // ================================================
    // EFFETS DE HOVER POUR LES IMAGES
    // ================================================
    function setupImageHoverEffects() {
        const cardImages = document.querySelectorAll('.premium-card img, .hover-card img');
        cardImages.forEach(img => {
            const card = img.closest('.premium-card, .hover-card');
            if (card) {
                card.addEventListener('mouseenter', () => {
                    img.style.transform = 'scale(1.05)';
                });
                card.addEventListener('mouseleave', () => {
                    img.style.transform = 'scale(1)';
                });
            }
        });
    }

    // ================================================
    // VALIDATION DES CHEMINS D'IMAGES
    // ================================================
    function validateImagePaths() {
        const images = document.querySelectorAll('img[src*="articles/"]');
        images.forEach(img => {
            const src = img.src;
            console.log('🔍 Vérification de l\'image:', src);
            
            // Test de l'existence de l'image
            const testImage = new Image();
            testImage.onload = function() {
                console.log('✅ Image accessible:', src);
            };
            testImage.onerror = function() {
                console.error('❌ Image inaccessible:', src);
                handleImageError(img);
            };
            testImage.src = src;
        });
    }

    // ================================================
    // INITIALISATION
    // ================================================
    setupImageOptimization();
    validateImagePaths();
    
    console.log('🌟 Optimisation des images initialisée avec succès !');
});
