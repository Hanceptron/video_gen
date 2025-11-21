# Manimator Script Template

This file serves as a template for creating videos with Manimator.
The parser looks for specific keywords: `## Scene:`, `**Narrative:**`, and `**Visual:**`.

---

## Scene: [Scene Name]
**Narrative:**
[Write the script or voiceover text here. This helps the AI understand the context of what is happening.]

**Visual:**
[Describe exactly what should appear on screen. Be specific about:]
- **Text:** What text to show? (e.g., "Show title 'Hello World'")
- **Layout:** Where should it go? (e.g., "Center of screen", "Top left")
- **Colors:** Any specific colors? (e.g., "Red text", "Blue circle")
- **Animations:** How should things appear? (e.g., "Fade in", "Write text", "Grow from center")

---

## Scene: Example - Introduction
**Narrative:**
Welcome to this tutorial on Python lists. Lists are versatile data structures.

**Visual:**
1. Display the title "Python Lists" in big bold yellow text at the top.
2. Below it, show a list of bullet points appearing one by one:
   - "Ordered"
   - "Mutable"
   - "Allow Duplicates"
3. Use a standard list layout (aligned left, moving down).

---

## Scene: Example - Code Visualization
**Narrative:**
Let's look at how we define a list in code.

**Visual:**
1. Clear the previous scene.
2. Show a code snippet in the center: `my_list = [1, 2, 3]`
3. Draw a box around the code snippet to highlight it.
4. Animate an arrow pointing to the brackets `[]` with the label "Square Brackets".

---

## Tips for Best Results
1. **Keep it Modular:** Break long topics into multiple small scenes.
2. **Be Explicit:** Instead of "Show some math", say "Show the equation E = mc^2 in the center".
3. **Layouts:** The AI is good at standard layouts. Ask for "lists", "grids", or "centered text".
4. **Keywords:** Use Manim keywords if you know them (e.g., "Create a VGroup", "Use Write animation", "FadeIn").
