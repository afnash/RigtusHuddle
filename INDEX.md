# 📖 LinkedIn Age Classifier Agent - Documentation Index

Welcome! This index will help you find the right documentation for your needs.

---

## 🚀 I Want to Get Started Quickly

**→ Read:** [`QUICK_START_GUIDE.md`](QUICK_START_GUIDE.md)

Get up and running in 5 minutes with step-by-step instructions.

---

## 📚 I Need Complete Setup Instructions

**→ Read:** [`AGENT_SETUP_DOCUMENTATION.md`](AGENT_SETUP_DOCUMENTATION.md)

Comprehensive guide covering:
- Detailed API key setup
- All configuration options
- Input/output formats
- Customization guide
- Troubleshooting
- Security best practices

---

## 🎯 I Want a Project Overview

**→ Read:** [`README_AGE_CLASSIFIER.md`](README_AGE_CLASSIFIER.md)

Quick overview of what the agent does and basic usage examples.

---

## 🔍 I Need Technical Details

**→ Read:** [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md)

Technical summary including:
- Architecture overview
- How it works (with diagrams)
- Performance metrics
- Use cases
- Integration examples

---

## 📁 Project Files Quick Reference

### Core Files
| File | Description |
|------|-------------|
| `age_classifier_agent.py` | Main agent implementation |
| `linkedin_comments_sample.json` | Sample data for testing |
| `agent_requirements.txt` | Python dependencies |

### Utility Files
| File | Description |
|------|-------------|
| `test_agent.py` | Offline functionality tests |
| `run_agent.sh` | Quick start shell script |
| `.env.example` | Environment variable template |

### Documentation Files
| File | Description |
|------|-------------|
| `QUICK_START_GUIDE.md` | 5-minute quick start |
| `AGENT_SETUP_DOCUMENTATION.md` | Complete setup guide |
| `README_AGE_CLASSIFIER.md` | Project README |
| `PROJECT_SUMMARY.md` | Technical summary |
| `INDEX.md` | This file |

---

## 🎓 Common Tasks

### First Time Setup
1. Read [`QUICK_START_GUIDE.md`](QUICK_START_GUIDE.md)
2. Get API key from https://makersuite.google.com/app/apikey
3. Run `export GEMINI_API_KEY='your_key'`
4. Run `python test_agent.py`
5. Run `python age_classifier_agent.py`

### Running the Agent
```bash
# With sample data
python age_classifier_agent.py

# With your data
python age_classifier_agent.py your_comments.json

# With custom output
python age_classifier_agent.py input.json output.json

# Using helper script
./run_agent.sh
```

### Testing
```bash
# Run offline tests
python test_agent.py

# Test with sample data
python age_classifier_agent.py linkedin_comments_sample.json
```

### Customization
- **Keywords:** Edit `young_adult_keywords` in `age_classifier_agent.py`
- **AI Model:** Change `model_name` parameter
- **Age Range:** Modify prompt in `analyze_comment_with_gemini()`
- See [`AGENT_SETUP_DOCUMENTATION.md`](AGENT_SETUP_DOCUMENTATION.md) for details

---

## 🆘 Troubleshooting

### Quick Fixes
| Problem | Solution | Details |
|---------|----------|---------|
| "GEMINI_API_KEY not set" | `export GEMINI_API_KEY='your_key'` | [Setup Guide](AGENT_SETUP_DOCUMENTATION.md#step-3-configure-api-key) |
| "Module not found" | `source venv/bin/activate` | [Setup Guide](AGENT_SETUP_DOCUMENTATION.md#step-1-install-dependencies) |
| "Invalid API key" | Verify at https://makersuite.google.com/app/apikey | [Setup Guide](AGENT_SETUP_DOCUMENTATION.md#step-2-get-google-gemini-api-key) |
| "Rate limit exceeded" | Wait a few minutes | [Setup Guide](AGENT_SETUP_DOCUMENTATION.md#api-rate-limits-and-pricing) |

### Full Troubleshooting Guide
**→ See:** [Troubleshooting Section](AGENT_SETUP_DOCUMENTATION.md#troubleshooting) in Setup Documentation

---

## 📊 Understanding the Output

### Console Output
- Real-time progress
- Summary statistics
- Detailed analysis for each comment

### JSON Report
- Complete analysis data
- Confidence scores
- Keywords identified
- AI reasoning

**→ See:** [Output Section](AGENT_SETUP_DOCUMENTATION.md#output) in Setup Documentation

---

## 🔧 Advanced Topics

### Python Integration
```python
from age_classifier_agent import LinkedInAgeClassifierAgent

agent = LinkedInAgeClassifierAgent(api_key="your_key")
analysis = agent.analyze_comment(comment_dict)
```

### Batch Processing
```bash
for file in comments_*.json; do
    python age_classifier_agent.py "$file" "report_$file"
done
```

### Custom Models
```python
agent = LinkedInAgeClassifierAgent(
    api_key=api_key,
    model_name="gemini-1.5-pro"
)
```

**→ See:** [Customization Section](AGENT_SETUP_DOCUMENTATION.md#customization) in Setup Documentation

---

## 🔐 Security & Best Practices

**→ See:** [Security Best Practices](AGENT_SETUP_DOCUMENTATION.md#security-best-practices) in Setup Documentation

Key points:
- Never commit API keys
- Use environment variables
- Rotate keys periodically
- Monitor API usage

---

## 📈 Performance & Costs

### Free Tier Limits
- 15 requests per minute
- 1,500 requests per day
- Totally free for most use cases

### Processing Speed
- ~3 seconds per comment
- 10 comments: ~30 seconds
- 100 comments: ~5 minutes

**→ See:** [API Rate Limits](AGENT_SETUP_DOCUMENTATION.md#api-rate-limits-and-pricing) in Setup Documentation

---

## 🎯 Use Cases

1. **Marketing Analysis** - Identify young adult engagement
2. **Audience Research** - Understand demographics
3. **Content Optimization** - Tailor messaging
4. **Trend Analysis** - Track language evolution
5. **Academic Research** - Study communication patterns

**→ See:** [Use Cases Section](PROJECT_SUMMARY.md#-use-cases) in Project Summary

---

## 📞 Getting Help

### Documentation
1. **Quick Start:** [`QUICK_START_GUIDE.md`](QUICK_START_GUIDE.md)
2. **Full Setup:** [`AGENT_SETUP_DOCUMENTATION.md`](AGENT_SETUP_DOCUMENTATION.md)
3. **Technical Details:** [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md)

### Testing
```bash
python test_agent.py
```

### Resources
- Google Gemini Docs: https://ai.google.dev/docs
- API Reference: https://ai.google.dev/api/python
- Get API Key: https://makersuite.google.com/app/apikey

---

## ✅ Checklist for First Run

- [ ] Read [`QUICK_START_GUIDE.md`](QUICK_START_GUIDE.md)
- [ ] Get API key from https://makersuite.google.com/app/apikey
- [ ] Set `GEMINI_API_KEY` environment variable
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Run tests: `python test_agent.py`
- [ ] Run agent: `python age_classifier_agent.py`
- [ ] Review output and JSON report
- [ ] Prepare your own data
- [ ] Customize as needed

---

## 🎉 You're Ready!

Pick the documentation that matches your needs and get started!

**Most users should start with:** [`QUICK_START_GUIDE.md`](QUICK_START_GUIDE.md)

Happy analyzing! 🚀

---

*Last Updated: December 12, 2025*

