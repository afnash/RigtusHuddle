from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_core import run_analysis
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')
    
    print(f"Received request to analyze: {url}")
    
    # In a real production app, we would scrape the URL (LinkedIn/Instagram) here.
    # For this Hackathon implementation, we use the local 'linkedin_comments.json'
    # as our data source to demonstrate the Multi-Agent capabilities.
    
    try:
        # Run the agent logic
        # We assume linkedin_comments.json is in the same directory
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
