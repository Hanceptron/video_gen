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
3. Use MarkupText for text generation to support bold/color (e.g., MarkupText("<b>Bold</b>", font_size=32)).
4. Use self.next_section() after every distinct animation block to allow for partial rendering/debugging.
5. Do not include ```python or ``` markdown fences. Just the raw code.
6. Assume `from manim import *` is already present.

Example of good output:
title = MarkupText("<b>My Scene</b>").to_edge(UP)
self.play(Write(title))
self.wait()

self.next_section()

bullets = VGroup(
    MarkupText("Point 1"),
    MarkupText("Point 2")
).arrange(DOWN, aligned_edge=LEFT)
bullets.next_to(title, DOWN, buff=1.0)
self.play(FadeIn(bullets, lag_ratio=0.5))
self.wait()
"""

def generate_scene_code(scene_data):
    """
    Generates Manim code for a single scene using OpenRouter.
    
    Args:
        scene_data (dict): {'scene_name': str, 'narrative': str, 'visual_instruction': str}
        
    Returns:
        str: The generated Python code for the construct method.
    """
    user_prompt = f"""
    Scene Name: {scene_data['scene_name']}
    Narrative Context: {scene_data['narrative']}
    Visual Instructions: {scene_data['visual_instruction']}
    
    Generate the Manim code for this scene.
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
