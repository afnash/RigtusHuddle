from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_core import run_analysis
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "Backend Agent Server is up and running. Use POST /analyze to analyze data."})

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    # Handle both GET (browser/query param) and POST (API/JSON)
    if request.method == 'GET':
        url = request.args.get('url')
    else:
        data = request.json or {}
        url = data.get('url')
    
    # Default to "demo" (local file) if no URL provided
    if not url:
        url = "demo"
    
    print(f"Received request to analyze: {url} (Method: {request.method})")
    
    # In a real production app, we would scrape the URL (LinkedIn/Instagram) here.
    # For this Hackathon implementation, we use the local 'linkedin_comments.json'
    # as our data source to demonstrate the Multi-Agent capabilities.
    
    try:
        # Run the agent logic
        # We assume linkedin_comments.json is in the same directory
        # In the future, 'url' could determine which file or scraper to use.
        results = run_analysis("linkedin_comments.json")
        
        if results.get("error"):
            return jsonify({"success": False, "error": results["error"]}), 500
            
        return jsonify({
            "success": True,
            "data": {
                "summary": "Analysis of LinkedIn comments for the campaign.",
                "youth_insight": results["youth_analysis"],
                "adult_insight": results["adult_analysis"],
                "strategy": results["strategy"]
            }
        })
        
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
