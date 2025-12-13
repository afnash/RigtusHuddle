# AdSage AI 🧠

**AdSage AI** is a next-generation marketing intelligence dashboard that uses multi-persona AI agents to predict, analyze, and optimize your social media campaigns. Whether you are validating a creative before launch or analyzing live performance, AdSage provides deep strategic insights.

## ✨ Key Features

### 🚀 Pre-Launch Simulation
*   **Predictive Analysis:** Upload your creative (Image + Text) to simulate reactions from distinct demographics (**Gen-Z Youth** vs. **Corporate Professionals**).
*   **Pros & Cons:** Get an honest, unfiltered list of strengths and weaknesses before you post.
*   **Visual Critique:** The AI "sees" your image and critiques aesthetics, branding, and vibe.

### 📊 Post-Launch Analytics
*   **URL Intelligence:** Paste any post link (LinkedIn/Instagram) to extract context and simulate realistic audience feedback.
*   **Deep Insight:** Analyze sentiment, engagement potential, and virality velocity.
*   **Strategic Breakdown:** Understand *why* a post worked or failed with "Tone Analysis" and "Hashtag Strategy".

### ⚡ Actionable Optimization
*   **Apply Suggestions:** Don't just get advice—implement it. Click **"Apply Suggestions"** to have the AI:
    *   ✍️ **Rewrite your copy** for better engagement.
    *   🎨 **Generate new visuals** using Google's **Imagen 3** model based on strategic feedback.

## 🛠️ Tech Stack

*   **Frontend:** HTML5, CSS3 (Glassmorphism UI), Vanilla JavaScript.
*   **Backend:** Python (Flask).
*   **AI Core:** 
    *   **Google Gemini 2.5 Flash** (Reasoning & Multimodal Analysis).
    *   **Google Imagen 3** (High-fidelity Image Generation).
    *   **Agentic Workflow:** Custom multi-agent system (Youth Agent, Adult Agent, Chief Strategist).

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   A Google Cloud Project with **Gemini API** access.

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/AdSage-AI.git
    cd AdSage-AI
    ```

2.  **Backend Setup**
    Navigate to the agent directory and set up the environment:
    ```bash
    cd backend/agent
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt  # Install flask, google-generativeai, pillow, python-dotenv, requests, beautifulsoup4
    ```

3.  **Environment Variables**
    Create a `.env` file in `backend/agent/` and add your API key:
    ```bash
    GEMINI_API_KEY=your_api_key_here
    ```

4.  **Run the Server**
    ```bash
    python server.py
    # Server runs on http://127.0.0.1:5000
    ```

5.  **Launch Frontend**
    Simply open the `UI/index.html` file in your preferred web browser.

## 📂 Project Structure

```
RigtusHuddle/
├── UI/                     # Frontend Application
│   ├── index.html          # Landing & Selection Page
│   ├── dashboard.html      # Main Analytics Dashboard
│   ├── style.css           # Futuristic Styling
│   └── app.js              # Client Logic & API Integration
└── backend/
    └── agent/              # Python Agent Server
        ├── server.py       # Flask API Endpoints
        ├── agent_core.py   # Multi-Agent Logic & Gemini Integration
        └── prompts/        # System Instructions for Persona Agents
```

