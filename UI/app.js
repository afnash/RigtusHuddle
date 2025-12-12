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
        console.log("Analyzing:", storedUrl);

        // Call the Backend API
        fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: storedUrl || "demo" })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                // Hide Loader
                loader.style.opacity = '0';
                setTimeout(() => {
                    loader.classList.add('hidden');

                    // Show Dashboard
                    dashboardGrid.classList.remove('hidden');

                    // Update Results
                    if (data.success && data.data) {
                        const strategy = data.data.strategy || "No strategy generated.";
                        const summary = "Analysis complete. See full strategy below which combines insights from both Youth and Adult demographics.";

                        // Simple text format
                        const summaryEl = document.getElementById('summaryText');
                        if (summaryEl) summaryEl.innerText = summary;

                        const verdictEl = document.getElementById('verdictText');
                        if (verdictEl) {
                            // The strategy text is markdown, but we'll specific simplistic display
                            // Replacing newlines with <br> for basic formatting
                            verdictEl.innerHTML = strategy.replace(/\n/g, '<br>');
                        }
                    }

                    // Trigger Entrance Animation
                    requestAnimationFrame(() => {
                        dashboardGrid.classList.add('visible');
                        animateBars();
                    });

                }, 500); // fade out time
            })
            .catch(error => {
                console.error('Error:', error);
                loader.innerHTML = `<div style="color:red; text-align:center;">Error: ${error.message}<br><br><a href="index.html" style="color:white">Try Again</a></div>`;
            });
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
