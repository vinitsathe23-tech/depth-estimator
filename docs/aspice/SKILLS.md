# ASPICE V-Model Agent Skills

**Document ID**: SKILLS-001  
**Version**: 1.0  
**Date**: May 2026  
**Status**: Active

## Overview

This document defines best practices and skills for AI agents working with the Monocular Depth Sandbox ASPICE V-Model documentation. It provides guidance on maintaining consistency, traceability, and compliance throughout the project.

## Mandatory Agent Workflow: Impact Analysis First

Any agent modifying this project must first perform change impact analysis and give the user an overview before editing files. Use [AGENTS.md](../../AGENTS.md) as the operating guideline and [CHANGE_IMPACT_ANALYSIS.md](CHANGE_IMPACT_ANALYSIS.md) as the analysis framework.

The pre-change overview must summarize:
- Requested change and proposed approach
- Files, requirements, design components, and traceability links affected
- Risk level: LOW, MEDIUM, HIGH, or CRITICAL
- ASPICE/V-model, documentation, and testing impacts
- Whether user approval is required before implementation

For minor typo or formatting fixes, a concise impact summary is acceptable. For requirements, architecture, traceability, viewer behavior, or perception-pipeline changes, provide a fuller analysis before proceeding.

---

## �️ ASPICE v4.0 Compliance Guidelines

### ASPICE Process Framework
Our project follows **Automotive SPICE (AS) v4.0** standards with focus on:
- **SWE-REQ**: Software Requirement Analysis - ✅ CL3 (Established)
- **SWE2**: Software Design - ✅ CL2-3 (Managed/Established)
- **SWE3**: Component Design - ✅ CL2-3 (Managed/Established)
- **Traceability**: Requirements-to-Design-to-Code - ✅ 100% coverage

**Reference**: [ASPICE Alignment Document](ASPICE_ALIGNMENT.md)

### ASPICE Compliance Checklist for Changes

Before finalizing ANY documentation change, verify:

✓ **Traceability**
- All SWE-REQ items traced to ≥1 SYS-REQ
- No orphaned requirements
- Bidirectional links maintained

✓ **Requirements Format**
- Uses formal language ("shall", "must")
- Measurable and testable
- Unique IDs following convention
- Priority assigned

✓ **Design Specifications**
- Architecture clear and documented
- Components have responsibilities
- Interfaces well-defined
- Design patterns applied

✓ **Quality Attributes**
- Non-functional requirements addressed
- Performance targets specified
- Reliability measures documented
- Maintainability considered

✓ **Documentation Standards**
- Consistent formatting
- Version control maintained
- Change history documented
- References accurate

### ASPICE Process Practices Applied

**PA SWE-REQ 1.1**: Derive software requirements from system requirements
- ✅ All SWE-REQ derived from SYS-REQ
- ✅ Mapping documented in RTM

**PA SWE-REQ 1.2**: Ensure requirements are clear and unambiguous
- ✅ Formal language used
- ✅ Requirements are testable
- ✅ No vague language

**PA SWE2 2.1**: Design software architecture
- ✅ Architecture diagram documented
- ✅ Components identified
- ✅ Integration points defined

**PA SWE2 2.2**: Define software design
- ✅ Component specifications provided
- ✅ Data structures defined
- ✅ Algorithms documented
- ✅ Interfaces specified

**PA SWE2 2.3**: Ensure design is verifiable
- ✅ Clear verification methods
- ✅ Test strategy defined
- ✅ Acceptance criteria established

---

## �🎯 Core Skills

### 1. Requirement Management

#### Skill: Adding New Requirements
**When**: Need to add a new requirement to SYS-REQ or SWE-REQ  
**How**:

1. **Identify the requirement type**
   - Is it system-level (SYS-REQ) or software-level (SWE-REQ)?
   - Determine if it's functional (F) or non-functional (NF)
   - Choose appropriate section/category

2. **Follow naming convention**
   - SYS-REQ: `SYS-F-XXX` or `SYS-NF-XXX`
   - SWE-REQ: `SWE-F-<CATEGORY>-XXX` where CATEGORY is:
     - I (Input), D (Depth), OD (Object Detection)
     - DE (Distance Estimation), V (Visualization)
     - O (Output), C (Configuration)
     - P (Performance), Q (Quality), R (Reliability)

3. **Ensure traceability**
   - Every SWE-REQ must reference at least one SYS-REQ
   - Add traceable reference in description: `(SYS-F-XXX)`
   - Update traceability matrix when requirement added

4. **Maintain priority consistency**
   - HIGH: Critical for core functionality
   - MEDIUM: Important but not blocking
   - LOW: Nice-to-have, future enhancement

5. **Template for new requirement**
   ```markdown
   | **SWE-F-CATEGORY-XXX** | Requirement Title | Description (SYS-F-XXX, SYS-NF-XXX) | PRIORITY |
   ```

#### Skill: Modifying Requirements
**When**: Requirements need updates or corrections  
**How**:

1. **Never delete requirements** - mark as deprecated instead
2. **Add change history** at document top:
   ```markdown
   **Changes**: v1.0 → v1.1: Updated SWE-F-D-001 description for clarity
   ```
3. **Update related traceability**
   - If SWE-REQ changes, update RTM
   - If SYS-REQ changes, cascade to dependent SWE-REQ
4. **Validate that all traces still exist**
   - Run through viewer to check coverage
5. **Update document version** if significant changes

6. **Before Committing
#### Skill: Requirement Validation
**When**: Adding or modifying requirements  
**How**:

1. ✓ Check requirement ID is unique
2. ✓ Verify priority is appropriate
3. ✓ Ensure traceability reference exists
4. ✓ Confirm description is clear and testable
5. ✓ Check formatting matches table style
6. ✓ Validate markdown syntax

---

### 2. Design Documentation

#### Skill: Adding Design Patterns
**When**: New design pattern introduced or needs documentation  
**How**:

1. **Document in SWE3 section** of `docs/design/system-architecture.md`
2. **Include pattern name and type** (Creational, Structural, Behavioral)
3. **Provide these sections**:
   - Usage: Where is it used?
   - Benefit: Why use it?
   - Example: Code or component example

4. **Template**:
   ```markdown
   ### 🔄 [Pattern Name] Pattern
   **Type**: [Creational/Structural/Behavioral]
   **Usage**: [Component/Module name]
   **Benefit**: [Primary advantage]
   **Example**: [Specific example in code]
   ```

#### Skill: Modifying Architecture
**When**: System architecture changes  
**How**:

1. **Update Mermaid diagram first**
   - Modify graph structure
   - Update node labels and relationships
   - Ensure diagram is valid

2. **Validate diagram**
   - Run through Mermaid validator
   - Check syntax

3. **Update component descriptions**
   - Modify component sections
   - Update responsibilities
   - Update methods/interfaces

4. **Update data flow diagram**
   - Modify sequence diagram if data flow changes
   - Ensure all components are accounted for

5. **Update integration points section**
   - Add/remove integration connections
   - Update integration diagram

6. **Cascade changes**
   - Check if any SWE-REQ affected
   - Update traceability if needed

#### Skill: Mermaid Diagram Management
**When**: Creating or modifying diagrams  
**How**:

1. **Syntax validation**
   - Diagram type: flowchart, sequenceDiagram, graph, etc.
   - Check bracket matching
   - Validate node IDs and references

2. **Best practices**
   - Keep diagrams focused (one concept per diagram)
   - Use clear labels
   - Use consistent naming
   - Add styling for visual clarity
   - Include legend if needed

3. **Example structure**:
   ```mermaid
   graph TD
       A["Clear Label"] -->|relationship| B["Another Label"]
       style A fill:#e3f2fd
   ```

4. **Integration**:
   - Wrap in markdown code block: ` ```mermaid ` ... ` ``` `
   - Place in appropriate section
   - Reference in text above diagram

---

### 3. Traceability Management

#### Skill: Maintaining Requirements Traceability Matrix (RTM)
**When**: Requirements added, modified, or deleted  
**How**:

1. **Map SWE-REQ to SYS-REQ**
   - Each SWE-REQ must map to ≥1 SYS-REQ
   - Use consistent format: `| SWE-ID | SYS-IDs |`

2. **Check for orphaned requirements**
   - All SWE-REQ should have traceability
   - All SYS-REQ should have coverage
   - Flag any unmapped requirements

3. **Coverage calculation**
   - Total Mapped SWE-REQ / Total SWE-REQ × 100 = Coverage %
   - Target: 100% coverage
   - Document in RTM header

4. **Update when**:
   - New requirement added
   - Requirement IDs changed
   - Traceability relationship changed

#### Skill: Bidirectional Traceability
**When**: Analyzing impact of changes  
**How**:

1. **If SYS-REQ changes**:
   - Identify all mapped SWE-REQ
   - Check if design (SWE2/SWE3) affected
   - Validate no "downstream" issues

2. **If SWE-REQ changes**:
   - Verify still maps to SYS-REQ
   - Check if design component affected
   - Update design if needed

3. **If SWE2 changes**:
   - Check which SWE-REQ affected
   - Verify SWE3 components updated
   - Validate SWE-REQ still achievable

4. **If SWE3 changes**:
   - Check which SWE2 architecture affected
   - Verify design still implements SWE-REQ
   - Update as needed

---

### 4. Documentation Quality

#### Skill: Writing Clear Requirements
**When**: Creating or editing requirements  
**How**:

1. **Use actionable language**
   - ✓ "System shall support..."
   - ✓ "Component must provide..."
   - ✗ "System might..." (too vague)
   - ✗ "Maybe support..." (not testable)

2. **Make requirements testable**
   - Include measurable criteria where possible
   - Avoid ambiguous terms (e.g., "fast", "reliable")
   - Be specific: "≥15 FPS" not "real-time"

3. **Keep requirements focused**
   - One requirement = one concept
   - Split complex requirements into smaller ones
   - Avoid compound "and/or" statements

4. **Checklist**:
   - ✓ Requirement ID is unique
   - ✓ Title is clear and concise
   - ✓ Description is 1-2 sentences
   - ✓ Priority is assigned
   - ✓ Traceability is included
   - ✓ Language is formal and consistent

#### Skill: Markdown Formatting
**When**: Writing documentation  
**How**:

1. **Headers**:
   ```markdown
   # H1 - Document Title (one per page)
   ## H2 - Major Section
   ### H3 - Subsection
   #### H4 - Detail/Point
   ```

2. **Tables**:
   ```markdown
   | Column 1 | Column 2 | Column 3 |
   |----------|----------|----------|
   | Data     | Data     | Data     |
   ```

3. **Code/Requirements**:
   - Use backticks for requirement IDs: `` `SYS-F-001` ``
   - Use backticks for code references: `` `ClassName.method()` ``
   - Use code blocks for multi-line code

4. **Emphasis**:
   - Bold for important: `**text**`
   - Italics for context: `*text*`
   - Avoid excessive formatting

5. **Lists**:
   - Bullet points (hyphens) for unordered
   - Numbers for ordered/sequential

---

### 5. Version Control & Updates

#### Skill: Updating Documentation Safely
**When**: Making changes to existing documents  
**How**:

1. **Before editing**:
   - Check current file state
   - Read surrounding context (3-5 lines before/after)
   - Understand full scope of change

2. **When editing**:
   - Include context in replacements (3-5 lines before/after)
   - Make minimal, focused changes
   - Preserve formatting and style

3. **After editing**:
   - Validate markdown syntax
   - Check diagrams still render
   - Verify traceability still intact
   - Test in viewer if possible

4. **Common pitfalls to avoid**:
   - ✗ Don't remove requirement IDs
   - ✗ Don't break markdown table formatting
   - ✗ Don't break Mermaid diagrams
   - ✗ Don't create orphaned requirements
   - ✗ Don't lose traceability

#### Skill: Managing Document Versions
**When**: Making significant changes  
**How**:

1. **Version format**: `Major.Minor`
   - Major: Significant structural changes
   - Minor: Content updates, clarifications

2. **Version history**:
   ```markdown
   **Version History**:
   - v1.1: [Date] - [Change description]
   - v1.0: [Date] - Initial version
   ```

3. **Update triggers**:
   - ✓ v1.1: Adding new requirements
   - ✓ v1.2: Modifying descriptions
   - ✓ v2.0: Major architecture changes
   - ✓ v2.1: Design pattern additions

---

### 6. V-Model Compliance

#### Skill: Maintaining V-Model Structure
**When**: Adding documentation or features  
**How**:

1. **Understand the V-Model phases**:
   - **LEFT (Definition)**: REQ → SWE2 → SWE3 → SWE4
   - **RIGHT (Verification)**: Tests → SWE6 → SWE5 → Unit Tests
   - **TRACEABILITY**: Bidirectional connections

2. **When adding requirements** (REQ phase):
   - Create at system level (SYS-REQ)
   - Decompose to software level (SWE-REQ)
   - Ensure traceability defined

3. **When creating design** (SWE2/SWE3):
   - Document architecture (SWE2)
   - Detail components (SWE3)
   - Trace back to SWE-REQ
   - Design for testability

4. **When planning tests** (right side):
   - Map tests to SWE-REQ (verification)
   - Map tests to SYS-REQ (validation)
   - Ensure coverage

#### Skill: ASPICE Alignment
**When**: Ensuring compliance  
**How**:

1. **Know the ASPICE processes**:
   - **SYS-REQ**: System requirements analysis ✓ (Documented)
   - **SWE-REQ**: Software requirements analysis ✓ (Documented)
   - **SWE2**: Software design - system level ✓ (Documented)
   - **SWE3**: Software design - component level ✓ (Documented)
   - **SWE4**: Software implementation ✓ (Structure ready)
   - **SWE5**: Software integration & testing ✓ (Plan ready)
   - **SWE6**: Software system testing ✓ (Plan ready)

2. **Maintain coverage**:
   - All phases documented
   - Traceability complete
   - Quality gates defined
   - No phase skipped

3. **Best practices**:
   - Keep documentation in sync with code
   - Maintain traceability
   - Use design patterns
   - Document decisions

---

### 7. Viewer & UI Management

#### Skill: Working with Flask Viewer
**When**: Modifying or extending the web UI  
**How**:

1. **Understand the structure**:
   - Backend: `app/v_model_viewer.py` (Flask routes & parsing)
   - Frontend: `viewer/templates/*.html` (UI pages)
   - Parser: `RequirementParser` class
   - Styling: CSS in `base.html`

2. **When updating documentation**:
   - Markdown files auto-refresh on viewer restart
   - No backend code changes needed
   - Diagrams render from Mermaid CDN

3. **When adding new pages**:
   - Create new template in `viewer/templates/`
   - Add route in `app/v_model_viewer.py`
   - Add navigation link in `base.html`
   - Test in browser

4. **Common modifications**:
   - Add requirement category: Edit `build_requirement_tree()` function
   - Change colors: Edit CSS in `base.html`
   - Add new tab: Create tab content div in template
   - Modify parsing: Update `RequirementParser` class

---

### 8. Common Tasks

#### Task: Add a New Functional Requirement

**Step 1**: Choose category
- Input (I), Depth (D), Detection (OD), Distance (DE), Visualization (V), Output (O), Config (C)

**Step 2**: Generate ID
- Example: `SWE-F-D-007` (next in Depth category)

**Step 3**: Write requirement
- Title: Clear, concise, action-oriented
- Description: What it does, reference SYS-REQ
- Priority: HIGH/MEDIUM/LOW

**Step 4**: Add to markdown table
- In `docs/requirements/software-requirements.md`
- Under appropriate section
- Maintain table formatting

**Step 5**: Update RTM
- Add entry to `requirements-traceability-matrix.md`
- Verify coverage % is 100%

**Step 6**: Test in viewer
- Restart viewer: `python app/v_model_viewer.py`
- Check Requirements tab
- Verify rendering in browser

#### Task: Update System Architecture

**Step 1**: Plan changes
- Identify components affected
- Determine if SWE2 or SWE3 or both

**Step 2**: Update diagrams
- Modify architecture diagram (Mermaid)
- Update data flow diagram if needed
- Validate syntax

**Step 3**: Update descriptions
- Modify component sections
- Update responsibilities
- Update method signatures

**Step 4**: Check traceability
- Does architecture change affect SWE-REQ?
- Are designs still achievable?
- Update requirements if needed

**Step 5**: Update design patterns
- Add new patterns if introduced
- Document pattern usage

**Step 6**: Test changes
- Restart viewer
- Check Design tab
- Verify diagrams render

#### Task: Verify Traceability

**Step 1**: Open RTM
- `docs/traceability/requirements-traceability-matrix.md`

**Step 2**: Check coverage
- Calculate: (Traced SWE-REQ / Total SWE-REQ) × 100
- Target: 100%

**Step 3**: Look for issues
- Red "NOT TRACED" flags = Orphaned requirements
- Missing SYS-REQ references = Incomplete requirements

**Step 4**: Fix issues
- Add missing traceability
- Update SWE-REQ descriptions
- Modify SYS-REQ if needed

**Step 5**: Verify in viewer
- Go to Traceability tab
- Check statistics
- Confirm 100% coverage

#### Task: Verify ASPICE Compliance

**Step 1**: Check Capability Levels
- Open: `ASPICE_ALIGNMENT.md`
- Review capability assessment matrix
- Verify current CL2-3 status

**Step 2**: Verify Process Implementation
- SWE-REQ: All requirements formal and traceable? ✓
- SWE2: Architecture documented and clear? ✓
- SWE3: Components well-specified? ✓
- Traceability: 100% coverage maintained? ✓

**Step 3**: Check ASPICE Practices
- PA SWE-REQ 1.1: All SWE-REQ derived from SYS-REQ? ✓
- PA SWE-REQ 1.2: Requirements clear and unambiguous? ✓
- PA SWE2 2.1: Architecture designed and documented? ✓
- PA SWE2 2.2: Components defined with interfaces? ✓
- PA SWE2 2.3: Design is verifiable? ✓

**Step 4**: Validate Documentation Standards
- Formal language used ("shall", "must")
- Measurable criteria included
- Unique IDs assigned
- Version control maintained
- Change history documented

**Step 5**: Update Compliance Record
- If changes made, update document versions
- Update compliance checklist section
- Document any capability improvements

**Step 6**: Reference Official Standard
- Refer to ASPICE v4.0 PAM for processes
- Cross-check with: `ASPICE_ALIGNMENT.md`
- Maintain audit trail

---

## 📋 Quality Checklist

Use this checklist before finalizing documentation:

### Requirement Checklist
- ✓ Requirement ID follows naming convention
- ✓ Title is clear and action-oriented
- ✓ Description is specific and testable
- ✓ Priority is assigned (HIGH/MEDIUM/LOW)
- ✓ Traceability reference included
- ✓ Markdown syntax is valid
- ✓ No duplicate IDs

### Design Checklist
- ✓ Architecture clear and well-organized
- ✓ Components have clear responsibilities
- ✓ Interfaces well-defined
- ✓ Mermaid diagrams valid and render correctly
- ✓ Data flow documented
- ✓ Design patterns explained
- ✓ Integration points identified

### Traceability Checklist
- ✓ All SWE-REQ mapped to ≥1 SYS-REQ
- ✓ All SYS-REQ have ≥1 SWE-REQ
- ✓ Coverage = 100%
- ✓ No orphaned requirements
- ✓ RTM up-to-date
- ✓ Bidirectional links valid

### Documentation Checklist
- ✓ Markdown formatting consistent
- ✓ No broken links
- ✓ Diagrams render correctly
- ✓ Version number updated if needed
- ✓ Change history documented
- ✓ Review for typos and clarity
- ✓ Tables properly formatted

### Viewer Checklist
- ✓ Flask app starts without errors
- ✓ All pages load correctly
- ✓ Navigation works
- ✓ Diagrams display
- ✓ Requirements parse correctly
- ✓ Traceability calculates correctly
- ✓ UI responsive on mobile

### ASPICE Compliance Checklist
- ✓ Traceability: 100% SWE-REQ → SYS-REQ
- ✓ Requirements: Formal language ("shall", "must")
- ✓ Requirements: Measurable and testable
- ✓ Design: Architecture documented (SWE2)
- ✓ Design: Components detailed (SWE3)
- ✓ Interfaces: Well-defined
- ✓ Patterns: Design patterns applied
- ✓ Verification: Test strategy aligned
- ✓ Documentation: Version controlled
- ✓ Compliance: Capability Level CL2-3 maintained

---

## 🚫 Anti-Patterns (Avoid These)

| Pattern | Problem | Solution |
|---------|---------|----------|
| Vague requirements | Not testable, hard to implement | Make specific: "≥15 FPS" not "fast" |
| Orphaned requirements | Lose traceability, management nightmare | Every SWE-REQ must map to SYS-REQ |
| Broken diagrams | Documentation unusable | Validate Mermaid syntax before committing |
| Deleted requirements | Lost history, traceability breaks | Mark deprecated, keep for audit trail |
| Inconsistent naming | Confusing, hard to maintain | Use exact naming convention consistently |
| No traceability | Can't verify completeness | Update RTM with every requirement change |
| Duplicate IDs | Parser confusion, display issues | Check existing IDs before creating new |
| Poor descriptions | Ambiguous, hard to test | Be specific, use measurable criteria |
| Broken links | Documentation broken | Check all references before publishing |
| Inconsistent formatting | Unprofessional, parser issues | Match existing table/header formats |

---

## 🔧 Tools & Resources

| Tool | Purpose | Location |
|------|---------|----------|
| **Flask Viewer** | Interactive UI | `app/v_model_viewer.py` |
| **Mermaid** | Diagram rendering | CDN (online) |
| **Markdown** | Documentation format | `.md` files |
| **Git** | Version control | `.git/` |
| **Browser** | Viewing UI | `http://localhost:5000` |

---

## 📚 References

- [V-Model Overview](../v-model/v-model-overview.md)
- [System Requirements](../requirements/system-requirements.md)
- [Software Requirements](../requirements/software-requirements.md)
- [System Architecture](../design/system-architecture.md)
- [Traceability Matrix](../traceability/requirements-traceability-matrix.md)
- [Implementation Guide](ASPICE_IMPLEMENTATION_GUIDE.md)
- [Quick Start](../../QUICK_START.md)

---

## 📞 When in Doubt

1. **Check existing documentation** - Pattern already exists?
2. **Follow the template** - Use existing examples as template
3. **Validate syntax** - Run through parser/validator
4. **Check traceability** - Is requirement traced?
5. **Test in viewer** - Does it display correctly?
6. **Review quality** - Does it match this skills guide?

---

**Document Version**: 1.0  
**Last Updated**: May 2026  
**Status**: Active  
**Audience**: AI Agents, Developers, Documentation Maintainers
