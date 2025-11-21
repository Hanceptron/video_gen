import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

REPAIR_SYSTEM_PROMPT = """You are a Manim Code Repairer.
Your job is to fix Python code that caused an error when running Manim.

You will be given:
1. The broken code.
2. The error traceback/message.

Instructions:
1. Analyze the error.
2. Fix the code to resolve the error.
3. Output ONLY the fixed Python code inside the `construct(self):` method.
4. Do NOT output the class definition, just the inner code.
5. Do not explain your fix, just output the code.

Common Fixes:
- NameError 'Clear' -> Use `self.clear()` or `self.remove(mobj)`.
- LaTeX Error -> The user might have used invalid LaTeX. Switch to `Text` or `MarkupText` if `Tex` fails, or fix the LaTeX syntax.
- IndentationError -> Ensure correct indentation.
- TypeError (VGroup) -> If adding ImageMobject to VGroup, change VGroup to Group.
- Write/Create on Image -> Change to FadeIn or ScaleInPlace.
"""

def repair_code(broken_code, error_message):
    """
    Uses LLM to repair broken Manim code based on the error message.
    
    Args:
        broken_code (str): The code that failed.
        error_message (str): The error traceback.
        
    Returns:
        str: The fixed code.
    """
    user_prompt = f"""
    ### BROKEN CODE:
    {broken_code}
    
    ### ERROR MESSAGE:
    {error_message}
    
    ### TASK:
    Fix the code to solve the error. Output only the code inside construct(self).
    """
    
    model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": REPAIR_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Lower temperature for more deterministic fixes
        )
        
        code = response.choices[0].message.content.strip()
        
        # Cleanup markdown fences
        if code.startswith("```python"):
            code = code[9:]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
            
        return code.strip()
        
    except Exception as e:
        print(f"Repair failed: {e}")
        return broken_code # Return original if repair fails
