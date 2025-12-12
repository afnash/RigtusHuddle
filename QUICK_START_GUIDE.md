# 🚀 Quick Start Guide - LinkedIn Age Classifier Agent

Get up and running in 5 minutes!

---

## Step 1: Get Your Google Gemini API Key (2 minutes)

1. Visit: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIzaSy...`)

---

## Step 2: Set Your API Key (30 seconds)

**Linux/Mac:**
```bash
export GEMINI_API_KEY='paste_your_key_here'
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="paste_your_key_here"
```

**Or create a `.env` file:**
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

---

## Step 3: Activate Virtual Environment (10 seconds)

```bash
source venv/bin/activate
```

---

## Step 4: Run the Agent! (30 seconds)

**Option A: Use the helper script**
```bash
./run_agent.sh
```

**Option B: Run directly**
```bash
python age_classifier_agent.py
```

**Option C: Use your own JSON file**
```bash
python age_classifier_agent.py your_comments.json
```

---

## What Happens Next?

The agent will:
1. ✅ Load your JSON file with comments
2. ✅ Analyze each comment using AI
3. ✅ Identify keywords and patterns
4. ✅ Display results in your terminal
5. ✅ Save a detailed JSON report

---

## Example Output

```
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
   Reasoning: Uses casual slang and emojis typical of young adults...
```

---

## Your JSON File Format

Create a JSON file like this:

```json
{
  "comments": [
    {
      "comment_id": "c001",
      "author": "John Doe",
      "text": "Your comment text here"
    }
  ]
}
```

**Required fields:**
- `text` - The comment content

**Optional fields:**
- `comment_id` - Unique identifier
- `author` - Commenter's name
- `timestamp` - When the comment was posted

---

## Testing Without API Key

Want to test the basic functionality first?

```bash
python test_agent.py
```

This runs offline tests without using the API.

---

## Troubleshooting

### "GEMINI_API_KEY not set"
➜ Make sure you exported the variable in your current terminal session

### "Module not found"
➜ Activate the virtual environment: `source venv/bin/activate`

### "Invalid API key"
➜ Double-check your key at https://makersuite.google.com/app/apikey

### "Rate limit exceeded"
➜ Free tier has limits. Wait a few minutes and try again.

---

## Files You'll Get

After running the agent:

📄 **age_classification_report.json** - Full analysis with all data  
📊 **Console output** - Human-readable summary  

---

## Next Steps

1. ✅ Try with the sample data
2. ✅ Prepare your own LinkedIn comments JSON
3. ✅ Run analysis on your data
4. ✅ Review the detailed report
5. ✅ Customize keywords if needed (edit `age_classifier_agent.py`)

---

## Need More Help?

📖 **Full Documentation:** `AGENT_SETUP_DOCUMENTATION.md`  
🧪 **Test Script:** `python test_agent.py`  
📝 **Sample Data:** `linkedin_comments_sample.json`  

---

## Pro Tips

💡 **Batch Processing:** Process multiple files by running the script multiple times  
💡 **Custom Keywords:** Edit the `young_adult_keywords` list in the agent  
💡 **Different Models:** Try `gemini-1.5-pro` for better accuracy  
💡 **Save API Calls:** The agent caches nothing, so each run costs API calls  

---

## API Usage & Costs

**Free Tier Limits:**
- 15 requests per minute
- 1,500 requests per day
- Totally free for most use cases!

**For 10 comments:** ~10 API calls (~1 per comment)  
**For 100 comments:** ~100 API calls  

Monitor usage at: https://aistudio.google.com/

---

## Questions?

The agent is ready to use! Just follow the 4 steps above and you're good to go! 🎉

Happy analyzing! 🚀

