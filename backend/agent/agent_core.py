from dotenv import load_dotenv
load_dotenv()
from google import generativeai as genai
from tools.load_json import load_linkedin_comments
import os
import base64
import io
from PIL import Image
import json
import requests
from bs4 import BeautifulSoup

# Configure Gemini API
api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
if api_key:
    genai.configure(api_key=api_key)

def run_analysis(data_file="linkedin_comments.json", platform="linkedin", url=None):
    """
    Runs the multi-agent analysis on existing comments (Post-Launch).
    If a URL is provided, it attempts to scrape/simulate comments for that URL.
    """
    results = {
        "youth_analysis": "",
        "adult_analysis": "",
        "strategy": "",
        "error": None
    }

    print(f"STEP 1: Starting analysis for {platform}...")

    try:
        # Test API configuration
        if not os.environ.get('GEMINI_API_KEY') and not os.environ.get('GOOGLE_API_KEY'):
            raise Exception("GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set")
        print("STEP 2: API configured successfully.")
    except Exception as e:
        error_msg = f"Failed to configure genai: {e}"
        print(f"❌ ERROR: {error_msg}")
        results["error"] = error_msg
        return results

    # Helper to load prompts safely
    def load_prompt(filename):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "prompts", filename)
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"❌ ERROR: Cannot load prompt {filename}: {e}")
            return None

    # --- Data Source Handling ---
    comments_text = ""
    
    if url and url != "demo":
        print(f"STEP 2.5: Analyzing URL: {url}")
        try:
            # Simple scrape attempt for context
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            page_text = ""
            try:
                resp = requests.get(url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.content, 'html.parser')
                    title = soup.title.string if soup.title else ""
                    meta = soup.find('meta', attrs={'name': 'description'})
                    desc = meta['content'] if meta else ""
                    page_text = f"Page Title: {title}\nDescription: {desc}"
            except:
                print("Direct scraping failed/blocked. Proceeding with URL simulation.")
            
            # Use LLM to generate realistic comments
            print("STEP 2.6: Generating synthetic comments for URL...")
            simulator_model = genai.GenerativeModel('gemini-2.5-flash')
            simulator_prompt = f"""
            You are a Social Media Simulator. The user provided this URL: {url}
            Context extracted: {page_text}
            
            Please generate a JSON dataset of 20 realistic comments that would likely appear on this post.
            Include a mix of ages (Youth/Adult), sentiments, and styles appropriate for {platform}.
            
            Format:
            [
                {{"user": "User1", "comment": "...", "age_group": "18-30"}},
                {{"user": "User2", "comment": "...", "age_group": "30-50"}}
            ]
            Return ONLY raw JSON.
            """
            sim_resp = simulator_model.generate_content(simulator_prompt)
            comments_text = sim_resp.text
            print("STEP 2.7: Synthetic comments generated.")
            
        except Exception as e:
            print(f"Error simulating URL data: {e}")
            comments_text = "[]" 
    else:
        # Fallback to local file
        data_source_name = "linkedin_comments.json"
        if platform == "instagram":
             data_source_name = "instagram_comments.json"
             
        # Use absolute path to ensure file is found
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, data_source_name)
        
        print(f"STEP 2.5: Loading local file: {file_path}")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                comments_text = f.read()
        else:
             print(f"❌ File not found: {file_path}")
             return {"error": f"Data file not found: {data_source_name}"}

    # Determine Prompts based on Platform
    if platform.lower() == "instagram":
        prompt_youth = "analyze_instagram_18_30.prompt"
        prompt_adult = "analyze_instagram_30_50.prompt"
    else:
        prompt_youth = "analyze_campaign.prompt"
        prompt_adult = "analyze_campaign_30_50.prompt"
        
    # Fallback to existing file if specific one missing
    # This block is now redundant due to the new data source handling, but keeping it as per instruction to not make unrelated edits.
    # The `data_source_name` variable is now local to the `else` block above.
    # if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", data_source_name)):
    #      data_source_name = data_file 

    # --- Agent for 18-30 Age Group ---
    try:
        instructions = load_prompt(prompt_youth)
        if not instructions:
            raise Exception(f"Failed to load {prompt_youth}")
        
        print(f"STEP 3: Loaded prompt (18-30) for {platform}.")

        # Load the comments data
        # comments_data = load_linkedin_comments(data_source_name) # Removed
        # comments_text = json.dumps(comments_data, indent=2) # Removed
        
        # Create model with system instruction
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=instructions
        )
        print("STEP 4: Model (18-30) created.")

        print("STEP 5: Sending message to agent (18-30)...")
        
        # Generate response
        full_prompt = f"Here is the comments data from {platform}:\n\n{comments_text[:30000]}\n\nPlease analyze these comments according to the instructions for the 18-30 age group."
        response = model.generate_content(full_prompt)

        print("STEP 6: Response (18-30) received.")
        results["youth_analysis"] = response.text

    except Exception as e:
        print(f"❌ ERROR during 18-30 agent execution: {e}")

    # --- Agent for 30-50 Age Group ---
    print("-" * 30)
    try:
        instructions_30_50 = load_prompt(prompt_adult)
        if not instructions_30_50:
            raise Exception(f"Failed to load {prompt_adult}")
            
        print(f"STEP 7: Loaded 30-50 prompt for {platform}.")
        
        # Create model with system instruction
        model_30_50 = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=instructions_30_50
        )
        print("STEP 8: Model (30-50) created.")
        
        print("STEP 9: Sending message to agent (30-50)...")
        
        # Generate response
        full_prompt_30_50 = f"Here is the comments data from {platform}:\n\n{comments_text[:30000]}\n\nPlease analyze these comments according to the instructions for the 30-50 age group."
        response_30_50 = model_30_50.generate_content(full_prompt_30_50)
        
        print("STEP 10: Response (30-50) received.")
        results["adult_analysis"] = response_30_50.text
        
    except Exception as e:
        print(f"❌ ERROR during 30-50 agent execution: {e}")

    # --- Strategist Agent ---
    return run_strategist(results, load_prompt, mode="post")


def run_pre_analysis(image_b64, text_content, platform="linkedin", target_group="all"):
    """
    Runs the predictive analysis on a creative (Image + Text).
    """
    results = {
        "youth_analysis": "",
        "adult_analysis": "",
        "strategy": "",
        "error": None
    }
    
    print(f"STEP 1: Starting PRE-analysis for {platform} targeting {target_group}...")

    # Decode Image
    try:
        if "base64," in image_b64:
            image_b64 = image_b64.split("base64,")[1]
        
        image_data = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_data))
        print("STEP 2.5: Image decoded successfully.")
    except Exception as e:
        return {"error": f"Invalid image data: {e}"}

    try:
        if not os.environ.get('GEMINI_API_KEY') and not os.environ.get('GOOGLE_API_KEY'):
            raise Exception("GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set")
        print("STEP 2: API configured successfully.")
    except Exception as e:
        return {"error": f"Failed to configure genai: {e}"}

    # Helper to load prompts safely
    def load_prompt(filename):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "prompts", filename)
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"❌ ERROR: Cannot load prompt {filename}: {e}")
            return None

    # --- Agents ---
    
    run_youth = target_group in ["all", "youth"]
    run_adult = target_group in ["all", "adult"]

    prompt_base = f"""
    You are analyzing a marketing creative for {platform}.
    Please look at the attached image and the following caption: "{text_content}"
    
    Predict the reaction. Will it work? Is it 'cringe' or 'cool' (if youth)? Is it 'trustworthy' or 'spammy' (if adult)?
    Be specific about the visual elements and the copy.
    """

    if run_youth:
        try:
            print("STEP: Running Youth Agent (Pre)...")
            model_youth = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction="You are a Gen-Z digital native (age 18-24). You are critical of ads. You value authenticity, aesthetics, and humor. You hate corporate speak."
            )
            response = model_youth.generate_content([prompt_base, image])
            results["youth_analysis"] = response.text
            print("STEP: Youth analysis done.")
        except Exception as e:
            print(f"❌ Youth Agent Error: {e}")

    if run_adult:
        try:
            print("STEP: Running Adult Agent (Pre)...")
            model_adult = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction="You are a working professional (age 35-50). You value clarity, value propositions, and professionalism. You are skeptical of clickbait."
            )
            response = model_adult.generate_content([prompt_base, image])
            results["adult_analysis"] = response.text
            print("STEP: Adult analysis done.")
        except Exception as e:
            print(f"❌ Adult Agent Error: {e}")

    # --- Strategist Agent ---
    return run_strategist(results, load_prompt, mode="pre")


def run_strategist(results, load_prompt_func, mode="post"):
    """
    Common strategist logic to synthesize results into the final JSON dashboard format.
    mode: 'post' (includes hashtags) or 'pre' (includes pros/cons)
    """
    if results["youth_analysis"] or results["adult_analysis"]:
        print("-" * 30)
        try:
            instructions_strategist = load_prompt_func("negotiate_suggestions.prompt")
            
            # Dynamic JSON Structure Definition
            additional_fields = ""
            if mode == "pre":
                additional_fields = """
                "pros_cons": {
                    "pros": ["list of strong points..."],
                    "cons": ["list of weak points..."]
                },
                """
            else:
                additional_fields = """
                "hashtag_strategy": {
                    "trending": ["#Trend1", "#Trend2"],
                    "niche": ["#Niche1", "#Niche2"],
                    "insight": "Explain why these tags were chosen..."
                },
                """

            # Complete JSON Instruction
            instructions_strategist += f"""
            
            CRITICAL: You must output your response in valid JSON format ONLY. 
            Structure:
            {{
                "final_verdict": "HTML string with bold verdict and explanation. Keep it under 50 words.",
                "tone_analysis": {{
                    "label": "e.g. Inspirational",
                    "score": 88
                }},
                "engagement_metrics": {{
                    "score": "8.5/10",
                    "virality": "High/Medium/Low",
                    "explanation": "Brief reason"
                }},
                {additional_fields}
                "strategic_suggestions": [
                    {{"title": "...", "priority": "High/Medium", "description": "..."}}
                ],
                "shared_positives": ["points that both groups liked..."]
            }}
            Do not use markdown code blocks like ```json. Return raw JSON.
            """
            
            model_strategist = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=instructions_strategist
            )
            
            strategist_message = f"""
            Analysis 1 (Youth): {results.get('youth_analysis', 'N/A')}
            Analysis 2 (Adult): {results.get('adult_analysis', 'N/A')}
            
            Synthesize a strategy for this campaign properly.
            """
            
            print("STEP: Sending to Strategist...")
            response_strategist = model_strategist.generate_content(strategist_message)
            results["strategy"] = response_strategist.text
            print("STEP: Strategist done.")
            
        except Exception as e:
            print(f"❌ Strategist Error: {e}")
            results["error"] = str(e)
    else:
        results["error"] = "No analysis generated from agents."

    return results

def apply_changes(image_b64, text_content, suggestions):
    """
    Applies strategic suggestions to the content and generates a new image prompt.
    """
    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"""
        You are an expert Copywriter and Creative Director.
        
        Original Content: "{text_content}"
        
        Strategic Suggestions to Apply:
        {suggestions}
        
        Task:
        1. Rewrite the caption/text content to incorporate the suggestions. Make it engaging.
        2. Create a detailed Image Generation Prompt that would result in a visual matching the suggestions.
        
        Output JSON:
        {{
            "new_content": "...",
            "new_image_prompt": "..."
        }}
        """
        
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        print(f"❌ Apply Changes Error: {e}")
        return None
