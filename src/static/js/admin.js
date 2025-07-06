// Admin Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Set active menu item based on current URL
    setActiveMenuItem();
    
    // Auto-collapse sidebar on smaller screens
    handleResponsiveSidebar();
    
    // Initialize dashboard features
    initializeDashboard();
    
    // Initialize admin table functionality
    initializeAdminTables();
});

function setActiveMenuItem() {
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.menu-link');
    
    menuLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Special case for dashboard (admin root)
    if (currentPath === '/admin' || currentPath === '/admin/') {
        const dashboardLink = document.querySelector('a[href*="admin_dashboard"]');
        if (dashboardLink) {
            dashboardLink.classList.add('active');
        }
    }
}

function handleResponsiveSidebar() {
    const sidebar = document.getElementById('admin-sidebar');
    const body = document.body;
    
    // Auto-collapse on mobile
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('mobile-open');
        body.classList.remove('sidebar-mobile-open');
    }
    
    // Handle resize events
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            body.classList.add('sidebar-collapsed');
        } else {
            sidebar.classList.remove('mobile-open');
            body.classList.remove('sidebar-mobile-open');
        }
    });
}

function initializeDashboard() {
    // Animate stat cards on load
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease';
            
            requestAnimationFrame(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            });
        }, index * 100);
    });
    
    // Add hover effects to action cards
    const actionCards = document.querySelectorAll('.action-card');
    actionCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '';
        });
    });
}

// Utility function to format numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Function to update stat cards (for real-time updates)
function updateStatCard(selector, newValue) {
    const statNumber = document.querySelector(selector + ' .stat-number');
    if (statNumber) {
        const currentValue = parseInt(statNumber.textContent);
        animateNumber(statNumber, currentValue, newValue);
    }
}

function animateNumber(element, start, end) {
    const duration = 1000;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = formatNumber(current);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Function to show success/error messages
function showMessage(message, type = 'success') {
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    
    const messageElement = document.createElement('div');
    messageElement.className = `flash-message flash-${type}`;
    messageElement.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
        ${message}
        <button class="flash-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    flashContainer.appendChild(messageElement);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageElement.parentNode) {
            messageElement.style.opacity = '0';
            setTimeout(() => {
                messageElement.remove();
            }, 300);
        }
    }, 5000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    const adminContent = document.querySelector('.admin-content');
    adminContent.insertBefore(container, adminContent.firstChild);
    return container;
}

// Admin table functionality
function initializeAdminTables() {
    // Initialize table search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', searchTable);
    }
    
    // Initialize table filters
    const statusFilter = document.getElementById('status-filter');
    if (statusFilter) {
        statusFilter.addEventListener('change', filterTable);
    }
}

function handleAddNew(button) {
    const addUrl = button.getAttribute('data-add-url');
    if (addUrl && addUrl !== '#') {
        window.location.href = addUrl;
    } else {
        alert('Add new functionality not implemented yet');
    }
}

function refreshTable() {
    window.location.reload();
}

function filterTable() {
    const statusFilter = document.getElementById('status-filter').value.toLowerCase();
    const table = document.getElementById('dataTable');
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const statusCell = row.querySelector('.status-badge');
        
        if (!statusFilter || !statusCell) {
            row.style.display = '';
            continue;
        }
        
        const statusText = statusCell.textContent.toLowerCase();
        let shouldShow = false;
        
        if (statusFilter === 'published' && statusText.includes('published')) {
            shouldShow = true;
        } else if (statusFilter === 'unpublished' && (statusText.includes('draft') || statusText.includes('unpublished'))) {
            shouldShow = true;
        } else if (statusFilter === 'approved' && statusText.includes('approved')) {
            shouldShow = true;
        } else if (statusFilter === 'pending' && statusText.includes('pending')) {
            shouldShow = true;
        }
        
        row.style.display = shouldShow ? '' : 'none';
    }
}

function searchTable() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const table = document.getElementById('dataTable');
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let shouldShow = false;
        
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].textContent.toLowerCase().includes(searchInput)) {
                shouldShow = true;
                break;
            }
        }
        
        row.style.display = shouldShow ? '' : 'none';
    }
}

function togglePublish(button) {
    const id = button.getAttribute('data-id');
    const type = button.getAttribute('data-type');
    const isPublished = button.getAttribute('data-published') === 'true';
    
    if (confirm(`Are you sure you want to ${isPublished ? 'unpublish' : 'publish'} this item?`)) {
        // TODO: Implement AJAX call to toggle publish status
        console.log(`Toggle publish for ${type} ID: ${id}`);
        // For now, just show a success message
        alert('Action logged to console. Full implementation pending.');
    }
}

function deleteItem(button) {
    const id = button.getAttribute('data-id');
    const type = button.getAttribute('data-type');
    
    if (confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
        // TODO: Implement AJAX call to delete item
        console.log(`Delete ${type} ID: ${id}`);
        // For now, just show a success message
        alert('Action logged to console. Full implementation pending.');
    }
}

function approveItem(button) {
    const id = button.getAttribute('data-id');
    const type = button.getAttribute('data-type');
    
    if (confirm('Are you sure you want to approve this item?')) {
        // TODO: Implement AJAX call to approve item
        console.log(`Approve ${type} ID: ${id}`);
        // For now, just show a success message
        alert('Action logged to console. Full implementation pending.');
    }
}

function editItem(button) {
    const id = button.getAttribute('data-id');
    const type = button.getAttribute('data-type');
    
    // TODO: Implement edit functionality
    console.log(`Edit ${type} ID: ${id}`);
    alert('Edit functionality not implemented yet');
}

function viewItem(button) {
    const id = button.getAttribute('data-id');
    const type = button.getAttribute('data-type');
    
    // TODO: Implement view functionality
    console.log(`View ${type} ID: ${id}`);
    alert('View functionality not implemented yet');
}
