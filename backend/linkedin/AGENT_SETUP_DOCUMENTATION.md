# LinkedIn Comments Age Classifier Agent - Setup Documentation

## Overview

This agent analyzes LinkedIn post comments and identifies which comments are likely from people in the 18-30 age group using Google Gemini AI and keyword analysis.

## Features

- **AI-Powered Analysis**: Uses Google Gemini API for intelligent age group classification
- **Keyword Detection**: Identifies young adult language patterns, slang, and expressions
- **Confidence Scoring**: Provides confidence scores for each classification
- **Detailed Reports**: Generates both console and JSON reports with analysis reasoning
- **Flexible Input**: Accepts JSON files with various comment structures

---

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Internet connection for API calls

---

## Setup Instructions

### Step 1: Install Dependencies

The required dependency `google-generativeai` is already in your `requirements.txt`. If you need to install it separately:

```bash
pip install google-generativeai
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### Step 2: Get Google Gemini API Key

1. **Visit Google AI Studio**
   - Go to: https://makersuite.google.com/app/apikey
   - Or: https://aistudio.google.com/

2. **Sign in with your Google Account**
   - Use any Google account (Gmail, Workspace, etc.)

3. **Create API Key**
   - Click on "Get API Key" or "Create API Key"
   - Select "Create API key in new project" or choose an existing project
   - Copy the generated API key (it will look like: `AIzaSyC...`)

4. **Important Security Notes**
   - ⚠️ Keep your API key secret - never commit it to version control
   - ⚠️ Don't share your API key publicly
   - ⚠️ Use environment variables or `.env` files (not tracked by git)

### Step 3: Configure API Key

**Option A: Using Environment Variable (Recommended)**

Linux/Mac:
```bash
export GEMINI_API_KEY='your_actual_api_key_here'
```

Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
```

Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
```

**Option B: Using .env File (Recommended for Development)**

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` file:
```bash
GEMINI_API_KEY=AIzaSyC_your_actual_key_here
```

3. Load environment variables (if using python-dotenv):
```python
from dotenv import load_dotenv
load_dotenv()
```

**Option C: Add to your shell profile (Persistent)**

Add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:
```bash
export GEMINI_API_KEY='your_actual_api_key_here'
```

Then reload:
```bash
source ~/.bashrc
```

---

## Usage

### Basic Usage

Run with the sample data file:

```bash
python age_classifier_agent.py
```

This will:
- Load `linkedin_comments_sample.json`
- Analyze all comments
- Display results in console
- Save detailed report to `age_classification_report.json`

### Custom Input File

```bash
python age_classifier_agent.py your_comments.json
```

### Custom Input and Output Files

```bash
python age_classifier_agent.py input_comments.json output_report.json
```

---

## Input JSON Format

The agent accepts JSON files in two formats:

**Format 1: Comments object with metadata**
```json
{
  "post_id": "linkedin_post_12345",
  "post_title": "Post title here",
  "post_date": "2025-12-10",
  "comments": [
    {
      "comment_id": "c001",
      "author": "John Doe",
      "text": "This is a comment",
      "timestamp": "2025-12-10T10:30:00Z"
    }
  ]
}
```

**Format 2: Direct list of comments**
```json
[
  {
    "comment_id": "c001",
    "author": "John Doe",
    "text": "This is a comment",
    "timestamp": "2025-12-10T10:30:00Z"
  }
]
```

**Required Fields:**
- `text`: The comment content (required)
- `comment_id`: Unique identifier (optional, defaults to "unknown")
- `author`: Comment author name (optional, defaults to "Unknown")

---

## Output

### Console Output

The agent displays:
- Progress indicator for each comment
- Total comments analyzed
- Number and percentage of 18-30 age group comments
- Detailed breakdown for each classified comment including:
  - Comment ID and author
  - Original text
  - Confidence score (0.0 - 1.0)
  - Keywords identified
  - AI reasoning

### JSON Report

Saved to specified output file (default: `age_classification_report.json`):

```json
{
  "analysis_timestamp": "2025-12-12T10:30:00.000000",
  "total_comments": 10,
  "young_adult_comments_count": 5,
  "percentage": 50.0,
  "young_adult_comments": [...],
  "all_analyses": [...]
}
```

---

## How the Agent Works

### 1. Keyword Detection
The agent maintains a comprehensive list of keywords and patterns associated with 18-30 age group:

- **Slang**: "lit", "fire", "bussin", "no cap", "fam", etc.
- **Education**: "college", "student", "graduated", "intern"
- **Generation markers**: "Gen Z", "millennial", "zoomer"
- **Digital native language**: "tiktok", "insta", "meme", "content creator"
- **Common emojis**: 🔥, 💯, ✨, etc.

### 2. AI Analysis
Uses Google Gemini to analyze:
- Language style (casual vs. formal)
- Vocabulary and expressions
- Career stage indicators
- Communication patterns
- Use of emojis and internet slang
- Life stage references

### 3. Combined Scoring
- Merges keyword detection with AI analysis
- Provides confidence scores
- Generates reasoning for each classification

---

## Customization

### Modify Keywords

Edit the `young_adult_keywords` list in `age_classifier_agent.py`:

```python
self.young_adult_keywords = [
    "your", "custom", "keywords", "here"
]
```

### Change AI Model

Use a different Gemini model:

```python
agent = LinkedInAgeClassifierAgent(
    api_key=api_key,
    model_name="gemini-1.5-pro"  # More powerful but slower
)
```

Available models:
- `gemini-1.5-flash` (default) - Fast and efficient
- `gemini-1.5-pro` - More capable, higher quality
- `gemini-1.0-pro` - Original model

### Adjust Analysis Prompt

Modify the `analyze_comment_with_gemini()` method to customize the AI analysis criteria.

---

## API Rate Limits and Pricing

### Gemini API Free Tier
- 15 requests per minute (RPM)
- 1 million tokens per minute (TPM)
- 1,500 requests per day (RPD)

### Pricing (as of Dec 2024)
- **Gemini 1.5 Flash**: Free up to quota limits
- **Gemini 1.5 Pro**: Pay-as-you-go after free tier

For current pricing: https://ai.google.dev/pricing

### Rate Limiting Handling

If you hit rate limits, add delays between requests:

```python
import time

for comment in comments:
    analysis = self.analyze_comment(comment)
    time.sleep(1)  # 1 second delay between requests
```

---

## Troubleshooting

### Error: "GEMINI_API_KEY environment variable not set"
- Make sure you've set the environment variable correctly
- Check spelling: `GEMINI_API_KEY` (case-sensitive)
- Try setting it in the current terminal session

### Error: "Invalid API key"
- Verify your API key is correct
- Ensure no extra spaces or quotes
- Try regenerating the key in Google AI Studio

### Error: "429 Too Many Requests"
- You've hit the rate limit
- Wait a few minutes before retrying
- Add delays between requests

### Error: "Invalid JSON format"
- Check your input JSON file is properly formatted
- Ensure it has either a "comments" key or is a direct list
- Validate JSON at: https://jsonlint.com/

### Poor Classification Results
- The AI may need more context - try providing longer comments
- Some comments may be ambiguous
- Consider adjusting the keyword list for your specific use case

---

## Security Best Practices

1. **Never hardcode API keys in your code**
2. **Add `.env` to `.gitignore`**
3. **Rotate API keys periodically**
4. **Use environment-specific keys** (dev, staging, production)
5. **Monitor API usage** in Google AI Studio
6. **Set up billing alerts** if using paid tier

---

## Example Workflow

1. **Prepare your data**:
   ```bash
   # Your JSON file with LinkedIn comments
   vi my_linkedin_comments.json
   ```

2. **Set API key**:
   ```bash
   export GEMINI_API_KEY='your_key_here'
   ```

3. **Run analysis**:
   ```bash
   python age_classifier_agent.py my_linkedin_comments.json my_report.json
   ```

4. **Review results**:
   ```bash
   cat my_report.json | python -m json.tool
   ```

---

## Sample Output

```
================================================================================
LINKEDIN COMMENTS AGE CLASSIFIER AGENT
================================================================================

Input file: linkedin_comments_sample.json
Output file: age_classification_report.json

Analyzing 10 comments...
--------------------------------------------------------------------------------
Processing comment 1/10... ✓
Processing comment 2/10... ✓
...

================================================================================
ANALYSIS REPORT - LINKEDIN COMMENTS AGE CLASSIFICATION
================================================================================

Total Comments Analyzed: 10
Comments from 18-30 Age Group: 5
Percentage: 50.0%

--------------------------------------------------------------------------------
COMMENTS IDENTIFIED AS 18-30 AGE GROUP:
--------------------------------------------------------------------------------

1. Comment ID: c001
   Author: Alex Johnson
   Text: "Yooo this is fire! 🔥 Can't wait to try it out. Congrats fam!"
   Confidence: 0.95
   Keywords: yooo, fire, fam, 🔥
   Reasoning: Uses casual slang typical of young adults...
```

---

## Support and Resources

- **Google Gemini Documentation**: https://ai.google.dev/docs
- **API Reference**: https://ai.google.dev/api/python
- **Get API Key**: https://makersuite.google.com/app/apikey
- **Pricing Info**: https://ai.google.dev/pricing

---

## License

This agent is provided as-is for educational and commercial use.

---

## Version History

- **v1.0.0** (Dec 2025) - Initial release
  - Google Gemini integration
  - Keyword-based detection
  - JSON report generation
  - Confidence scoring

---

## Contributing

Feel free to modify and extend this agent for your specific needs!

**Suggested improvements**:
- Add support for other age groups
- Implement batch processing for large datasets
- Add caching to reduce API calls
- Create a web interface
- Add sentiment analysis
- Export to CSV format

