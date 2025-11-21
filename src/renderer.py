import os
import subprocess
import sys
from rich.console import Console

console = Console()

TEMPLATE = """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        {code}
"""

def render_code(python_code, scene_name, output_dir="output"):
    """
    Wraps the generated code in a Scene class and renders it using Manim.
    
    Args:
        python_code (str): The code inside construct(self).
        scene_name (str): Name of the scene (used for file naming).
        output_dir (str): Directory for output.
    """
    # Indent the code to fit inside the class
    indented_code = "\n        ".join(python_code.splitlines())
    full_script = TEMPLATE.format(code=indented_code)
    
    temp_file = f"temp_{scene_name.lower().replace(' ', '_')}.py"
    
    with open(temp_file, "w") as f:
        f.write(full_script)
        
    # Run Manim
    # -ql = Quality Low (faster for testing)
    # --media_dir = specify output directory
    cmd = [
        "manim",
        "-ql",
        "--media_dir", output_dir,
        temp_file,
        "GeneratedScene"
    ]
    
    console.print(f"[bold blue]Rendering scene: {scene_name}...[/bold blue]")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        console.print(f"[bold green]Successfully rendered {scene_name}![/bold green]")
        # Optional: Print stdout if needed, or just keep it clean
        
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error rendering {scene_name}![/bold red]")
        console.print(e.stderr)
    finally:
        # Cleanup temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
