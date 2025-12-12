#!/usr/bin/env python3
"""
Linken Comments Age Classifier Agent
Uses Google Gemini API to analyze comments and classify likely age group (18-30)
"""

import json
import os
import sys
from typing import List, Dict, Any
from dataclasses import dataclass
import google.generativeai as genai
from datetime import datetime


@dataclass
class CommentAnalysis:
    """Data class to store comment analysis results"""
    comment_id: str
    author: str
    text: str
    is_young_adult: bool
    confidence_score: float
    reasoning: str
    keywords_identified: List[str]


class LinkedInAgeClassifierAgent:
    """Agent to classify LinkedIn comments by age group using Gemini AI"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        """
        Initialize the agent with Gemini API
        
        Args:
            api_key: Google Gemini API key
            model_name: Gemini model to use (default: gemini-2.5-flash)
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.young_adult_keywords = [
            # Slang and informal language
            "yooo", "lit", "fire", "fam", "bro", "dude", "sick", "af", "bussin",
            "no cap", "vibing", "rn", "omg", "squad", "collab", "lowkey", "highkey",
            "fr", "ngl", "tbh", "imo", "bet", "slay", "goat", "flex", "sus",
            
            # Education and career stage
            "college", "university", "student", "graduated", "just started",
            "intern", "internship", "first job", "learning", "studying",
            
            # Generation markers
            "gen z", "millennial", "zoomer",
            
            # Digital native language
            "app", "tiktok", "insta", "snap", "meme", "content creator",
            "influencer", "stream", "vibe check",
            
            # Emojis (common among young adults)
            "🔥", "💯", "✨", "🎉", "🚀", "😂", "💀", "👀"
        ]
        
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract young adult keywords from comment text
        
        Args:
            text: Comment text to analyze
            
        Returns:
            List of identified keywords
        """
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in self.young_adult_keywords:
            if keyword.lower() in text_lower or keyword in text:
                found_keywords.append(keyword)
                
        return found_keywords
    
    def analyze_comment_with_gemini(self, comment_text: str) -> Dict[str, Any]:
        """
        Use Gemini API to analyze a single comment
        
        Args:
            comment_text: The comment text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        prompt = f"""
Analyze the following LinkedIn comment and determine if it's likely written by someone 
in the 18-30 age group (young adult/Gen Z/young millennial).

Consider:
1. Language style (casual/formal, slang usage)
2. Vocabulary and expressions
3. Career stage indicators (student, recent graduate, early career)
4. Communication patterns typical of young adults
5. Use of emojis and internet slang
6. References to experiences or life stage

Comment: "{comment_text}"

Provide your analysis in the following JSON format ONLY (no other text):
{{
    "is_young_adult": true/false,
    "confidence_score": 0.0-1.0,
    "reasoning": "brief explanation of your decision",
    "age_indicators": ["list", "of", "specific", "indicators", "found"]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            # Parse JSON response
            analysis = json.loads(response_text.strip())
            return analysis
            
        except Exception as e:
            print(f"Error analyzing comment with Gemini: {e}")
            return {
                "is_young_adult": False,
                "confidence_score": 0.0,
                "reasoning": f"Error: {str(e)}",
                "age_indicators": []
            }
    
    def analyze_comment(self, comment: Dict[str, Any]) -> CommentAnalysis:
        """
        Analyze a single comment combining keyword extraction and Gemini AI
        
        Args:
            comment: Comment dictionary with 'comment_id', 'author', 'text'
            
        Returns:
            CommentAnalysis object with results
        """
        comment_text = comment.get("text", "")
        comment_id = comment.get("comment_id", "unknown")
        author = comment.get("author", "Unknown")
        
        # Extract keywords first
        keywords = self.extract_keywords(comment_text)
        
        # Use Gemini for deeper analysis
        gemini_analysis = self.analyze_comment_with_gemini(comment_text)
        
        # Combine results
        is_young_adult = gemini_analysis.get("is_young_adult", False)
        confidence = gemini_analysis.get("confidence_score", 0.0)
        reasoning = gemini_analysis.get("reasoning", "No reasoning provided")
        age_indicators = gemini_analysis.get("age_indicators", [])
        
        # Merge keywords and age indicators
        all_keywords = list(set(keywords + age_indicators))
        
        return CommentAnalysis(
            comment_id=comment_id,
            author=author,
            text=comment_text,
            is_young_adult=is_young_adult,
            confidence_score=confidence,
            reasoning=reasoning,
            keywords_identified=all_keywords
        )
    
    def analyze_all_comments(self, comments: List[Dict[str, Any]]) -> List[CommentAnalysis]:
        """
        Analyze all comments in the list
        
        Args:
            comments: List of comment dictionaries
            
        Returns:
            List of CommentAnalysis objects
        """
        results = []
        total = len(comments)
        
        print(f"\n⏳ Analyzing {total} comments...\n")
        
        for idx, comment in enumerate(comments, 1):
            print(f"  [{idx}/{total}] ", end="", flush=True)
            analysis = self.analyze_comment(comment)
            results.append(analysis)
            print("✓")
            
        return results
    
    def generate_report(self, analyses: List[CommentAnalysis], output_file: str = None):
        """
        Generate a detailed report of the analysis
        
        Args:
            analyses: List of CommentAnalysis objects
            output_file: Optional file path to save JSON report
        """
        young_adult_comments = [a for a in analyses if a.is_young_adult]
        
        print(f"\n{'='*60}")
        print(f"📊 RESULTS")
        print(f"{'='*60}")
        print(f"  Total Comments: {len(analyses)}")
        print(f"  Age 18-30: {len(young_adult_comments)} ({len(young_adult_comments)/len(analyses)*100:.1f}%)")
        print(f"{'='*60}\n")
        
        if young_adult_comments:
            print("🎯 COMMENTS FROM 18-30 AGE GROUP:\n")
            for idx, a in enumerate(young_adult_comments, 1):
                # Truncate long comments
                text_preview = a.text[:80] + "..." if len(a.text) > 80 else a.text
                print(f"  {idx}. [{a.comment_id}] Confidence: {a.confidence_score:.2f}")
                print(f"     \"{text_preview}\"")
                if a.keywords_identified:
                    print(f"     Keywords: {', '.join(a.keywords_identified[:5])}")
                print()
        
        # Generate JSON report
        if output_file:
            report_data = {
                "analysis_timestamp": datetime.now().isoformat(),
                "total_comments": len(analyses),
                "young_adult_comments_count": len(young_adult_comments),
                "percentage": len(young_adult_comments)/len(analyses)*100,
                "young_adult_comments": [
                    {
                        "comment_id": a.comment_id,
                        "text": a.text,
                        "confidence_score": a.confidence_score,
                        "keywords_identified": a.keywords_identified,
                        "reasoning": a.reasoning
                    }
                    for a in young_adult_comments
                ],
                "all_analyses": [
                    {
                        "comment_id": a.comment_id,
                        "text": a.text,
                        "is_young_adult": a.is_young_adult,
                        "confidence_score": a.confidence_score,
                        "keywords_identified": a.keywords_identified,
                        "reasoning": a.reasoning
                    }
                    for a in analyses
                ]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Report saved: {output_file}\n")


def load_comments_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Load comments from JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        List of comment dictionaries
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_comments = []
        
        # Handle new "posts" format
        if isinstance(data, dict) and "posts" in data:
            for post_idx, post in enumerate(data["posts"], 1):
                post_url = post.get("postUrl", f"post_{post_idx}")
                comments = post.get("comments", [])
                
                for comment_idx, comment_text in enumerate(comments, 1):
                    all_comments.append({
                        "comment_id": f"p{post_idx}_c{comment_idx}",
                        "author": "Unknown",
                        "text": comment_text,
                        "post_url": post_url
                    })
            return all_comments
            
        # Handle old "comments" format
        elif isinstance(data, dict) and "comments" in data:
            return data["comments"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid JSON format. Expected 'posts' or 'comments' key")
            
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)


def main():
    """Main function to run the age classifier agent"""
    
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not set!")
        print("   export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)
    
    # Get input file from command line or use default
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "test.json"
    
    # Get output file from command line or use default
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = "age_classification_report.json"
    
    print(f"\n🤖 LinkedIn Age Classifier")
    print(f"📁 Input: {input_file}")
    
    # Load comments
    comments = load_comments_from_json(input_file)
    
    # Initialize agent
    agent = LinkedInAgeClassifierAgent(api_key=api_key)
    
    # Analyze comments
    analyses = agent.analyze_all_comments(comments)
    
    # Generate report
    agent.generate_report(analyses, output_file=output_file)


if __name__ == "__main__":
    main()

