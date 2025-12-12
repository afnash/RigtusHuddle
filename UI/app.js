/**
 * AdSage AI - Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- Index Page Logic ---
    const urlInput = document.getElementById('urlInput');
    const analyzeBtn = document.getElementById('analyzeBtn');

    if (urlInput && analyzeBtn) {

        // Function to handle navigation
        const handleAnalyze = () => {
            const url = urlInput.value.trim();
            if (!url) {
                // Shake / Error effect
                urlInput.style.borderColor = 'var(--accent-pink)';
                urlInput.style.boxShadow = '0 0 15px rgba(255, 0, 85, 0.3)';
                setTimeout(() => {
                    urlInput.style.borderColor = 'var(--glass-border)';
                    urlInput.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.1)';
                }, 1000);
                return;
            }

            // Save URL to localStorage to pass to next page
            localStorage.setItem('adsage_url', url);

            // Navigate to Dashboard
            window.location.href = 'dashboard.html';
        };

        // Event Listeners
        analyzeBtn.addEventListener('click', handleAnalyze);

        urlInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                handleAnalyze();
            }
        });
    }


    // --- Dashboard Page Logic ---
    const loader = document.getElementById('loader');
    const dashboardGrid = document.getElementById('dashboardResults');

    if (loader && dashboardGrid) {
        // Retrieve Data (Simulated)
        const storedUrl = localStorage.getItem('adsage_url');
        console.log("Analyzing:", storedUrl); // In a real app, we'd fetch API data here

        // Simulate API delay
        setTimeout(() => {
            // Hide Loader
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.classList.add('hidden');

                // Show Dashboard
                dashboardGrid.classList.remove('hidden');

                // Trigger Entrance Animation
                // Small delay to ensure display:grid applies before opacity transition
                requestAnimationFrame(() => {
                    dashboardGrid.classList.add('visible');
                    animateBars();
                });

            }, 500); // fade out time
        }, 2000); // 2 seconds fake processing
    }

    // --- Helper Functions ---

    function animateBars() {
        const barYouth = document.getElementById('bar-youth');
        const barAdult = document.getElementById('bar-adult');
        const barSenior = document.getElementById('bar-senior');

        if (barYouth && barAdult && barSenior) {
            // Slight delay for bar animation to look cool
            setTimeout(() => {
                barYouth.style.width = '65%';
                barAdult.style.width = '30%';
                barSenior.style.width = '5%';
            }, 300);
        }
    }
});
