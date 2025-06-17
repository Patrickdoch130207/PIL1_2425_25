
        // Génération des particules animées
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 50;

            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                // Taille aléatoire
                const size = Math.random() * 4 + 2;
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                
                // Position aléatoire
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                
                // Délai d'animation aléatoire
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
                
                particlesContainer.appendChild(particle);
            }
        }

        // Effet de parallaxe au scroll
        function parallaxEffect() {
            const card = document.querySelector('.welcome-card');
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            
            if (card) {
                card.style.transform = `translateY(${rate}px)`;
            }
        }

        // Animation du bouton au survol
        function initButtonAnimations() {
            const button = document.querySelector('.cta-button');
            
            if (button) {
                button.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-3px) scale(1.05)';
                });
                
                button.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0) scale(1)';
                });
            }
        }

        // Animation d'entrée séquentielle
        function initSequentialAnimations() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.animationPlayState = 'running';
                    }
                });
            });

            const animatedElements = document.querySelectorAll('[class*="animation"]');
            animatedElements.forEach(el => observer.observe(el));
        }

        // Effet de typing pour le titre
        function typeWriter(element, text, speed = 100) {
            let i = 0;
            element.innerHTML = '';
            
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            
            setTimeout(type, 1000);
        }

        // Initialisation au chargement de la page
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
            initButtonAnimations();
            initSequentialAnimations();
            
            // Effet de typing sur le titre (optionnel)
            // const title = document.querySelector('.main-title');
            // if (title) {
            //     const originalText = title.textContent;
            //     typeWriter(title, originalText, 100);
            // }
            
            // Ajout de l'effet parallaxe
            window.addEventListener('scroll', parallaxEffect);
            
            // Animation au clic sur les fonctionnalités
            const features = document.querySelectorAll('.feature');
            features.forEach(feature => {
                feature.addEventListener('click', function() {
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                    }, 150);
                });
            });
        });

        // Gestion du redimensionnement de la fenêtre
        window.addEventListener('resize', function() {
            // Réajustement responsive si nécessaire
            const card = document.querySelector('.welcome-card');
            if (window.innerWidth < 576 && card) {
                card.style.padding = '1.5rem 1rem';
            }
        });
    