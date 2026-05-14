# ASPICE V-Model Complete Implementation Guide

**Project**: Monocular Depth Sandbox  
**Compliance**: ASPICE (Automotive SPICE) V-Model  
**Version**: 1.0  
**Date**: May 2026  
**Status**: Active

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Running the V-Model Viewer](#running-the-v-model-viewer)
4. [Documentation Files](#documentation-files)
5. [V-Model Phases](#v-model-phases)
6. [Traceability](#traceability)
7. [Quick Start](#quick-start)

---

## Overview

This project is now **ASPICE-compliant** with a complete V-Model implementation including:

✅ **System Requirements** (SYS-REQ) - Generic, system-level requirements  
✅ **Software Requirements** (SWE-REQ) - Detailed software specifications  
✅ **System Design** (SWE2) - High-level architecture using Mermaid diagrams  
✅ **Detailed Design** (SWE3) - Component-level design specifications  
✅ **Full Traceability** - Requirements → Design → Code → Tests  
✅ **Interactive Web UI** - Python Flask-based V-Model viewer

---

## Project Structure

```
monocular-depth-sandbox/
├── docs/
│   ├── README.md
│   ├── v-model/
│   │   └── v-model-overview.md          ← V-Model lifecycle
│   ├── requirements/
│   │   ├── system-requirements.md       ← SYS-REQ (17 requirements)
│   │   └── software-requirements.md     ← SWE-REQ (43 requirements)
│   ├── design/
│   │   └── system-architecture.md       ← SWE2 & SWE3 design
│   ├── traceability/
│   │   └── requirements-traceability-matrix.md
│   └── verification/
│       ├── test-plan.md
│       └── acceptance-criteria.md
├── app/
│   └── v_model_viewer.py                ← Flask web app for UI
├── viewer/
│   ├── README.md                        ← How to run the viewer
│   └── templates/                       ← Viewer templates
├── requirements/
│   └── viewer.txt                       ← Flask dependencies
└── [other project files...]
```

---

## Running the V-Model Viewer

### Step 1: Install Flask Dependencies
```bash
pip install -r requirements/viewer.txt
```

### Step 2: Start the Viewer
```bash
python app/v_model_viewer.py
```

Expected output:
```
Starting ASPICE V-Model Viewer...
Open http://localhost:5000 in your browser
```

### Step 3: Open Browser
Navigate to: `http://localhost:5000`

### Step 4: Explore
- **Homepage**: V-Model overview with diagrams and requirements summary
- **Requirements Tab**: Browse all SYS-REQ and SWE-REQ
- **Design Tab**: View architecture and component design with Mermaid diagrams
- **Traceability Tab**: See how requirements map to design and code

---

## Documentation Files

### 1. docs/v-model/v-model-overview.md
**Purpose**: Comprehensive V-Model documentation

**Contents**:
- V-Model architecture diagram
- Phase descriptions (left side: definition, right side: verification)
- Traceability flow explanation
- ASPICE alignment information

**Key Sections**:
- Requirements Analysis (REQ)
- System Design (SWE2)
- Detailed Design (SWE3)
- Implementation (SWE4)
- Unit Testing
- Integration Testing (SWE5)
- System Testing (SWE6)
- Acceptance Testing (VAL)

### 2. docs/requirements/system-requirements.md
**Document ID**: SYS-REQ-001  
**Type**: System-Level Requirements

**Contents**:
- 8 Functional Requirements (SYS-F-001 to SYS-F-008)
- 8 Non-Functional Requirements (SYS-NF-001 to SYS-NF-008)
- Quality attributes (Performance, Reliability, Usability, Maintainability)
- Use cases
- Risk assessment
- Constraints and dependencies

**Requirement Categories**:
- Video Input Support
- Depth Estimation
- Object Detection
- Distance Calibration
- Position Estimation
- Real-Time Visualization
- Output Export
- Configuration Management

### 3. docs/requirements/software-requirements.md
**Document ID**: SWE-REQ-001  
**Type**: Software-Level Requirements

**Contents**:
- 43 Software Requirements organized by subsystem
- Performance requirements
- Code quality requirements
- Reliability requirements

**Categories** (7 sections):
1. **Input Management (SWE-REQ-I)**: 5 requirements
2. **Depth Estimation (SWE-REQ-D)**: 6 requirements
3. **Object Detection (SWE-REQ-OD)**: 6 requirements
4. **Distance Estimation (SWE-REQ-DE)**: 6 requirements
5. **Visualization (SWE-REQ-V)**: 7 requirements
6. **Data Output (SWE-REQ-O)**: 4 requirements
7. **Configuration & CLI (SWE-REQ-C)**: 5 requirements

**All requirements traced to SYS-REQ** for complete traceability!

### 4. docs/design/system-architecture.md
**Document ID**: SWE2-ARCH-001  
**Type**: System Design (SWE2) & Detailed Design (SWE3)

**Contents**:
- System architecture diagram (Mermaid)
- Component descriptions:
  - Input Layer (FrameCapture)
  - Processing Components (DepthEstimator, ObjectDetector, CalibrationEngine)
  - State Management (Configuration, Calibration State)
  - Output Layer (Visualizer, DataExporter)
- Data flow sequence diagram
- Design patterns (Strategy, Factory, State, Observer)
- Integration points
- Quality attributes

**Key Subsystems**:
- **FrameCapture**: Unified video source interface
- **DepthEstimator**: Pluggable depth backends (Pseudo-Depth, Depth Anything v2)
- **ObjectDetector**: Pluggable detection backends (Depth-Blob, YOLO)
- **CalibrationEngine**: One-point calibration system
- **PositionEstimator**: 3D coordinate calculation
- **Visualizer**: 3-panel real-time display
- **DataExporter**: Output in frames, CSV, JSON, MP4

---

## V-Model Phases

### Left Side: Definition (Top → Bottom)

```
    ↓ Requirements Analysis (REQ)
    ↓ System Design (SWE2)
    ↓ Detailed Design (SWE3)
    ↓ Implementation (SWE4)
```

### Right Side: Verification (Bottom → Top)

```
    ↑ Unit Testing
    ↑ Integration Testing (SWE5)
    ↑ System Testing (SWE6)
    ↑ Acceptance Testing (VAL)
```

### Traceability Flow

```
Requirements (SYS-REQ)
    ↓ decomposed into
Software Requirements (SWE-REQ)
    ↓ designed in
System Architecture (SWE2)
    ↓ refined by
Component Design (SWE3)
    ↓ implemented in
Source Code (SWE4)
    ↓ verified by
Unit Tests → Integration Tests → System Tests → Acceptance Tests
    ↓ validates back to
Requirements (SYS-REQ)
```

---

## Traceability

### Requirements Coverage

| Type | Total | High Priority | Medium Priority | Low Priority |
|------|-------|---------------|-----------------|--------------|
| **System Requirements (SYS-REQ)** | 17 | 8 | 5 | 4 |
| **Software Requirements (SWE-REQ)** | 43 | 28 | 15 | 0 |
| **Total** | 60 | 36 | 20 | 4 |

### Traceability Matrix

**All SWE-REQ items are traced to SYS-REQ** demonstrating:
- Complete requirement coverage
- No orphaned requirements
- Clear impact analysis

### Example Traceability

```
SYS-F-002: Depth Estimation
    ↓ traced to
SWE-F-D-001: Implement pseudo-depth backend
SWE-F-D-002: Implement AI-based depth backend
SWE-F-D-003: Load and cache depth model
    ↓ designed in
SWE2: DepthEstimator component
    ↓ detailed in
SWE3: DepthEstimator abstract class, backends
    ↓ implemented in
app/depth_sandbox.py: DepthEstimator classes
```

---

## Quick Start Workflow

### For Requirements Analysis

1. Open browser: `http://localhost:5000`
2. Go to **Requirements** tab
3. Browse System Requirements (SYS-REQ)
4. Review Software Requirements (SWE-REQ)
5. Check **Traceability** tab to see mapping

### For Design Review

1. Go to **Design** tab
2. View System Architecture diagram (SWE2)
3. Explore Component Details (SWE3)
4. Review Data Flow Sequence
5. Check Design Patterns Applied

### For Traceability Analysis

1. Go to **Traceability** tab
2. View Requirements Traceability Matrix
3. Check coverage statistics
4. Identify any orphaned requirements (if any)

### For Stakeholder Review

1. Share V-Model viewer URL with stakeholders
2. They can navigate and explore all documentation
3. Requirements are color-coded by priority
4. Diagrams provide visual understanding
5. No additional tools needed (web-based)

---

## Key Features

### 🎨 Beautiful UI
- Modern, responsive design
- Tab-based navigation
- Color-coded priority levels
- Interactive diagrams

### 📊 Mermaid Diagrams
- V-Model lifecycle visualization
- System architecture diagram
- Data flow sequence diagram
- Traceability flow diagram
- All diagrams embedded in markdown

### 🔍 Full Traceability
- Requirement-to-requirement mapping
- Requirement-to-design relationships
- Design pattern documentation
- Orphaned requirement detection

### 📱 Responsive Design
- Works on desktop, tablet, mobile
- Mobile-friendly navigation
- Readable on all screen sizes

### ⚡ Zero Maintenance
- No database required
- Markdown-based documentation
- Python Flask (lightweight)
- Easy to version control

---

## Adding New Requirements

### Step 1: Edit Markdown File

Open `docs/requirements/software-requirements.md` and add to the appropriate table:

```markdown
| **SWE-F-NEW-001** | New Requirement | Requirement description | HIGH |
```

### Step 2: Ensure Traceability

Include traceability reference in description:
```markdown
| **SWE-F-NEW-001** | New Requirement | Description (SYS-F-XXX) | HIGH |
```

### Step 3: Reload Viewer

Refresh the browser - documentation is parsed on-demand.

---

## Customization

### Change Port
Edit `app/v_model_viewer.py`:
```python
app.run(debug=True, host='localhost', port=5001)
```

### Add New Section
1. Create markdown file in `docs/`
2. Add route in `app/v_model_viewer.py`
3. Create template in `viewer/templates/`
4. Add navigation link in `base.html`

### Modify Styling
Edit `viewer/templates/base.html` CSS section:
- Colors
- Fonts
- Layout
- Responsive breakpoints

---

## Verification & Validation

### Verification (Left → Right: Design → Code → Tests)
- Design is verified correct by unit tests
- Unit tests verify component specifications
- Integration tests verify component interactions
- System tests verify requirements implementation

### Validation (Right → Left: Tests → Requirements)
- Acceptance tests validate customer requirements
- System tests validate all requirements
- Test results trace back to requirements

### Quality Gates
Each phase has entry/exit criteria:
- Requirements complete and reviewed
- Design reviewed and approved
- Code reviewed and tested
- All tests passing
- Traceability complete

---

## ASPICE Alignment

This implementation follows **ASPICE (Automotive SPICE)** best practices:

- ✅ **SWE2**: Software Design - High-level architecture documented
- ✅ **SWE3**: Software Implementation - Detailed component design
- ✅ **SWE4**: Software Unit Development - Code structure defined
- ✅ **SWE5**: Software Integration - Integration test planning
- ✅ **SWE6**: Software System Testing - Test strategy defined
- ✅ **REQ**: Requirements Analysis - Requirements documented

---

## Support & Documentation

### If You Need To...

**Understand the V-Model**
- Read: `docs/v-model/v-model-overview.md`

**View Requirements**
- Use: V-Model Viewer → Requirements tab
- Or read: `docs/requirements/*.md`

**Understand Architecture**
- Use: V-Model Viewer → Design tab
- Or read: `docs/design/system-architecture.md`

**Check Traceability**
- Use: V-Model Viewer → Traceability tab
- Or read: `docs/traceability/requirements-traceability-matrix.md`

**Modify Documentation**
- Edit markdown files in `docs/`
- Viewer refreshes on next page load
- Changes are automatically visible

**Deploy or Share**
- Run: `python app/v_model_viewer.py`
- Share URL: `http://localhost:5000`
- No installation needed for viewers

---

## Summary

You now have:

✅ Complete ASPICE V-Model documentation  
✅ 60 requirements (17 system + 43 software)  
✅ Full requirement traceability  
✅ System & detailed design with Mermaid diagrams  
✅ Interactive web-based viewer  
✅ Color-coded priorities & status  
✅ Requirement filtering by category  
✅ Design pattern documentation  

**Everything is markdown-based, versioned, and accessible through an easy-to-use web UI!**

---

**Questions?** Check the individual documentation files or review the V-Model Viewer README for detailed instructions.

**Ready to start?** Run `python app/v_model_viewer.py` and open `http://localhost:5000`
