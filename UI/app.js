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
        fetch('http://127.0.0.1:5000/analyze', {
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
                        // Parse Strategy JSON
                        let strategyData = null;
                        try {
                            // Clean up potential markdown code blocks if present (e.g. ```json ... ```)
                            const rawStrategy = (data.data.strategy || "{}").replace(/```json/g, '').replace(/```/g, '').trim();
                            strategyData = JSON.parse(rawStrategy);
                        } catch (e) {
                            console.warn("Could not parse strategy JSON:", e);
                            strategyData = { final_verdict: data.data.strategy }; // Fallback
                        }

                        // 1. Render Final Verdict
                        const verdictEl = document.getElementById('verdictText');
                        if (verdictEl && strategyData.final_verdict) {
                            verdictEl.innerHTML = strategyData.final_verdict;
                        }

                        // 2. Render Suggestions (Improvements)
                        const improvementList = document.getElementById('improvementList');
                        if (improvementList && strategyData.strategic_suggestions && Array.isArray(strategyData.strategic_suggestions)) {
                            improvementList.innerHTML = strategyData.strategic_suggestions.map(item => {
                                // Determine icon based on priority or random
                                let icon = 'fa-lightbulb';
                                if (item.priority === 'High') icon = 'fa-star';
                                else if (item.priority === 'Medium') icon = 'fa-arrow-trend-up';

                                return `
                                <li>
                                    <i class="fa-solid ${icon}"></i>
                                    <div>
                                        <strong>${item.title}</strong> <span style="font-size:0.7em; text-transform:uppercase; opacity:0.7; border:1px solid #555; padding:2px 5px; border-radius:4px; margin-left:5px;">${item.priority}</span><br>
                                        <span style="color: #bbb;">${item.description}</span>
                                    </div>
                                </li>
                            `}).join('');
                        }

                        // 3. Render Summary (Shared Positives)
                        const summaryEl = document.getElementById('summaryText');
                        if (summaryEl) {
                            if (strategyData.shared_positives && strategyData.shared_positives.length > 0) {
                                summaryEl.innerHTML = "<strong>Key Strengths Analyzed:</strong><br><br>" +
                                    strategyData.shared_positives.map(p => `<i class="fa-solid fa-check" style="color:var(--primary-neon); margin-right:5px;"></i> ${p}`).join('<br>');
                            } else {
                                summaryEl.innerText = "Analysis complete. Review the strategy below for details.";
                            }
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
