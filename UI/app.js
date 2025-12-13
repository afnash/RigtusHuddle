/**
 * AdSage AI - Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- Index Page Logic ---
    const urlInput = document.getElementById('urlInput');
    const analyzeBtn = document.getElementById('analyzeBtn');

    // Navigation Elements
    const selectionSection = document.getElementById('selectionSection');
    const postUploadSection = document.getElementById('postUploadSection');
    const preUploadSection = document.getElementById('preUploadSection');
    const btnPreUpload = document.getElementById('btnPreUpload');
    const btnPostUpload = document.getElementById('btnPostUpload');

    // Pre-Upload Form Elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    const contentInput = document.getElementById('contentInput');
    const platformSelect = document.getElementById('platformSelect');
    const targetSelect = document.getElementById('targetSelect');
    const predictBtn = document.getElementById('predictBtn');


    // 1. Navigation Logic
    if (selectionSection) {
        btnPreUpload.addEventListener('click', () => {
            selectionSection.classList.add('hidden');
            preUploadSection.classList.remove('hidden');
        });

        btnPostUpload.addEventListener('click', () => {
            selectionSection.classList.add('hidden');
            postUploadSection.classList.remove('hidden');
        });

        document.querySelectorAll('.back-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                postUploadSection.classList.add('hidden');
                preUploadSection.classList.add('hidden');
                selectionSection.classList.remove('hidden');
            });
        });
    }

    // 2. Post-Upload Analysis Logic
    if (urlInput && analyzeBtn) {
        const handleAnalyze = () => {
            const url = urlInput.value.trim();
            if (!url) {
                shakeInput(urlInput);
                return;
            }
            localStorage.setItem('adsage_mode', 'post');
            localStorage.setItem('adsage_url', url);
            window.location.href = 'dashboard.html';
        };

        analyzeBtn.addEventListener('click', handleAnalyze);
        urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleAnalyze();
        });
    }

    // 3. Pre-Upload Analysis Logic
    if (dropZone && fileInput) {
        // Drag & Drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });

        dropZone.addEventListener('drop', handleDrop, false);
        dropZone.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }

        function handleFiles(files) {
            if (files.length > 0) {
                const file = files[0];
                if (!file.type.startsWith('image/')) {
                    alert('Please upload an image file.');
                    return;
                }
                previewFile(file);
            }
        }

        function previewFile(file) {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = function () {
                const img = document.createElement('img');
                img.src = reader.result;
                filePreview.innerHTML = '';
                filePreview.appendChild(img);
                filePreview.classList.remove('hidden');

                // Store base64 briefly in memory/element (or we use the fileInput)
                dropZone.dataset.base64 = reader.result;
            }
        }

        // Predict Button Action
        if (predictBtn) {
            predictBtn.addEventListener('click', () => {
                const text = contentInput.value.trim();
                const platform = platformSelect.value;
                const target = targetSelect.value;
                const base64Image = dropZone.dataset.base64;

                if (!base64Image) {
                    alert("Please upload an image first.");
                    return;
                }
                if (!text) {
                    shakeInput(contentInput);
                    return;
                }

                // We prepare the data to be analyzed directly
                // Store data in localStorage to run analysis on Dashboard page (similar flow)
                // OR run it here. Running here allows us to fail fast. 
                // But to keep UX consistent (loader on dashboard), let's pass data.

                localStorage.setItem('adsage_mode', 'pre');
                localStorage.setItem('adsage_image', base64Image); // Warning: Storage limit
                localStorage.setItem('adsage_text', text);
                localStorage.setItem('adsage_platform', platform);
                localStorage.setItem('adsage_target', target);

                window.location.href = 'dashboard.html';
            });
        }
    }

    function shakeInput(element) {
        element.style.borderColor = 'var(--accent-pink)';
        element.style.boxShadow = '0 0 15px rgba(255, 0, 85, 0.3)';
        setTimeout(() => {
            element.style.borderColor = 'var(--glass-border)';
            element.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.1)';
        }, 1000);
    }


    // --- Dashboard Page Logic ---
    const loader = document.getElementById('loader');
    const dashboardGrid = document.getElementById('dashboardResults');

    if (loader && dashboardGrid) {
        // Check Mode
        const mode = localStorage.getItem('adsage_mode') || 'post';

        // Prepare Request
        let fetchUrl = 'http://127.0.0.1:5000/analyze';
        let payload = {};

        if (mode === 'post') {
            const storedUrl = localStorage.getItem('adsage_url');
            console.log("Analyzing Post URL:", storedUrl);
            payload = { mode: 'post', url: storedUrl || "demo" };
        } else {
            console.log("Analyzing Pre-Upload");
            payload = {
                mode: 'pre',
                image: localStorage.getItem('adsage_image'),
                text: localStorage.getItem('adsage_text'),
                platform: localStorage.getItem('adsage_platform'),
                target: localStorage.getItem('adsage_target')
            };
        }

        // Call the Backend API
        fetch(fetchUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Analysis failed ' + response.statusText);
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
                        renderDashboard(data.data);
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

                // Mock Error Handling specifically for Large Payload / Network issues
                // If local storage was too full, we might have issues earlier.

                loader.innerHTML = `<div style="color:red; text-align:center;">
                    <i class="fa-solid fa-triangle-exclamation" style="font-size: 2rem; margin-bottom: 1rem;"></i><br>
                    Analysis Error: ${error.message}<br>
                    <span style="font-size: 0.8rem; color: #888;">Note: Large images might fail in this demo configuration.</span><br><br>
                    <a href="index.html" style="color:white; text-decoration: underline;">Try Again</a>
                </div>`;
            });
    }

    function renderDashboard(data) {
        // Parse Strategy JSON
        let strategyData = null;
        try {
            // Clean up potential markdown code blocks
            const rawStrategy = (data.strategy || "{}").replace(/```json/g, '').replace(/```/g, '').trim();
            strategyData = JSON.parse(rawStrategy);
        } catch (e) {
            console.warn("Could not parse strategy JSON:", e);
            strategyData = { final_verdict: data.strategy }; // Fallback
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
                    strategyData.shared_positives.map(p => `<i class="fa-solid fa-check" style="color:var(--primary-neon); margin-right:5px;"></i> ${p}`).join('<br>'); // Fixed newline
            } else {
                summaryEl.innerHTML = data.summary || "Analysis complete.";
            }
        }

        // 4. Render Dynamic Tone Analysis
        const toneContainer = document.getElementById('toneContainer');
        if (toneContainer) {
            const tone = strategyData.tone_analysis || { label: "Unknown", score: 0 };
            toneContainer.innerHTML = `
                <div class="flex" style="justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>${tone.label}</span>
                    <span style="color: var(--primary-neon);">${tone.score}%</span>
                </div>
                <div style="width:100%; height:4px; background:rgba(255,255,255,0.1); border-radius:2px;">
                    <div style="width:${tone.score}%; height:100%; background:var(--primary-neon); border-radius:2px;"></div>
                </div>
            `;
        }

        // 5. Render Engagement Metrics
        const engScore = document.getElementById('engagementScore');
        const engLabel = document.getElementById('engagementLabel');
        const virScore = document.getElementById('viralityScore');

        if (engScore && strategyData.engagement_metrics) {
            engScore.innerText = strategyData.engagement_metrics.score || "N/A";
            engLabel.innerText = strategyData.engagement_metrics.explanation || "Based on visual appeal";
            virScore.innerHTML = `${strategyData.engagement_metrics.virality || "Medium"} <span class="virality-badge">Predicted</span>`;
        }

        // 6. Render Strategy Column (Hashtags vs Pros/Cons)
        const stratTitle = document.getElementById('strategyTitle');
        const stratContent = document.getElementById('strategyContent');
        const mode = localStorage.getItem('adsage_mode');

        if (stratContent) {
            if (mode === 'pre' && strategyData.pros_cons) {
                // Render Pros & Cons
                stratTitle.innerHTML = '<i class="fa-solid fa-scale-balanced"></i> Pros & Cons';
                stratContent.innerHTML = `
                    <div style="margin-bottom: 1rem;">
                        <strong style="color: var(--primary-neon);"><i class="fa-solid fa-thumbs-up"></i> Pros</strong>
                        <ul style="list-style: none; margin-top: 0.5rem; font-size: 0.85rem; color: #ccc;">
                            ${(strategyData.pros_cons.pros || []).map(p => `<li style="margin-bottom:4px;">+ ${p}</li>`).join('')}
                        </ul>
                    </div>
                    <div>
                        <strong style="color: var(--accent-pink);"><i class="fa-solid fa-thumbs-down"></i> Cons</strong>
                         <ul style="list-style: none; margin-top: 0.5rem; font-size: 0.85rem; color: #ccc;">
                            ${(strategyData.pros_cons.cons || []).map(c => `<li style="margin-bottom:4px;">- ${c}</li>`).join('')}
                        </ul>
                    </div>
                `;
            } else if (strategyData.hashtag_strategy) {
                // Render Hashtags
                stratTitle.innerHTML = '<i class="fa-solid fa-hashtag"></i> Hashtag Strategy';
                stratContent.innerHTML = `
                    <div class="tags-container">
                        ${(strategyData.hashtag_strategy.trending || []).map(t => `<div class="tag hot">${t}</div>`).join('')}
                        ${(strategyData.hashtag_strategy.niche || []).map(t => `<div class="tag">${t}</div>`).join('')}
                    </div>
                    <p style="font-size: 0.8rem; color: #888; margin-top: 1rem;">
                        <i class="fa-solid fa-info-circle"></i> ${strategyData.hashtag_strategy.insight || "AI suggested tags."}
                    </p>
                `;
            }
        }

        // 7. Setup Apply Suggestions Button
        const btnApply = document.getElementById('btnApplySuggestions');
        if (btnApply) {
            // Remove old listeners to prevent duplicates if re-rendered
            const newBtn = btnApply.cloneNode(true);
            btnApply.parentNode.replaceChild(newBtn, btnApply);

            newBtn.addEventListener('click', () => {
                const resultsArea = document.getElementById('appliedResults');
                const contentOut = document.getElementById('newContentOutput');
                const imageOut = document.getElementById('newImagePrompt');

                newBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Applying...';
                newBtn.disabled = true;

                const suggestionsText = strategyData.strategic_suggestions.map(s => s.description).join('\n');

                fetch('http://127.0.0.1:5000/apply-suggestions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image: localStorage.getItem('adsage_image'),
                        content: localStorage.getItem('adsage_text') || localStorage.getItem('adsage_url'),
                        suggestions: suggestionsText
                    })
                })
                    .then(res => res.json())
                    .then(resData => {
                        newBtn.innerHTML = 'Apply Suggestions <i class="fa-solid fa-wand-sparkles"></i>';
                        newBtn.disabled = false;

                        if (resData.success) {
                            const parsed = JSON.parse(resData.data);
                            resultsArea.classList.remove('hidden');
                            contentOut.innerText = parsed.new_content;
                            imageOut.innerText = parsed.new_image_prompt;

                            // Scroll to results
                            resultsArea.scrollIntoView({ behavior: 'smooth' });
                        } else {
                            alert("Error: " + resData.error);
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        newBtn.innerHTML = 'Error. Try Again';
                        newBtn.disabled = false;
                    });
            });
        }
    }

    // --- Helper Functions ---

    function animateBars() {
        const barYouth = document.getElementById('bar-youth');
        const barAdult = document.getElementById('bar-adult');
        const barSenior = document.getElementById('bar-senior');

        if (barYouth && barAdult && barSenior) {
            setTimeout(() => {
                barYouth.style.width = '65%';
                barAdult.style.width = '30%';
                barSenior.style.width = '5%';
            }, 300);
        }
    }
});
