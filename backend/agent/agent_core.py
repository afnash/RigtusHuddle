from google import genai
from google.genai import types
from tools.load_json import load_linkedin_comments
import os

def run_analysis(data_file="linkedin_comments.json"):
    """
    Runs the multi-agent analysis on the provided data file.
    Returns a dictionary with the results.
    """
    results = {
        "youth_analysis": "",
        "adult_analysis": "",
        "strategy": "",
        "error": None
    }

    print(f"STEP 1: Starting analysis on {data_file}...")

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
            # Construct absolute path or ensure relative path works
            # We assume prompts are in the 'prompts' subdirectory relative to this file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "prompts", filename)
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"❌ ERROR: Cannot load prompt {filename}: {e}")
            return None

    # --- Agent for 18-30 Age Group ---
    try:
        instructions = load_prompt("analyze_campaign.prompt")
        if not instructions:
            raise Exception("Failed to load analyze_campaign.prompt")
        
        print("STEP 3: Loaded prompt (18-30).")

        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[load_linkedin_comments],
                system_instruction=instructions
            )
        )
        print("STEP 4: Chat session (18-30) created.")

        print("STEP 5: Sending message to agent (18-30)...")
        # We pass the filename to the prompt/tool if needed, or just rely on the tool knowing what to do.
        # The prompt in main.py hardcoded 'linkedin_comments.json'. 
        # Ideally we should pass the filename if the tool accepts it, but load_linkedin_comments might be fixed.
        # Let's inspect tools/load_json.py if possible, but for now we follow main.py pattern.
        # main.py message: "Please load the linkedin comments from 'linkedin_comments.json'..."
        
        response = chat.send_message(
            message=f"Please load the linkedin comments from '{data_file}' and analyze them according to the instructions."
        )

        print("STEP 6: Response (18-30) received.")
        results["youth_analysis"] = response.text

    except Exception as e:
        print(f"❌ ERROR during 18-30 agent execution: {e}")
        # We might continue or return error depending on strictness. 
        # Let's continue to try other agents but note the error?
        # For now, if this fails, strategy will likely fail too.

    # --- Agent for 30-50 Age Group ---
    print("-" * 30)
    try:
        instructions_30_50 = load_prompt("analyze_campaign_30_50.prompt")
        if not instructions_30_50:
            raise Exception("Failed to load analyze_campaign_30_50.prompt")
            
        print("STEP 7: Loaded 30-50 prompt.")
        
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
            message=f"Please load the linkedin comments from '{data_file}' and analyze them for the 30-50 age group."
        )
        
        print("STEP 10: Response (30-50) received.")
        results["adult_analysis"] = response_30_50.text
        
    except Exception as e:
        print(f"❌ ERROR during 30-50 agent execution: {e}")

    # --- Strategist Agent ---
    if results["youth_analysis"] and results["adult_analysis"]:
        print("-" * 30)
        try:
            instructions_strategist = load_prompt("negotiate_suggestions.prompt")
            if not instructions_strategist:
                raise Exception("Failed to load negotiate_suggestions.prompt")

            print("STEP 11: Loaded Strategist prompt.")
            
            chat_strategist = client.chats.create(
                model="gemini-2.5-flash", 
                config=types.GenerateContentConfig(
                    system_instruction=instructions_strategist
                )
            )
            print("STEP 12: Chat session (Strategist) created.")
            
            strategist_message = f"""
            Here is the analysis from the 18-30 Age Group:
            {results['youth_analysis']}
            
            Here is the analysis from the 30-50 Age Group:
            {results['adult_analysis']}
            
            Please negotiate and provide strategic suggestions based on these reports.
            """
            
            print("STEP 13: Sending message to Strategist Agent...")
            response_strategist = chat_strategist.send_message(message=strategist_message)
            
            print("STEP 14: STRATEGIST RESPONSE received.")
            results["strategy"] = response_strategist.text
            
        except Exception as e:
            print(f"❌ ERROR during Strategist execution: {e}")
            results["error"] = str(e) # Capture strategist error if it happens
    else:
        msg = "Skipping Strategist: Missing analysis from one or more groups."
        print(msg)
        if not results["error"]:
             results["error"] = msg

    return results
