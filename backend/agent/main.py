from google import genai
from google.genai import types
from tools.load_json import load_linkedin_comments

print("STEP 1: Starting script...")

try:
    client = genai.Client()
    print("STEP 2: Client created successfully.")
except Exception as e:
    print("❌ ERROR: Failed to create genai client:", e)
    exit()

try:
    instructions = open("prompts/analyze_campaign.prompt").read()
    print("STEP 3: Loaded prompt.")
except Exception as e:
    print("❌ ERROR: Cannot load prompt:", e)
    exit()

try:
    # Create the chat session with the model and tools
    # Note: 'tools' should be a list of functions or tool objects
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
        message="Please load the linkedin comments from 'linkedin_comments.json' and analyze them according to the instructions."
    )

    print("STEP 6: Response (18-30) received.")
    print(response.text)
    analysis_18_30 = response.text

    # --- Agent for 30-50 Age Group ---
    print("-" * 30)
    analysis_30_50 = ""
    try:
        instructions_30_50 = open("prompts/analyze_campaign_30_50.prompt").read()
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
            message="Please load the linkedin comments from 'linkedin_comments.json' and analyze them for the 30-50 age group."
        )
        
        print("STEP 10: Response (30-50) received.")
        print(response_30_50.text)
        analysis_30_50 = response_30_50.text
        
    except Exception as e:
         print("❌ ERROR during 30-50 agent execution:", e)

    # --- Strategist Agent ---
    if analysis_18_30 and analysis_30_50:
        print("-" * 30)
        try:
            instructions_strategist = open("prompts/negotiate_suggestions.prompt").read()
            print("STEP 11: Loaded Strategist prompt.")
            
            # Strategist doesn't need the JSON tool, just the text analysis
            chat_strategist = client.chats.create(
                model="gemini-2.5-flash", 
                config=types.GenerateContentConfig(
                    system_instruction=instructions_strategist
                )
            )
            print("STEP 12: Chat session (Strategist) created.")
            
            strategist_message = f"""
            Here is the analysis from the 18-30 Age Group:
            {analysis_18_30}
            
            Here is the analysis from the 30-50 Age Group:
            {analysis_30_50}
            
            Please negotiate and provide strategic suggestions based on these reports.
            """
            
            print("STEP 13: Sending message to Strategist Agent...")
            response_strategist = chat_strategist.send_message(message=strategist_message)
            
            print("STEP 14: STRATEGIST RESPONSE received.")
            print(response_strategist.text)
            
        except Exception as e:
            print("❌ ERROR during Strategist execution:", e)
    else:
        print("Skipping Strategist: Missing analysis from one or more groups.")

except Exception as e:
    print("❌ ERROR during agent execution:", e)
    import traceback
    traceback.print_exc()
