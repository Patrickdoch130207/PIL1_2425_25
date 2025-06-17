// Toggle sidebar for mobile
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('show');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebarMenu();
    initializeMobileHandlers();
    initializeTopBarHandlers();
});

// Initialize top bar interactions
function initializeTopBarHandlers() {
    // Message icon click handler
    const messageIcon = document.querySelector('.message-icon');
    if (messageIcon) {
        messageIcon.addEventListener('click', function() {
            console.log('Messages clicked');
            // Ajoutez ici la logique pour ouvrir les messages
        });
    }

    // User profile click handler
    const userProfile = document.querySelector('.user-profile');
    if (userProfile) {
        userProfile.addEventListener('click', function() {
            console.log('Profile clicked');
            // Ajoutez ici la logique pour ouvrir le menu utilisateur
        });
    }
}

// Initialize sidebar menu interactions
function initializeSidebarMenu() {
    const menuItems = document.querySelectorAll('.sidebar-menu .menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            
            
            // Remove active class from all items
            menuItems.forEach(el => el.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Close sidebar on mobile after selection
            if (window.innerWidth <= 768) {
                document.querySelector('.sidebar').classList.remove('show');
            }
        });
    });
}

// Initialize mobile-specific handlers
function initializeMobileHandlers() {
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            const sidebar = document.querySelector('.sidebar');
            const toggleBtn = document.querySelector('[onclick="toggleSidebar()"]');
            
            if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        const sidebar = document.querySelector('.sidebar');
        
        // Remove show class if window becomes larger
        if (window.innerWidth > 768) {
            sidebar.classList.remove('show');
        }
    });
}