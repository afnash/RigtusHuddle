from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_core import run_analysis, run_pre_analysis
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "Backend Agent Server is up. Use POST /analyze."})

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    # Handle both GET (browser/query param) and POST (API/JSON)
    if request.method == 'GET':
        url = request.args.get('url')
        mode = 'post'
    else:
        data = request.json or {}
        mode = data.get('mode', 'post') # Default to post for backward compatibility
        url = data.get('url')
        
    print(f"Received request: Mode={mode}")

    try:
        if mode == 'post':
            # Default to "demo" (local file) if no URL provided
            if not url:
                url = "demo"
            
            # Detect platform
            platform = "linkedin"
            if url and "instagram" in url.lower():
                platform = "instagram"
            
            # Post-Launch Analysis (Existing)
            results = run_analysis("linkedin_comments.json", platform=platform)
            
            summary_text = "Analysis of comments for the campaign."

        elif mode == 'pre':
            # Pre-Launch Analysis (New)
            image_b64 = data.get('image')
            text_content = data.get('text')
            platform = data.get('platform', 'linkedin')
            target_group = data.get('target', 'all')
            
            if not image_b64 or not text_content:
                return jsonify({"success": False, "error": "Missing image or text for pre-analysis"}), 400

            results = run_pre_analysis(
                image_b64=image_b64, 
                text_content=text_content, 
                platform=platform, 
                target_group=target_group
            )
            summary_text = f"Predictive analysis for {platform} targeting {target_group}."

        else:
            return jsonify({"success": False, "error": "Invalid mode"}), 400

        # Common Response Handling
        if results.get("error"):
            return jsonify({"success": False, "error": results["error"]}), 500
            
        return jsonify({
            "success": True,
            "data": {
                "summary": summary_text,
                "strategy": results["strategy"] 
                # Note: strategy acts as the main JSON object for the dashboard
            }
        })
        
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
