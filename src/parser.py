import re

def parse_markdown(file_path):
    """
    Parses a markdown file into a list of scene dictionaries.
    
    Args:
        file_path (str): Path to the markdown file.
        
    Returns:
        list: A list of dicts, e.g., [{'scene_name': 'Intro', 'narrative': '...', 'visual_instruction': '...'}]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by "## Scene: "
    # The regex looks for "## Scene:" followed by the name, then captures everything until the next "## Scene:" or end of file.
    scene_chunks = re.split(r'## Scene:\s*(.+)', content)[1:] # Skip the preamble before the first scene
    
    scenes = []
    
    # re.split returns [name1, content1, name2, content2, ...]
    for i in range(0, len(scene_chunks), 2):
        scene_name = scene_chunks[i].strip()
        scene_content = scene_chunks[i+1]
        
        # Extract Narrative and Visual using simple string searching or regex
        # Assuming format: **Narrative:** ... **Visual:** ...
        # But let's be robust to variations like **Narrative**: or just Narrative:
        
        narrative_match = re.search(r'\*\*Narrative:?\*\*\s*(.*?)(?=\*\*Visual|\Z)', scene_content, re.DOTALL | re.IGNORECASE)
        visual_match = re.search(r'\*\*Visual:?\*\*\s*(.*?)(?=$)', scene_content, re.DOTALL | re.IGNORECASE)
        
        narrative = narrative_match.group(1).strip() if narrative_match else ""
        visual_instruction = visual_match.group(1).strip() if visual_match else ""
        
        scenes.append({
            'scene_name': scene_name,
            'narrative': narrative,
            'visual_instruction': visual_instruction
        })
        
    return scenes

if __name__ == "__main__":
    # Simple test
    import sys
    if len(sys.argv) > 1:
        print(parse_markdown(sys.argv[1]))
