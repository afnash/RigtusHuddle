#!/usr/bin/env python3
"""
LinkedIn Comments Age Classifier Agent
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
        
        print(f"\nAnalyzing {total} comments...")
        print("-" * 80)
        
        for idx, comment in enumerate(comments, 1):
            print(f"Processing comment {idx}/{total}...", end=" ")
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
        
        print("\n" + "=" * 80)
        print("ANALYSIS REPORT - LINKEDIN COMMENTS AGE CLASSIFICATION")
        print("=" * 80)
        print(f"\nTotal Comments Analyzed: {len(analyses)}")
        print(f"Comments from 18-30 Age Group: {len(young_adult_comments)}")
        print(f"Percentage: {len(young_adult_comments)/len(analyses)*100:.1f}%")
        print("\n" + "-" * 80)
        print("COMMENTS IDENTIFIED AS 18-30 AGE GROUP:")
        print("-" * 80)
        
        for idx, analysis in enumerate(young_adult_comments, 1):
            print(f"\n{idx}. Comment ID: {analysis.comment_id}")
            print(f"   Author: {analysis.author}")
            print(f"   Text: \"{analysis.text}\"")
            print(f"   Confidence: {analysis.confidence_score:.2f}")
            print(f"   Keywords: {', '.join(analysis.keywords_identified) if analysis.keywords_identified else 'None'}")
            print(f"   Reasoning: {analysis.reasoning}")
        
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
                        "author": a.author,
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
                        "author": a.author,
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
            
            print(f"\n" + "=" * 80)
            print(f"Detailed JSON report saved to: {output_file}")
        
        print("=" * 80 + "\n")


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
            
        # Handle different JSON structures
        if isinstance(data, dict) and "comments" in data:
            return data["comments"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid JSON format. Expected 'comments' key or list of comments")
            
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)


def main():
    """Main function to run the age classifier agent"""
    
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set!")
        print("Please set it using: export GEMINI_API_KEY='your-api-key'")
        print("Or create a .env file with: GEMINI_API_KEY=your-api-key")
        sys.exit(1)
    
    # Get input file from command line or use default
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "linkedin_comments_sample.json"
    
    # Get output file from command line or use default
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = "age_classification_report.json"
    
    print("=" * 80)
    print("LINKEDIN COMMENTS AGE CLASSIFIER AGENT")
    print("=" * 80)
    print(f"\nInput file: {input_file}")
    print(f"Output file: {output_file}")
    
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

