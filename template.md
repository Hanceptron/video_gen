# Manimator Script Generation Template

**INSTRUCTIONS FOR THE AI SCRIPTWRITER:**
You are generating a script for "Manimator", a tool that converts Markdown into Python/Manim animations.
Your output must follow the **Strict Format** below. The "Visual" descriptions are the most important part—they must be literal, geometric, and specific.

---

## Strict Format Rules
1.  Each scene must start with `## Scene: [Name]`.
2.  **Narrative:** Write the voiceover text. Keep it concise (approx. 20-40 words per scene).
3.  **Visual:** Write a numbered list of instructions.

## How to Write "Visual" Instructions (CRITICAL)
The Animation AI is literal. It does not know what abstract concepts look like.
*   **BAD:** "Show the concept of inflation." (The AI will fail or just write the word "Inflation")
*   **GOOD:** "Show a balloon labeled 'Prices' growing larger and turning red."

*   **BAD:** "Draw a Blockchain."
*   **GOOD:** "Draw 3 squares horizontally aligned. Connect them with lines. Label them 'Block 1', 'Block 2', 'Block 3'."

*   **BAD:** "Show a server."
*   **GOOD:** "Draw a grey rectangle with small blinking lights (circles) on the front."

*   **Layouts:** Explicitly ask for "Grid layout", "List layout", or "Centered".

---

## Template (Copy and Fill)

```markdown
# [Video Title]

[Brief description of the video topic]

---

## Scene: [Scene Name]
**Narrative:**
[Voiceover text here...]

**Visual:**
1. [Step 1: Clear screen or keep previous?]
2. [Step 2: Describe object 1 (Shape, Color, Text, Position)]
3. [Step 3: Describe animation (FadeIn, Write, Grow, Move)]
4. [Step 4: Describe layout (e.g., "Arrange these items in a row")]

---
```

## Example Output

```markdown
# Understanding RAM vs Disk

---

## Scene: Introduction
**Narrative:**
Your computer has two types of memory. RAM is fast but temporary, while the Hard Disk is slow but permanent.

**Visual:**
1. Split the screen into two halves (Left and Right).
2. On the LEFT, draw a green square labeled "RAM". Above it, show text "Fast & Temporary".
3. On the RIGHT, draw a grey cylinder labeled "Disk". Above it, show text "Slow & Permanent".
4. Animate them appearing one by one.

---

## Scene: The Data Flow
**Narrative:**
When you open a program, data moves from the slow disk into the fast RAM so the CPU can use it.

**Visual:**
1. Keep the RAM and Disk from the previous scene.
2. Draw a small circle labeled "Data" inside the "Disk".
3. Animate the "Data" circle moving from the Disk to the RAM.
4. Make the RAM glow yellow when the data arrives.
```
