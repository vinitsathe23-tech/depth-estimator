# ASPICE V-Model Documentation Viewer

An interactive web-based UI for browsing and exploring your ASPICE V-Model documentation, requirements, designs, and traceability matrix.

## Features

✨ **Interactive V-Model Visualization**
- Visual V-Model diagram with Mermaid
- Navigate through all lifecycle phases
- Understand relationships between phases

📋 **Requirements Management**
- Browse System Requirements (SYS-REQ)
- Browse Software Requirements (SWE-REQ)
- Filter by priority, category, and type
- View requirement details

🏗️ **Design Documentation**
- System Architecture (SWE2)
- Detailed Component Design (SWE3)
- Data flow diagrams
- Design pattern explanations

🔗 **Traceability Matrix**
- Requirements-to-Design mapping
- Requirements-to-Code traceability
- Design-to-Test relationships
- Orphaned requirement detection

🎨 **Beautiful UI**
- Modern responsive design
- Dark/light mode ready
- Tab-based navigation
- Mermaid diagram rendering
- Syntax highlighting

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup

1. **Install Flask dependencies:**
```bash
pip install -r requirements/viewer.txt
```

2. **Ensure documentation exists:**
The viewer expects these files:
```
docs/
├── v-model/v-model-overview.md
├── requirements/
│   ├── system-requirements.md
│   └── software-requirements.md
└── design/
    └── system-architecture.md
```

## Usage

### Start the Viewer

```bash
python app/v_model_viewer.py
```

Output:
```
Starting ASPICE V-Model Viewer...
Open http://localhost:5000 in your browser
```

### Access the UI

Open your browser and navigate to:
```
http://localhost:5000
```

## Navigation

### Home / Overview
- V-Model diagram with all phases
- Requirements summary statistics
- Quick navigation to other sections
- Key principles explanation

### Requirements Page
Tabs for:
- System Functional Requirements (SYS-F)
- System Non-Functional Requirements (SYS-NF)
- Software Requirements by category:
  - Input Management (SWE-F-I)
  - Depth Estimation (SWE-F-D)
  - Object Detection (SWE-F-OD)
  - Distance Estimation (SWE-F-DE)
  - Visualization (SWE-F-V)
  - Data Output (SWE-F-O)
  - Configuration (SWE-F-C)

Each requirement shows:
- Requirement ID (e.g., SYS-F-001)
- Title and description
- Priority (HIGH/MEDIUM/LOW)
- Section information

### Design Page
Tabs for:
- System Design Overview (SWE2)
- System Architecture Diagram
- Component Details (SWE3)
  - Depth Estimator backends comparison
  - Object Detector backends comparison
  - Detection object structure
  - Calibration engine model
- Data Flow Sequence Diagram
- Design Patterns Applied
  - Strategy Pattern
  - Factory Pattern
  - State Pattern
  - Observer Pattern

### Traceability Page
- Requirements Traceability Matrix (RTM)
- Visual traceability flow diagram
- Software-to-System requirement mapping
- Coverage statistics
- Orphaned requirement detection

## API Endpoints

The viewer also provides REST APIs:

### Get Requirement Summary
```
GET /api/requirements/summary
```
Returns:
```json
{
  "system": {
    "total": 17,
    "high": 8,
    "medium": 5,
    "low": 4
  },
  "software": {
    "total": 43,
    "high": 28,
    "medium": 15,
    "low": 0
  }
}
```

### Get Specific Requirement
```
GET /api/requirement/<REQ_ID>
```
Example: `/api/requirement/SYS-F-001`

Returns requirement details in JSON format.

## Configuration

The application automatically discovers:
- Documentation files in `docs/` directory
- Markdown files in requirements and design subdirectories
- Mermaid diagrams embedded in markdown

No additional configuration needed!

## Customization

### Adding New Requirement Categories

1. Add new markdown table in `docs/requirements/software-requirements.md`
2. Update the `RequirementParser` to extract new category
3. Add new tab in `viewer/templates/requirements.html`

### Modifying Design Pages

1. Edit design documentation in `docs/design/`
2. Add new diagrams or content
3. Create new tabs in `viewer/templates/design.html`

### Styling

Edit CSS in `viewer/templates/base.html`:
- Header colors: `header` style
- Tab styling: `.tab` and `.tab.active`
- Requirement cards: `.requirement-card`
- Priority badges: `.priority-high`, `.priority-medium`, `.priority-low`

## Architecture

### Backend (Flask)
- `app/v_model_viewer.py`: Main Flask application
- Routes for each major section
- Markdown parsing and extraction
- Mermaid diagram extraction

### Frontend (HTML/CSS/JavaScript)
- `viewer/templates/base.html`: Base template with styling
- `viewer/templates/index.html`: Homepage and V-model overview
- `viewer/templates/requirements.html`: Requirements browser
- `viewer/templates/design.html`: Design documentation
- `viewer/templates/traceability.html`: Traceability matrix

### Data Processing
- `RequirementParser`: Extracts requirements from markdown tables
- `extract_mermaid_diagrams()`: Extracts Mermaid diagrams for rendering
- `extract_section()`: Identifies section headers for organization

## Troubleshooting

### Port 5000 Already in Use
Change the port in `app/v_model_viewer.py`:
```python
app.run(debug=True, host='localhost', port=5001)
```

### Markdown Not Rendering
Ensure markdown files are in `docs/` subdirectories with correct names:
- `docs/v-model/v-model-overview.md`
- `docs/requirements/system-requirements.md`
- `docs/requirements/software-requirements.md`
- `docs/design/system-architecture.md`

### Diagrams Not Showing
The viewer uses Mermaid.js CDN. Ensure internet connection is available.
Mermaid diagrams must be in markdown code blocks:
````
```mermaid
graph TD
  A --> B
```
````

## Performance

- Markdown parsing: One-time on app startup
- Diagram rendering: Client-side (browser)
- No database required
- Minimal memory footprint

## Future Enhancements

- [ ] Full-text search across documentation
- [ ] Advanced filtering and sorting
- [ ] Export traceability matrix to Excel
- [ ] Real-time documentation updates
- [ ] User annotations and notes
- [ ] Version history and change tracking
- [ ] PDF export of selected sections
- [ ] Dark mode toggle
- [ ] Code snippet integration
- [ ] Test case viewer

## License

Part of Monocular Depth Sandbox project.

## Support

For issues or questions:
1. Check documentation in `docs/`
2. Review markdown formatting in source files
3. Check browser console for JavaScript errors
4. Verify Flask is running on correct port

---

**Version**: 1.0  
**Last Updated**: May 2026  
**Status**: Active
