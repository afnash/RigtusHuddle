# LinkedIn Age Classifier Agent 🎯

A Python agent that analyzes LinkedIn post comments to identify which ones are likely from people aged 18-30, using Google Gemini AI.

## Quick Start

### 1. Set up your API key

```bash
export GEMINI_API_KEY='your_gemini_api_key'
```

Get your key from: https://makersuite.google.com/app/apikey

### 2. Run the agent

```bash
python age_classifier_agent.py
```

That's it! The agent will analyze the sample comments and generate a report.

## Usage Examples

```bash
# Use default sample file
python age_classifier_agent.py

# Analyze your own JSON file
python age_classifier_agent.py your_comments.json

# Specify custom output file
python age_classifier_agent.py input.json output.json
```

## What You Get

✅ AI-powered age group classification  
✅ Confidence scores for each comment  
✅ Keyword detection (slang, emojis, etc.)  
✅ Detailed reasoning for classifications  
✅ JSON report with all analysis data  

## Files Included

- `age_classifier_agent.py` - Main agent script
- `linkedin_comments_sample.json` - Sample data to test with
- `AGENT_SETUP_DOCUMENTATION.md` - Complete setup guide
- `README_AGE_CLASSIFIER.md` - This file

## Sample Input Format

```json
{
  "comments": [
    {
      "comment_id": "c001",
      "author": "John Doe",
      "text": "Yooo this is fire! 🔥"
    }
  ]
}
```

## Sample Output

```
Total Comments Analyzed: 10
Comments from 18-30 Age Group: 5
Percentage: 50.0%

1. Comment ID: c001
   Author: Alex Johnson
   Text: "Yooo this is fire! 🔥"
   Confidence: 0.95
   Keywords: yooo, fire, 🔥
   Reasoning: Uses casual slang and emojis typical of young adults
```

## Need Help?

📖 Read the full documentation: `AGENT_SETUP_DOCUMENTATION.md`

## How It Works

1. **Keyword Detection** - Identifies youth slang, emojis, and patterns
2. **AI Analysis** - Gemini analyzes language style and context
3. **Scoring** - Combines both methods for accurate classification
4. **Reporting** - Generates detailed insights

Happy analyzing! 🚀

