from google import genai
from google.genai import types
from tools.load_json import load_linkedin_comments
import os
import base64
import io
from PIL import Image

def run_analysis(data_file="linkedin_comments.json", platform="linkedin"):
    """
    Runs the multi-agent analysis on existing comments (Post-Launch).
    platform: 'linkedin' or 'instagram'
    """
    results = {
        "youth_analysis": "",
        "adult_analysis": "",
        "strategy": "",
        "error": None
    }

    print(f"STEP 1: Starting analysis on {data_file} for {platform}...")

    try:
        client = genai.Client()
        print("STEP 2: Client created successfully.")
    except Exception as e:
        error_msg = f"Failed to create genai client: {e}"
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

    # Determine Prompts based on Platform
    if platform.lower() == "instagram":
        prompt_youth = "analyze_instagram_18_30.prompt"
        prompt_adult = "analyze_instagram_30_50.prompt"
        data_source_name = "instagram_comments.json" 
    else:
        prompt_youth = "analyze_campaign.prompt"
        prompt_adult = "analyze_campaign_30_50.prompt"
        data_source_name = "linkedin_comments.json"
        
    # Fallback to existing file if specific one missing
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", data_source_name)):
         data_source_name = data_file 

    # --- Agent for 18-30 Age Group ---
    try:
        instructions = load_prompt(prompt_youth)
        if not instructions:
            raise Exception(f"Failed to load {prompt_youth}")
        
        print(f"STEP 3: Loaded prompt (18-30) for {platform}.")

        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[load_linkedin_comments],
                system_instruction=instructions
            )
        )
        print("STEP 4: Chat session (18-30) created.")

        print("STEP 5: Sending message to agent (18-30)...")
        
        response = chat.send_message(
            message=f"Please load the comments from '{data_source_name}' and analyze them according to the instructions for {platform}."
        )

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
        
        chat_30_50 = client.chats.create(
            model="gemini-2.5-flash", 
            config=types.GenerateContentConfig(
                tools=[load_linkedin_comments],
                system_instruction=instructions_30_50
            )
        )
        print("STEP 8: Chat session (30-50) created.")
        
        print("STEP 9: Sending message to agent (30-50)...")
        response_30_50 = chat_30_50.send_message(
            message=f"Please load the comments from '{data_source_name}' and analyze them for the 30-50 age group on {platform}."
        )
        
        print("STEP 10: Response (30-50) received.")
        results["adult_analysis"] = response_30_50.text
        
    except Exception as e:
        print(f"❌ ERROR during 30-50 agent execution: {e}")

    # --- Strategist Agent ---
    return run_strategist(results, client, load_prompt)


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
        print("STEP 1.5: Image decoded successfully.")
    except Exception as e:
        return {"error": f"Invalid image data: {e}"}

    try:
        client = genai.Client()
    except Exception as e:
        return {"error": f"Failed to create genai client: {e}"}

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
    # We use a generic prompt structure for visual analysis but customize the persona system instruction.
    
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
            # We can reuse the existing system instruction for persona, or send it in the message.
            # Let's use a fresh chat with specific instructions.
            chat_youth = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction="You are a Gen-Z digital native (age 18-24). You are critical of ads. You value authenticity, aesthetics, and humor. You hate corporate speak."
                )
            )
            response = chat_youth.send_message(message=[prompt_base, image])
            results["youth_analysis"] = response.text
            print("STEP: Youth analysis done.")
        except Exception as e:
            print(f"❌ Youth Agent Error: {e}")

    if run_adult:
        try:
            print("STEP: Running Adult Agent (Pre)...")
            chat_adult = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction="You are a working professional (age 35-50). You value clarity, value propositions, and professionalism. You are skeptical of clickbait."
                )
            )
            response = chat_adult.send_message(message=[prompt_base, image])
            results["adult_analysis"] = response.text
            print("STEP: Adult analysis done.")
        except Exception as e:
            print(f"❌ Adult Agent Error: {e}")

    # --- Strategist Agent ---
    return run_strategist(results, client, load_prompt)


def run_strategist(results, client, load_prompt_func):
    """
    Common strategist logic to synthesize results into the final JSON dashboard format.
    """
    if results["youth_analysis"] or results["adult_analysis"]:
        print("-" * 30)
        try:
            # We need a prompt that forces the JSON output format expected by the frontend
            # The existing 'negotiate_suggestions.prompt' might return text. 
            # We should wrap it or enforce JSON. 
            
            instructions_strategist = load_prompt_func("negotiate_suggestions.prompt")
            # We append a strong JSON instruction
            instructions_strategist += """
            
            CRITICAL: You must output your response in valid JSON format ONLY. 
            Structure:
            {
                "final_verdict": "HTML string with bold verdict and explanation",
                "strategic_suggestions": [
                    {"title": "...", "priority": "High/Medium", "description": "..."}
                ],
                "shared_positives": ["points that both groups liked..."]
            }
            Do not use markdown code blocks like ```json. Return raw JSON.
            """
            
            chat_strategist = client.chats.create(
                model="gemini-2.5-flash", 
                config=types.GenerateContentConfig(
                    system_instruction=instructions_strategist
                )
            )
            
            strategist_message = f"""
            Analysis 1 (Youth): {results.get('youth_analysis', 'N/A')}
            Analysis 2 (Adult): {results.get('adult_analysis', 'N/A')}
            
            Synthesize a strategy for this campaign properly.
            """
            
            print("STEP: Sending to Strategist...")
            response_strategist = chat_strategist.send_message(message=strategist_message)
            results["strategy"] = response_strategist.text
            print("STEP: Strategist done.")
            
        except Exception as e:
            print(f"❌ Strategist Error: {e}")
            results["error"] = str(e)
    else:
        results["error"] = "No analysis generated from agents."

    return results
