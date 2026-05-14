"""
ASPICE V-Model Documentation Viewer
Interactive web UI for browsing V-model documentation, requirements, designs, and traceability.
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import re

ROOT_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT_DIR / "viewer" / "templates"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
app.config['JSON_SORT_KEYS'] = False

# Configuration
DOCS_DIR = ROOT_DIR / "docs"
REQUIREMENTS_FILE = DOCS_DIR / "requirements" / "system-requirements.md"
SW_REQUIREMENTS_FILE = DOCS_DIR / "requirements" / "software-requirements.md"
ARCH_FILE = DOCS_DIR / "design" / "system-architecture.md"
VMODEL_FILE = DOCS_DIR / "v-model" / "v-model-overview.md"


class RequirementParser:
    """Parse requirements from markdown tables"""
    
    @staticmethod
    def extract_requirements(content: str) -> List[Dict]:
        """Extract requirements from markdown content"""
        requirements = []
        # Match markdown tables with ID, Requirement, Description, Priority
        table_pattern = r'\|\s*([A-Z\-\d]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([A-Z]+)?\s*\|'
        
        matches = re.finditer(table_pattern, content)
        for match in matches:
            req_id, title, description, priority = match.groups()
            req_id = req_id.strip()
            title = title.strip()
            description = description.strip()
            priority = (priority or "MEDIUM").strip()
            
            # Skip header rows
            if req_id in ["ID", "----"]:
                continue
            
            requirements.append({
                "id": req_id,
                "title": title,
                "description": description,
                "priority": priority,
                "type": "system" if "SYS" in req_id else "software",
                "section": extract_section(content, match.start())
            })
        
        return requirements
    
    @staticmethod
    def extract_traceability(sw_req_content: str, arch_content: str) -> Dict:
        """Extract traceability links between requirements and design"""
        traceability = {}
        
        # Extract SWE-REQ to SYS-REQ mappings
        sys_pattern = r'\*\*([A-Z\-\d]+)\*\*'
        
        # Find all traceability references in design
        for line in arch_content.split('\n'):
            if 'Traceability' in line or 'traceability' in line:
                continue
            
        return traceability


def extract_section(content: str, position: int) -> str:
    """Extract section name before the given position"""
    preceding = content[:position]
    headers = re.findall(r'#+\s+(.+)', preceding)
    return headers[-1] if headers else "General"


def load_markdown_file(filepath: Path) -> str:
    """Load and parse markdown file"""
    if not filepath.exists():
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def extract_mermaid_diagrams(content: str) -> List[Dict]:
    """Extract Mermaid diagrams from markdown"""
    diagrams = []
    pattern = r'```mermaid\n(.*?)\n```'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    for i, match in enumerate(matches):
        diagram_code = match.group(1).strip()
        diagrams.append({
            "id": f"diagram_{i}",
            "code": diagram_code,
            "position": match.start()
        })
    
    return diagrams


def build_requirement_tree() -> Dict:
    """Build hierarchical requirement tree"""
    sys_content = load_markdown_file(REQUIREMENTS_FILE)
    sw_content = load_markdown_file(SW_REQUIREMENTS_FILE)
    
    sys_reqs = RequirementParser.extract_requirements(sys_content)
    sw_reqs = RequirementParser.extract_requirements(sw_content)
    
    tree = {
        "system": {
            "functional": [r for r in sys_reqs if "F" in r["id"]],
            "non_functional": [r for r in sys_reqs if "NF" in r["id"]]
        },
        "software": {
            "input": [r for r in sw_reqs if "I" in r["id"]],
            "depth": [r for r in sw_reqs if "D" in r["id"]],
            "detection": [r for r in sw_reqs if "OD" in r["id"]],
            "distance": [r for r in sw_reqs if "DE" in r["id"]],
            "visualization": [r for r in sw_reqs if "V" in r["id"]],
            "output": [r for r in sw_reqs if "O" in r["id"]],
            "config": [r for r in sw_reqs if "C" in r["id"]],
            "performance": [r for r in sw_reqs if "P" in r["id"]],
            "quality": [r for r in sw_reqs if "Q" in r["id"]],
            "reliability": [r for r in sw_reqs if "R" in r["id"]]
        }
    }
    
    return tree


# Routes

@app.route('/')
def index():
    """Main dashboard with V-model overview"""
    vmodel_content = load_markdown_file(VMODEL_FILE)
    diagrams = extract_mermaid_diagrams(vmodel_content)
    
    return render_template('index.html', 
                         vmodel_content=vmodel_content,
                         diagrams=diagrams)


@app.route('/requirements')
def requirements():
    """Requirements page with SYS-REQ and SWE-REQ"""
    sys_content = load_markdown_file(REQUIREMENTS_FILE)
    sw_content = load_markdown_file(SW_REQUIREMENTS_FILE)
    
    sys_diagrams = extract_mermaid_diagrams(sys_content)
    sw_diagrams = extract_mermaid_diagrams(sw_content)
    
    req_tree = build_requirement_tree()
    
    return render_template('requirements.html',
                         sys_content=sys_content,
                         sw_content=sw_content,
                         sys_diagrams=sys_diagrams,
                         sw_diagrams=sw_diagrams,
                         req_tree=req_tree)


@app.route('/design')
def design():
    """Design page with SWE2 System Architecture and SWE3 Detailed Design"""
    arch_content = load_markdown_file(ARCH_FILE)
    diagrams = extract_mermaid_diagrams(arch_content)
    
    return render_template('design.html',
                         arch_content=arch_content,
                         diagrams=diagrams)


@app.route('/traceability')
def traceability():
    """Traceability matrix page"""
    sys_content = load_markdown_file(REQUIREMENTS_FILE)
    sw_content = load_markdown_file(SW_REQUIREMENTS_FILE)
    arch_content = load_markdown_file(ARCH_FILE)
    
    sys_reqs = RequirementParser.extract_requirements(sys_content)
    sw_reqs = RequirementParser.extract_requirements(sw_content)
    
    # Build traceability matrix
    rtm = []
    for sw_req in sw_reqs:
        # Extract traceability from description (typically contains SYS-* references)
        traced_to = re.findall(r'(SYS-[A-Z\-\d]+)', sw_req['description'] + ' ' + sw_req['title'])
        rtm.append({
            "sw_id": sw_req['id'],
            "sw_title": sw_req['title'],
            "sys_ids": list(set(traced_to)) if traced_to else [],
            "priority": sw_req['priority']
        })
    
    return render_template('traceability.html',
                         sys_reqs=sys_reqs,
                         sw_reqs=sw_reqs,
                         rtm=rtm)


@app.route('/api/requirement/<req_id>')
def get_requirement(req_id):
    """API endpoint to get requirement details"""
    sys_content = load_markdown_file(REQUIREMENTS_FILE)
    sw_content = load_markdown_file(SW_REQUIREMENTS_FILE)
    
    content = sys_content if "SYS" in req_id else sw_content
    reqs = RequirementParser.extract_requirements(content)
    
    for req in reqs:
        if req['id'] == req_id:
            return jsonify(req)
    
    return jsonify({"error": "Requirement not found"}), 404


@app.route('/api/requirements/summary')
def get_requirements_summary():
    """API endpoint for requirements statistics"""
    sys_content = load_markdown_file(REQUIREMENTS_FILE)
    sw_content = load_markdown_file(SW_REQUIREMENTS_FILE)
    
    sys_reqs = RequirementParser.extract_requirements(sys_content)
    sw_reqs = RequirementParser.extract_requirements(sw_content)
    
    summary = {
        "system": {
            "total": len(sys_reqs),
            "high": len([r for r in sys_reqs if r['priority'] == 'HIGH']),
            "medium": len([r for r in sys_reqs if r['priority'] == 'MEDIUM']),
            "low": len([r for r in sys_reqs if r['priority'] == 'LOW'])
        },
        "software": {
            "total": len(sw_reqs),
            "high": len([r for r in sw_reqs if r['priority'] == 'HIGH']),
            "medium": len([r for r in sw_reqs if r['priority'] == 'MEDIUM']),
            "low": len([r for r in sw_reqs if r['priority'] == 'LOW'])
        }
    }
    
    return jsonify(summary)


@app.template_filter('markdown_to_html')
def markdown_to_html(text):
    """Convert markdown to HTML (basic conversion)"""
    # This is a simple converter; consider using python-markdown for production
    import re
    
    # Headers
    text = re.sub(r'# (.*?)(?:\n|$)', r'<h1>\1</h1>', text)
    text = re.sub(r'## (.*?)(?:\n|$)', r'<h2>\1</h2>', text)
    text = re.sub(r'### (.*?)(?:\n|$)', r'<h3>\1</h3>', text)
    text = re.sub(r'#### (.*?)(?:\n|$)', r'<h4>\1</h4>', text)
    
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
    
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    
    # Code
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    
    # Links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    
    return text


if __name__ == '__main__':
    print("Starting ASPICE V-Model Viewer...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='localhost', port=5000)
