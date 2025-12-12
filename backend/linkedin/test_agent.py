#!/usr/bin/env python3
"""
Quick test script for the Age Classifier Agent
Tests basic functionality without requiring API key
"""

import json
from age_classifier_agent import LinkedInAgeClassifierAgent


def test_keyword_extraction():
    """Test keyword extraction functionality"""
    print("Testing keyword extraction...")
    
    # Mock agent (no API key needed for keyword extraction)
    class MockAgent:
        def __init__(self):
            self.young_adult_keywords = [
                "yooo", "lit", "fire", "fam", "bro", "dude", "sick", "af", "bussin",
                "no cap", "vibing", "rn", "omg", "squad", "collab", "college",
                "student", "graduated", "gen z", "🔥", "💯", "✨"
            ]
        
        def extract_keywords(self, text):
            text_lower = text.lower()
            found_keywords = []
            for keyword in self.young_adult_keywords:
                if keyword.lower() in text_lower or keyword in text:
                    found_keywords.append(keyword)
            return found_keywords
    
    agent = MockAgent()
    
    test_cases = [
        {
            "text": "Yooo this is fire! 🔥 Can't wait to try it out. Congrats fam!",
            "expected": ["yooo", "fire", "fam", "🔥"]
        },
        {
            "text": "lit af bro 💯 gonna share this with my squad",
            "expected": ["lit", "af", "bro", "squad", "💯"]
        },
        {
            "text": "I'm in college studying CS and this is exactly what I've been looking for",
            "expected": ["college"]
        },
        {
            "text": "As someone with 25 years of experience in the industry, I believe this is solid.",
            "expected": []
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        keywords = agent.extract_keywords(test["text"])
        expected = test["expected"]
        
        # Check if all expected keywords are found
        success = all(k in keywords for k in expected)
        
        if success:
            print(f"  ✓ Test {i} passed")
            passed += 1
        else:
            print(f"  ✗ Test {i} failed")
            print(f"    Expected: {expected}")
            print(f"    Got: {keywords}")
            failed += 1
    
    print(f"\nKeyword Extraction Tests: {passed} passed, {failed} failed")
    return failed == 0


def test_json_loading():
    """Test JSON file loading"""
    print("\nTesting JSON loading...")
    
    try:
        with open("linkedin_comments_sample.json", 'r') as f:
            data = json.load(f)
        
        if "comments" in data:
            comments = data["comments"]
            print(f"  ✓ Successfully loaded {len(comments)} comments")
            print(f"  ✓ Sample comment: {comments[0]['text'][:50]}...")
            return True
        else:
            print("  ✗ No 'comments' key found in JSON")
            return False
            
    except Exception as e:
        print(f"  ✗ Error loading JSON: {e}")
        return False


def test_data_structure():
    """Test that sample data has correct structure"""
    print("\nTesting data structure...")
    
    try:
        with open("linkedin_comments_sample.json", 'r') as f:
            data = json.load(f)
        
        comments = data.get("comments", [])
        
        if not comments:
            print("  ✗ No comments found")
            return False
        
        required_fields = ["comment_id", "author", "text"]
        
        for i, comment in enumerate(comments):
            for field in required_fields:
                if field not in comment:
                    print(f"  ✗ Comment {i} missing field: {field}")
                    return False
        
        print(f"  ✓ All {len(comments)} comments have required fields")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("AGE CLASSIFIER AGENT - QUICK TESTS")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Keyword Extraction", test_keyword_extraction()))
    results.append(("JSON Loading", test_json_loading()))
    results.append(("Data Structure", test_data_structure()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! The agent is ready to use.")
        print("\nNext steps:")
        print("1. Set your GEMINI_API_KEY environment variable")
        print("2. Run: python age_classifier_agent.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

