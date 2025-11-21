import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

SYSTEM_PROMPT = """You are a Manim Code Generator. You output ONLY valid Python code inside a construct(self): method. Do not output the class definition, just the code inside.

CRITICAL CONSTRAINTS (The "Slide-First" Rule):
1. RARELY use absolute coordinates (like UP * 3). Instead, use relative positioning: .next_to(), .arrange(), .to_edge().
2. For lists of text, ALWAYS use VGroup and .arrange(DOWN, aligned_edge=LEFT).
   - WARNING: VGroup ONLY accepts vector objects (Text, Circle, etc.).
   - If you are using ImageMobject, you MUST use Group(), not VGroup().
   - DO NOT use `Write` or `Create` on ImageMobject or SVGMobject. Use `FadeIn`, `ScaleInPlace`, or `GrowFromCenter`.
3. Use MarkupText for text generation to support bold/color (e.g., MarkupText("<b>Bold</b>", font_size=32)).
   - IMPORTANT: MarkupText ONLY supports Pango Markup.
   - DO NOT use LaTeX commands like `\\checkbox`, `\\textbf`, `\\item` inside MarkupText.
   - For bullet points, just use a string like "• Item".
   - For checkmarks, use unicode "✓" or "✗".
   - If you need complex symbols, create them using shapes (e.g., Square(), Circle()) or use MathTex for actual math.
4. Use self.next_section() after every distinct animation block.
5. Do not include ```python or ``` markdown fences. Just the raw code.
6. Assume `from manim import *` is already present.

TIMING & PACING (Crucial):
- You will be given an 'Estimated Duration' for the narrative.
- You MUST ensure the total `self.wait()` times in the scene add up to at least this duration.
- Distribute the waits *after* animations so the viewer has time to absorb the visual before the next thing happens.
- NEVER use `self.wait()` without arguments if you need a specific pause. Use `self.wait(2)` etc.

VISUAL FIDELITY (Crucial):
- If the user asks for an icon or object (e.g., "notebook", "bank", "server"), DO NOT just write the word "Bank".
- COMPOSE the object using geometric primitives (Rectangle, Circle, Line, etc.).
  - Example: A "Server" could be a Rectangle with small Circles (lights) and Lines (vents).
  - Example: A "Block" should be a Square with Lines inside representing data.
- If an animation is described (e.g., "rejected stamp"), create a visual representation of that (e.g., a red "REJECTED" text with a box around it, appearing with a `ScaleInPlace` animation).
"""

def generate_scene_code(scene_data):
    """
    Generates Manim code for a single scene using OpenRouter.
    
    Args:
        scene_data (dict): {'scene_name': str, 'narrative': str, 'visual_instruction': str}
        
    Returns:
        str: The generated Python code for the construct method.
    """
    # Calculate estimated duration based on narrative word count
    # Avg reading speed: 150 wpm = 2.5 words/sec
    narrative = scene_data.get('narrative', "")
    word_count = len(narrative.split())
    estimated_duration = max(2.0, word_count / 2.5) # Minimum 2 seconds
    
    user_prompt = f"""
    Scene Name: {scene_data['scene_name']}
    Narrative Context: {scene_data['narrative']}
    Visual Instructions: {scene_data['visual_instruction']}
    Estimated Duration Needed: {estimated_duration:.1f} seconds
    
    Generate the Manim code for this scene. Ensure the total wait time matches the estimated duration.
    Make the visuals rich and composed of shapes, not just text labels.
    """
    
    model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )
    
    code = response.choices[0].message.content.strip()
    
    # Cleanup if the LLM still adds markdown fences despite instructions
    if code.startswith("```python"):
        code = code[9:]
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
        
    return code.strip()
