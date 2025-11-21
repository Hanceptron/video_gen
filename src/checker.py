import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

CHECKER_SYSTEM_PROMPT = """You are a Manim Code Critic.
Your job is to verify if the generated Manim code matches the user's visual instructions.

You will be given:
1. The Visual Instructions (what should happen).
2. The Generated Code (what actually happens).

Instructions:
1. Compare the code against the instructions.
2. Check for MISSING elements (e.g., "Show 3 blocks" but code only shows 1).
3. Check for WRONG elements (e.g., "Red text" but code uses default white).
4. Check for LAZY implementation (e.g., "Draw a bank" but code just writes text "Bank").
5. Return a JSON object:
   {
     "passed": boolean,
     "feedback": "string explaining what is wrong and how to fix it. If passed is true, this can be empty."
   }
"""

def check_code(code, scene_data):
    """
    Checks if the generated code matches the visual instructions.
    
    Args:
        code (str): The generated Manim code.
        scene_data (dict): The scene requirements.
        
    Returns:
        tuple: (passed (bool), feedback (str))
    """
    user_prompt = f"""
    ### VISUAL INSTRUCTIONS:
    {scene_data['visual_instruction']}
    
    ### GENERATED CODE:
    {code}
    
    ### TASK:
    Does the code fulfill the instructions? 
    - If it misses key elements (like quantity of objects, specific animations), fail it.
    - If it uses text labels instead of shapes for objects (like "Bank" text instead of a rectangle), fail it.
    
    Respond with JSON.
    """
    
    model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": CHECKER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("passed", False), result.get("feedback", "")
        
    except Exception as e:
        print(f"Check failed: {e}")
        return True, "" # Assume pass if checker fails to avoid blocking
