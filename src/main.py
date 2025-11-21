import argparse
import os
import sys
from rich.console import Console
from dotenv import load_dotenv

# Add src to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser import parse_markdown
from generator import generate_scene_code
from renderer import render_code

load_dotenv()
console = Console()

def main():
    parser = argparse.ArgumentParser(description="Manimator: Convert Markdown to Manim Video")
    parser.add_argument("input_file", help="Path to the input markdown file")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        console.print(f"[bold red]Input file not found: {args.input_file}[/bold red]")
        return

    if not os.getenv("OPENROUTER_API_KEY"):
        console.print("[bold red]Error: OPENROUTER_API_KEY not found in .env[/bold red]")
        return

    console.print(f"[bold green]Processing {args.input_file}...[/bold green]")
    
    scenes = parse_markdown(args.input_file)
    console.print(f"Found {len(scenes)} scenes.")
    
    for scene in scenes:
        console.print(f"\n[bold cyan]Generating code for scene: {scene['scene_name']}...[/bold cyan]")
        try:
            code = generate_scene_code(scene)
            # console.print(f"[dim]{code}[/dim]") # Debug: show generated code
            
            render_code(code, scene['scene_name'])
            
        except Exception as e:
            console.print(f"[bold red]Failed to process scene {scene['scene_name']}: {e}[/bold red]")

if __name__ == "__main__":
    main()
