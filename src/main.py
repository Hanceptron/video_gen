import argparse
import os
import sys
import subprocess
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
    
    video_files = []
    
    for scene in scenes:
        console.print(f"\n[bold cyan]Generating code for scene: {scene['scene_name']}...[/bold cyan]")
        try:
            code = generate_scene_code(scene)
            
            # Check code quality
            console.print(f"[dim]Checking code quality...[/dim]")
            from checker import check_code
            passed, feedback = check_code(code, scene)
            
            if not passed:
                console.print(f"[bold yellow]Quality Check Failed: {feedback}[/bold yellow]")
                console.print(f"[bold yellow]Regenerating with feedback...[/bold yellow]")
                # Regenerate with feedback (simple approach: append feedback to prompt)
                # For now, we'll just re-call generate with a modified prompt or just trust the repairer for crashes.
                # To properly regenerate, we'd need to modify generate_scene_code to accept feedback.
                # Let's do a simple hack: update the visual instruction temporarily
                original_instruction = scene['visual_instruction']
                scene['visual_instruction'] += f"\n\nCRITICAL FEEDBACK FROM PREVIOUS ATTEMPT: {feedback}"
                code = generate_scene_code(scene)
                scene['visual_instruction'] = original_instruction # Restore
                
                console.print(f"[bold green]Regenerated code.[/bold green]")
            else:
                console.print(f"[dim]Quality Check Passed.[/dim]")

            video_path = render_code(code, scene['scene_name'])
            if video_path:
                video_files.append(video_path)
            
        except Exception as e:
            console.print(f"[bold red]Failed to process scene {scene['scene_name']}: {e}[/bold red]")

    if video_files:
        console.print("\n[bold green]Merging videos...[/bold green]")
        # Create a file list for ffmpeg
        list_file = "video_list.txt"
        with open(list_file, "w") as f:
            for v in video_files:
                # ffmpeg requires absolute paths or relative safe paths
                abs_path = os.path.abspath(v)
                f.write(f"file '{abs_path}'\n")
        
        output_merged = "final_video.mp4"
        # ffmpeg command to concat
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            "-y", # overwrite
            output_merged
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            console.print(f"[bold green]Final video saved to: {os.path.abspath(output_merged)}[/bold green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]Error merging videos![/bold red]")
        finally:
            if os.path.exists(list_file):
                os.remove(list_file)
    else:
        console.print("[bold yellow]No videos were generated to merge.[/bold yellow]")

if __name__ == "__main__":
    main()
