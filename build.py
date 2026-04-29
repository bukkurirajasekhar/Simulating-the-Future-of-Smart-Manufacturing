import re

with open('presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the NAV buttons to standard links
nav_replacements = {
    """<button class="active" onclick="show('home')">Home</button>""": """<a href="index.html" class="nav-btn">Home</a>""",
    """<button onclick="show('home')">Home</button>""": """<a href="index.html" class="nav-btn">Home</a>""",
    """<button onclick="show('problem')">Problem</button>""": """<a href="problem.html" class="nav-btn">Problem</a>""",
    """<button onclick="show('objectives')">Objectives</button>""": """<a href="objectives.html" class="nav-btn">Objectives</a>""",
    """<button onclick="show('architecture')">Architecture</button>""": """<a href="architecture.html" class="nav-btn">Architecture</a>""",
    """<button onclick="show('simulation')">Live Demo</button>""": """<a href="simulation.html" class="nav-btn">Live Demo</a>""",
    """<button onclick="show('results')">Results & ROI</button>""": """<a href="results.html" class="nav-btn">Results & ROI</a>""",
    """<button onclick="show('tech')">Tech Stack</button>""": """<a href="tech.html" class="nav-btn">Tech Stack</a>""",
    """<button onclick="show('ai-guide')" style="color: var(--accent-purple); background: rgba(175, 82, 222, 0.1);">🧠 AI Guide</button>""": """<a href="ai-guide.html" class="nav-btn ai-btn">🧠 AI Guide</a>"""
}

# 2. Add some CSS for the new A tags
css_addition = """
  /* Styles for new A tag links */
  nav a.nav-btn {
    text-decoration: none;
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 10px 18px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  }
  nav a.nav-btn:hover, nav a.nav-btn.active {
    color: var(--text-main);
    background: rgba(0, 0, 0, 0.05);
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  }
  body.dark-mode nav a.nav-btn:hover, body.dark-mode nav a.nav-btn.active {
    background: rgba(255, 255, 255, 0.1);
  }
  nav a.ai-btn { color: var(--accent-purple) !important; background: rgba(175, 82, 222, 0.1) !important; }
"""
html = html.replace("/* ── SECTIONS ── */", css_addition + "\n  /* ── SECTIONS ── */")

# Remove "display: none" from sections
html = html.replace(".section {\n    display: none;", ".section {\n    display: block;")

for old, new in nav_replacements.items():
    html = html.replace(old, new)

# 3. Add localStorage to theme toggle
old_toggle = """function toggleDarkMode() {
  const body = document.body;
  const toggleBtn = document.querySelector('.theme-toggle');
  
  if (isDarkMode) {
    body.classList.remove('dark-mode');
    toggleBtn.textContent = '🌙';
    isDarkMode = false;
  } else {
    body.classList.add('dark-mode');
    toggleBtn.textContent = '☀️';
    isDarkMode = true;
  }
  
  if(oeeChartInstance) updateChartTheme();
}"""

new_toggle = """
// Check local storage on load
if(localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
    isDarkMode = true;
    document.addEventListener("DOMContentLoaded", () => {
        const toggleBtn = document.querySelector('.theme-toggle');
        if(toggleBtn) toggleBtn.textContent = '☀️';
    });
}

function toggleDarkMode() {
  const body = document.body;
  const toggleBtn = document.querySelector('.theme-toggle');
  
  if (isDarkMode) {
    body.classList.remove('dark-mode');
    toggleBtn.textContent = '🌙';
    isDarkMode = false;
    localStorage.setItem('theme', 'light');
  } else {
    body.classList.add('dark-mode');
    toggleBtn.textContent = '☀️';
    isDarkMode = true;
    localStorage.setItem('theme', 'dark');
  }
  
  if(typeof oeeChartInstance !== 'undefined' && oeeChartInstance) updateChartTheme();
}"""
html = html.replace(old_toggle, new_toggle)

# 4. Remove `nav button` css since we use `nav a` now
html = re.sub(r'nav button \{.*?\}', '', html, flags=re.DOTALL)
html = re.sub(r'nav button:hover.*?\}', '', html, flags=re.DOTALL)
html = re.sub(r'body\.dark-mode nav button:hover.*?\}', '', html, flags=re.DOTALL)

# 5. Extract sections
sections = ['home', 'problem', 'objectives', 'architecture', 'simulation', 'results', 'tech', 'ai-guide']
files = ['index.html', 'problem.html', 'objectives.html', 'architecture.html', 'simulation.html', 'results.html', 'tech.html', 'ai-guide.html']

for target_id, target_file in zip(sections, files):
    new_html = html
    
    # Active state for nav link
    if target_file == 'ai-guide.html':
        active_str = f'href="{target_file}" class="nav-btn ai-btn"'
        new_html = new_html.replace(active_str, f'href="{target_file}" class="nav-btn ai-btn active"')
    else:
        active_str = f'href="{target_file}" class="nav-btn"'
        new_html = new_html.replace(active_str, f'href="{target_file}" class="nav-btn active"')
    
    # Remove all sections EXCEPT the target section
    for s in sections:
        if s != target_id:
            # We use non-greedy matching .*?
            pattern = re.compile(rf'<!-- ══.*?══ -->\s*<section id="{s}".*?</section>', re.DOTALL)
            new_html = re.sub(pattern, '', new_html)
            
    # Modify simulation init logic
    if target_id == 'simulation':
        new_html = new_html.replace("window.onload = startCycle;", "window.onload = () => { startCycle(); initChart(); };")
    
    with open(target_file, 'w', encoding='utf-8') as out:
        out.write(new_html)

print("Generated all 8 files successfully!")
