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
    # -o = specify output filename explicitly to make it predictable
    output_filename = f"{scene_name.replace(' ', '_')}.mp4"
    
    cmd = [
        "manim",
        "-ql",
        "--media_dir", output_dir,
        "-o", output_filename,
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
        
        # Construct the expected output path
        # Manim structure: {media_dir}/videos/{temp_file_basename}/480p15/{output_filename}
        # Note: temp_file has .py extension, basename removes it? No, manim uses the module name usually.
        # Let's verify the folder structure Manim creates.
        # Usually: media_dir/videos/temp_scene_intro/480p15/Intro.mp4
        
        # We can try to parse the output for "File ready at" to be sure
        import re
        match = re.search(r"File ready at '(.+?)'", result.stdout)
        match_stderr = re.search(r"File ready at '(.+?)'", result.stderr) # Manim often prints to stderr
        
        if match:
            return match.group(1)
        elif match_stderr:
            return match_stderr.group(1)
        else:
            # Fallback guess
            # This might be risky if Manim changes structure, but let's try to find it
            # It's likely in output_dir/videos/{temp_file without .py}/480p15/{output_filename}
            module_name = temp_file.replace(".py", "")
            # For -ql (quality low), it's 480p15
            possible_path = os.path.join(output_dir, "videos", module_name, "480p15", output_filename)
            if os.path.exists(possible_path):
                return possible_path
            
            console.print(f"[yellow]Warning: Could not determine output path for {scene_name}[/yellow]")
            return None
            
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error rendering {scene_name}![/bold red]")
        console.print(e.stderr)
        return None
