/**
 * Daily KI-Briefing - Frontend JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Generate Briefing Buttons
    const generateBtn = document.getElementById('generateBtn');
    const generateBtnEmpty = document.getElementById('generateBtnEmpty');
    const loadingOverlay = document.getElementById('loadingOverlay');

    async function generateBriefing() {
        // Show loading
        loadingOverlay.classList.remove('hidden');

        // Disable buttons
        if (generateBtn) generateBtn.disabled = true;
        if (generateBtnEmpty) generateBtnEmpty.disabled = true;

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                // Reload page to show new briefing
                window.location.reload();
            } else {
                alert('Fehler beim Generieren des Briefings: ' + (data.error || 'Unbekannter Fehler'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Netzwerkfehler beim Generieren des Briefings');
        } finally {
            loadingOverlay.classList.add('hidden');
            if (generateBtn) generateBtn.disabled = false;
            if (generateBtnEmpty) generateBtnEmpty.disabled = false;
        }
    }

    // Attach event listeners
    if (generateBtn) {
        generateBtn.addEventListener('click', generateBriefing);
    }

    if (generateBtnEmpty) {
        generateBtnEmpty.addEventListener('click', generateBriefing);
    }

    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

    // Add animation class to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe article cards
    document.querySelectorAll('.article-card, .summary-item').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        observer.observe(card);
    });
});
