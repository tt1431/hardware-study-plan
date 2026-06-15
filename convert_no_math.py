#!/usr/bin/env python3
"""
Convert markdown notes with LaTeX math to plain-text-readable versions.
Strips $...$ / $$...$$ and converts common LaTeX constructs.
"""
import re, os

NOTES_DIR = os.path.join(os.path.dirname(__file__), 'notes')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'notes_plain')
os.makedirs(OUT_DIR, exist_ok=True)

def convert_simple_frac(m):
    """Convert \frac{a}{b} to a/b"""
    return m.group(1) + '/' + m.group(2)

def convert_sqrt(m):
    return 'sqrt(' + m.group(1) + ')'

def replace_math(text):
    # Remove display math $$...$$ - treat as block
    text = re.sub(r'\$\$(.*?)\$\$', lambda m: replace_inline_math(m.group(1).strip()), text, flags=re.DOTALL)
    # Inline math $...$
    text = re.sub(r'\$(.*?)\$', lambda m: replace_inline_math(m.group(1)), text)
    return text

def replace_inline_math(s):
    # Remove \displaystyle
    s = re.sub(r'\\displaystyle\s*', '', s)
    # Remove \text{...}
    s = re.sub(r'\\text\{([^}]*)\}', r'\1', s)
    # Remove \mathrm{...}
    s = re.sub(r'\\mathrm\{([^}]*)\}', r'\1', s)
    # \textbf{...} / \textit{...} / \emph{...}
    s = re.sub(r'\\textbf\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\textit\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\emph\{([^}]*)\}', r'\1', s)
    # \frac{a}{b}
    s = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', convert_simple_frac, s)
    # \sqrt{x}
    s = re.sub(r'\\sqrt\{([^}]*)\}', convert_sqrt, s)
    # \times
    s = s.replace('\\times', 'x')
    # \approx
    s = s.replace('\\approx', '≈')
    # \rightarrow → \Rightarrow → \Longrightarrow →
    s = s.replace('\\rightarrow', '→')
    s = s.replace('\\Rightarrow', '⇒')
    s = s.replace('\\Longrightarrow', '⇒')
    # \leftarrow
    s = s.replace('\\leftarrow', '←')
    # \cdot
    s = s.replace('\\cdot', '·')
    # \cdots
    s = s.replace('\\cdots', '...')
    # \propto
    s = s.replace('\\propto', '∝')
    # \infty
    s = s.replace('\\infty', '∞')
    # \ne
    s = s.replace('\\ne', '≠')
    # \ge / \le
    s = s.replace('\\ge', '≥')
    s = s.replace('\\le', '≤')
    # Greek letters
    s = s.replace('\\Gamma', 'Γ')
    s = s.replace('\\varepsilon', 'ε')
    s = s.replace('\\pi', 'π')
    s = s.replace('\\omega', 'ω')
    s = s.replace('\\Omega', 'Ω')
    # Handle \left(, \right) etc. BEFORE general backslash removal
    s = re.sub(r'\\left\s*\(', '(', s)
    s = re.sub(r'\\right\s*\)', ')', s)
    s = re.sub(r'\\left\s*\[', '[', s)
    s = re.sub(r'\\right\s*\]', ']', s)
    s = re.sub(r'\\left\s*\{', '{', s)
    s = re.sub(r'\\right\s*\}', '}', s)
    s = re.sub(r'\\left\s*\.', '', s)  # fallback for \left.<char>
    # Handle \ followed by space (LaTeX space escape)
    s = re.sub(r'\\(?=\s)', '', s)
    # \; and \, spacing
    s = s.replace('\\;', ' ')
    s = s.replace('\\,', ' ')
    s = re.sub(r'\\(\w+)\b', lambda m: m.group(1), s)  # remove backslash from remaining commands
    # Remove extra braces
    s = re.sub(r'\{(\d+)\}', r'\1', s)
    # Clean up: remove double spaces
    s = re.sub(r'  +', ' ', s)
    return s

def convert_table_row(row):
    """Handle tables - they may contain pipes in markdown tables but not needed for plain text"""
    return row

def process_file(filename):
    path = os.path.join(NOTES_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace math
    converted = replace_math(content)
    
    out_path = os.path.join(OUT_DIR, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    original_math = content.count('$')
    remaining_math = converted.count('$')
    print(f"  {filename}: {original_math} math markers → {remaining_math} remaining")
    return out_path

if __name__ == '__main__':
    files = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith('.md'))
    print("Processing files...")
    for fname in files:
        out = process_file(fname)
    print(f"\nDone! Plain-text notes saved to: {OUT_DIR}")
