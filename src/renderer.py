import os
import subprocess
import sys
import textwrap
from rich.console import Console

console = Console()

TEMPLATE = """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        {code}
"""

def fix_indentation(code):
    """
    Heuristic to fix indentation errors from LLM output.
    Rules:
    1. If previous line ends with :, (, [, {, ,, \, keep indentation.
    2. Otherwise, strip indentation (force flat).
    """
    lines = code.splitlines()
    fixed_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            fixed_lines.append("")
            continue
        
        # Find previous non-empty line
        prev_line = ""
        for p in reversed(fixed_lines):
            if p.strip():
                prev_line = p.strip()
                break
        
        # Check if we should preserve indentation
        if prev_line and (prev_line.endswith(":") or 
                          prev_line.endswith("(") or 
                          prev_line.endswith("[") or 
                          prev_line.endswith("{") or 
                          prev_line.endswith(",") or 
                          prev_line.endswith("\\")):
            fixed_lines.append(line)
        else:
            fixed_lines.append(stripped)
            
    return "\n".join(fixed_lines)

def render_code(python_code, scene_name, output_dir="output"):
    """
    Wraps the generated code in a Scene class and renders it using Manim.
    
    Args:
        python_code (str): The code inside construct(self).
        scene_name (str): Name of the scene (used for file naming).
        output_dir (str): Directory for output.
    """
    # Fix indentation using heuristic
    # First dedent to handle the case where the whole block is indented
    dedented_code = textwrap.dedent(python_code)
    fixed_code = fix_indentation(dedented_code)
    
    # Retry loop for repair
    max_retries = 3
    current_code = fixed_code
    
    for attempt in range(max_retries + 1):
        # Indent the code to fit inside the class
        indented_code = "\n        ".join(current_code.splitlines())
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
        
        console.print(f"[bold blue]Rendering scene: {scene_name} (Attempt {attempt+1}/{max_retries+1})...[/bold blue]")
        
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
            import re
            match = re.search(r"File ready at '(.+?)'", result.stdout)
            match_stderr = re.search(r"File ready at '(.+?)'", result.stderr) # Manim often prints to stderr
            
            if match:
                return match.group(1)
            elif match_stderr:
                return match_stderr.group(1)
            else:
                # Fallback guess
                module_name = temp_file.replace(".py", "")
                possible_path = os.path.join(output_dir, "videos", module_name, "480p15", output_filename)
                if os.path.exists(possible_path):
                    return possible_path
                
                console.print(f"[yellow]Warning: Could not determine output path for {scene_name}[/yellow]")
                return None
                
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error rendering {scene_name}![/bold red]")
            # console.print(e.stderr) # Too verbose, maybe just show last few lines?
            
            if attempt < max_retries:
                console.print(f"[bold yellow]Attempting to repair code...[/bold yellow]")
                # Call repairer
                from repairer import repair_code
                # We pass the *inner* code (current_code) and the error
                current_code = repair_code(current_code, e.stderr)
                # Loop continues to next attempt with new code
            else:
                console.print("[bold red]Max retries reached. Giving up.[/bold red]")
                console.print(e.stderr)
                return None
        finally:
            # Cleanup temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
