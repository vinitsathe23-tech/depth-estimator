# Quick Start: ASPICE V-Model Viewer 🚀

## Agent Rule Before Changes

Before any agent modifies this project, it must perform impact analysis and give the user an overview of affected files, requirements, traceability, risks, and proposed steps. See [AGENTS.md](AGENTS.md) and [CHANGE_IMPACT_ANALYSIS.md](docs/aspice/CHANGE_IMPACT_ANALYSIS.md).

## Get Started in 3 Steps

### Step 1️⃣: Install Flask
```bash
pip install -r requirements/viewer.txt
```

### Step 2️⃣: Start the Viewer
```bash
python app/v_model_viewer.py
```

### Step 3️⃣: Open Browser
```
http://localhost:5000
```

**Done!** You now have an interactive V-Model explorer. 🎉

---

## What You'll See

### 🏠 **Home Page** (Overview)
- V-Model lifecycle diagram
- Requirements statistics
- Quick navigation buttons
- Key principles explained

### 📋 **Requirements Tab**
- Browse all System Requirements (SYS-REQ) - 17 total
- Browse all Software Requirements (SWE-REQ) - 43 total
- Filter by category:
  - Input, Depth Estimation, Object Detection
  - Distance Estimation, Visualization, Output
  - Configuration & CLI
- Color-coded by priority (HIGH/MEDIUM/LOW)

### 🏗️ **Design Tab**
- System Architecture diagram (SWE2)
- Component details (SWE3)
- Depth Estimator backends comparison
- Object Detector backends comparison
- Data flow sequence
- Design patterns:
  - Strategy, Factory, State, Observer

### 🔗 **Traceability Tab**
- Requirements Traceability Matrix
- Software-to-System mapping
- Coverage statistics
- Orphaned requirement detection

---

## What Was Created

```
✅ docs/
   ├── v-model/v-model-overview.md          - V-Model documentation
   ├── requirements/
   │   ├── system-requirements.md           - 17 SYS-REQ
   │   └── software-requirements.md         - 43 SWE-REQ
   ├── design/
   │   └── system-architecture.md           - SWE2 & SWE3
   ├── traceability/
   │   └── requirements-traceability-matrix.md
   └── verification/
       ├── test-plan.md
       └── acceptance-criteria.md

✅ app/v_model_viewer.py                    - Flask web app
✅ viewer/templates/
   ├── base.html                           - Base template
   ├── index.html                          - Homepage
   ├── requirements.html                   - Requirements browser
   ├── design.html                         - Design viewer
   └── traceability.html                   - Traceability matrix

✅ requirements/viewer.txt                  - Dependencies
✅ docs/aspice/ASPICE_IMPLEMENTATION_GUIDE.md - Full documentation
✅ viewer/README.md                         - Detailed instructions
```

---

## Features

| Feature | Details |
|---------|---------|
| 📊 **Mermaid Diagrams** | V-Model, architecture, data flow visualizations |
| 🎨 **Beautiful UI** | Modern design with color-coded priorities |
| 🔗 **Full Traceability** | Requirements → Design → Code mapping |
| 📱 **Responsive** | Works on desktop, tablet, mobile |
| ⚡ **Zero Maintenance** | Markdown-based, no database |
| 🎯 **ASPICE Compliant** | Follows automotive SPICE standards |
| 📈 **60 Requirements** | 17 system + 43 software requirements |
| 🏛️ **Architecture** | Modular design with 6+ components |

---

## Example Navigation

### I want to see all HIGH priority requirements
1. Go to **Requirements tab**
2. Look for red **HIGH** badges
3. Click on any requirement to see details

### I want to understand the system architecture
1. Go to **Design tab**
2. View "System Architecture Diagram"
3. Explore "Component Details"
4. Check "Design Patterns Applied"

### I want to verify traceability
1. Go to **Traceability tab**
2. See SWE-REQ to SYS-REQ mapping
3. Check coverage percentage
4. Look for any red "NOT TRACED" warnings

### I want to understand each phase
1. Go to **Home page**
2. Click tabs: "Left Side: Definition" or "Right Side: Verification"
3. Read descriptions of each phase

---

## V-Model at a Glance

```
Definition (Top)          Verification (Bottom)
─────────────────         ──────────────────
    REQ                       VAL (Accept)
     ↓                           ↑
    SWE2 (Design)             SWE6 (System Test)
     ↓                           ↑
    SWE3 (Detail)             SWE5 (Integration)
     ↓                           ↑
   SWE4 (Code)               Unit Tests
```

---

## Requirements Summary

| Category | Functional | Non-Functional | Total |
|----------|-----------|-----------------|-------|
| **System (SYS)** | 8 | 8 | 16 |
| **Software (SWE)** | 35 | 8 | 43 |
| **Total** | 43 | 16 | 59 |

### Priority Distribution
- 🔴 **HIGH**: 36 requirements (61%)
- 🟡 **MEDIUM**: 20 requirements (34%)
- 🟢 **LOW**: 4 requirements (5%)

---

## Keyboard Shortcuts (Browser)

| Key | Action |
|-----|--------|
| `Ctrl+F` | Search page |
| `Home` | Go to overview |
| Click tabs | Switch sections |
| Click requirement IDs | Jump to details |

---

## Troubleshooting

### ❌ Port 5000 Already in Use
Edit `app/v_model_viewer.py`, change port to 5001:
```python
app.run(debug=True, host='localhost', port=5001)
```

### ❌ Documentation Not Showing
Ensure these files exist:
- `docs/v-model/v-model-overview.md`
- `docs/requirements/system-requirements.md`
- `docs/requirements/software-requirements.md`
- `docs/design/system-architecture.md`

### ❌ Diagrams Not Rendering
Refresh page (Ctrl+R). Mermaid diagrams load from CDN.

### ❌ Flask Not Starting
Install dependencies:
```bash
pip install -r requirements/viewer.txt
```

---

## Next Steps

1. **Explore the Requirements**
   - See what the system must do
   - Understand software subsystems
   - Check priorities and status

2. **Review the Design**
   - Understand the architecture
   - See how components interact
   - Learn the design patterns

3. **Check Traceability**
   - Verify complete coverage
   - See requirement mapping
   - Validate design alignment

4. **Add More Requirements** (Optional)
   - Edit markdown files in `docs/`
   - Viewer auto-refreshes

5. **Share with Stakeholders**
   - They can view at `http://localhost:5000`
   - Beautiful, easy-to-understand UI
   - No installation needed for viewers

---

## Resources

📄 **Full Guides**:
- [ASPICE Implementation Guide](docs/aspice/ASPICE_IMPLEMENTATION_GUIDE.md)
- [V-Model Viewer README](viewer/README.md)

📚 **Documentation**:
- [V-Model Overview](docs/v-model/v-model-overview.md)
- [System Requirements](docs/requirements/system-requirements.md)
- [Software Requirements](docs/requirements/software-requirements.md)
- [System Architecture](docs/design/system-architecture.md)

---

## Success Checklist

- ✅ Flask installed (`pip install -r requirements/viewer.txt`)
- ✅ Viewer running (`python app/v_model_viewer.py`)
- ✅ Browser opened to `http://localhost:5000`
- ✅ Home page shows V-Model diagram
- ✅ Requirements tab shows 60 requirements
- ✅ Design tab shows architecture diagrams
- ✅ Traceability tab shows RTM with 100% coverage

**All set!** 🎉 You have a complete ASPICE V-Model system with interactive documentation and traceability!

---

**Last Updated**: May 2026  
**Status**: Ready to Use  
**Questions?** Check the full guides above
