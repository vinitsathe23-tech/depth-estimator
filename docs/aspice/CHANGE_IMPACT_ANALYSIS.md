# Change Impact Analysis Framework

**Document ID**: CIA-001  
**Version**: 1.0  
**Date**: May 2026  
**Status**: Active

## Overview

This document provides a framework for **Change Impact Analysis (CIA)** - a systematic approach to assess the effects of proposed changes on the ASPICE V-Model documentation, design, and traceability before implementation.

Every change should be evaluated for:
- **Scope**: What is affected?
- **Risk**: What could break?
- **Traceability**: What loses/gains mappings?
- **Compliance**: Does ASPICE compliance change?
- **Effort**: How much work is this?
- **Dependencies**: What else depends on this?

---

## 📋 Impact Analysis Template

### Change Information
```
Change ID: [Generated]
Change Type: [Requirement | Design | Traceability | Documentation | UI | Process]
Priority: [HIGH | MEDIUM | LOW]
Requested By: [User/Agent]
Date Requested: [Date]
Change Description: [What is changing?]
Reason for Change: [Why is this needed?]
```

### Impact Assessment

#### 1. Direct Scope Impact
**Question**: What documents/requirements/design components are directly affected?

**Analysis**:
- List affected documents
- Identify requirement IDs
- Name design components
- List diagram changes needed
- Document sections involved

**Example**:
```
Direct Impact:
- Document: docs/requirements/software-requirements.md
- Requirements: SWE-F-D-001, SWE-F-D-002
- Component: DepthEstimator
- Diagrams: Architecture diagram, Data flow diagram
```

#### 2. Traceability Impact
**Question**: What traceability links are affected?

**Analysis**:
- SWE-REQ → SYS-REQ mappings changed?
- Design → SWE-REQ mappings changed?
- Test → Design mappings affected?
- Are all traces still valid?
- Any new orphaned requirements created?
- Coverage percentage changes?

**Risk Assessment**:
- ✅ No impact on traceability
- ⚠️ May need RTM updates
- ❌ Risk of breaking traceability

**Example**:
```
Traceability Impact:
- Change affects: SWE-F-D-001 (Maps to SYS-F-002)
- Result: SYS-F-002 traceability unchanged
- RTM Updates needed: Yes (1 entry)
- Coverage remains: 100%
- Risk: LOW
```

#### 3. Dependency Impact
**Question**: What else depends on the changed item?

**Analysis**:
- Which requirements depend on this one?
- Which design components use this component?
- Which tests verify this?
- Which other documents reference this?
- Are there downstream requirements?

**Example**:
```
Dependency Impact:
- SWE-F-D-001 is referenced by: SWE-F-OD-001, SWE-F-DE-001
- DepthEstimator used by: CalibrationEngine, PositionEstimator
- Design change cascades: YES
- Need to update: 3 downstream requirements
- Risk: MEDIUM
```

#### 4. ASPICE Compliance Impact
**Question**: Does this change affect ASPICE v4.0 compliance?

**Analysis**:
- Does it affect capability level?
- Does it affect process implementation?
- Does it follow ASPICE practices?
- Does it maintain quality attributes?
- Does it preserve V-Model structure?

**Example**:
```
Compliance Impact:
- Capability Level: CL2-3 maintained ✓
- Process PA SWE2 2.1: Still implemented ✓
- Traceability: 100% maintained ✓
- Quality: Non-functional requirements addressed ✓
- V-Model: Structure preserved ✓
- Risk: LOW
```

#### 5. Design Consistency Impact
**Question**: Does this maintain design integrity?

**Analysis**:
- Violates design patterns?
- Breaks component responsibilities?
- Changes interface contracts?
- Affects non-functional requirements?
- Introduces technical debt?

**Example**:
```
Design Consistency Impact:
- Design Pattern: Strategy pattern still applicable ✓
- Component Responsibility: DepthEstimator focus maintained ✓
- Interface Changes: None ✓
- Non-Functional Impact: Performance targets still met ✓
- Technical Debt: None introduced ✓
- Risk: LOW
```

#### 6. Documentation Consistency Impact
**Question**: What documentation needs to stay in sync?

**Analysis**:
- V-Model overview affected?
- Architecture diagram needs update?
- Component descriptions need update?
- Data flow diagram affected?
- Integration points changed?
- Version numbers need updates?

**Example**:
```
Documentation Consistency Impact:
- Update needed: docs/design/system-architecture.md
- Diagrams: Architecture (update component), Data Flow (no change)
- Section updates: Component descriptions (1 section)
- Version: Bump to v1.1 (minor change)
- Effort: 30 minutes
- Risk: LOW (isolated changes)
```

#### 7. Testing Impact
**Question**: What testing is affected?

**Analysis**:
- Unit tests affected?
- Integration tests affected?
- System tests affected?
- Test cases need updates?
- New tests needed?
- Coverage changes?

**Example**:
```
Testing Impact:
- Unit Tests: 3 tests may need updates
- Integration Tests: 2 tests affected
- System Tests: 5 tests may be affected
- New tests: Yes (1 new test case)
- Coverage: Remains ≥90%
- Effort: 4 hours
- Risk: MEDIUM (test updates required)
```

#### 8. Effort Estimate
**Question**: How much work is this change?

**Analysis**:
- Documentation updates: X hours
- Design changes: X hours
- Code/template changes: X hours
- Testing changes: X hours
- Review/validation: X hours
- **Total estimate**: X hours

**Example**:
```
Effort Breakdown:
- Update requirement: 0.5 hours
- Update RTM: 0.25 hours
- Update architecture doc: 0.5 hours
- Update diagrams: 1 hour
- Validation/review: 0.5 hours
- TOTAL: 2.75 hours
```

---

## 🎯 Impact Risk Matrix

### Risk Assessment Framework

```
         PROBABILITY
         Low  Medium  High
HIGH     MED  HIGH   CRIT
IMPACT
MEDIUM   LOW  MED    HIGH
LOW      LOW  LOW    MED
```

### Severity Ratings

| Level | Definition | Action |
|-------|-----------|--------|
| **LOW** | Isolated change, no cascading effects, minimal review needed | Proceed with normal review |
| **MEDIUM** | Some dependencies, limited cascading, standard review | Require traceability review |
| **HIGH** | Significant dependencies, cascading effects, extensive review | Require ASPICE compliance review |
| **CRITICAL** | Breaks traceability, affects compliance, widespread cascading | Require architecture review + approval |

---

## 📊 Impact Analysis Categories

### By Change Type

#### 1. Adding a New Requirement
**Typical Impact**:
- Low impact if isolated to single category
- Requires traceability mapping
- May require RTM update

**Key Questions**:
- Is it properly traced to SYS-REQ?
- Does it affect existing components?
- Is priority appropriate?
- Does design support it?

**Risk Level**: Usually LOW-MEDIUM

#### 2. Modifying Existing Requirement
**Typical Impact**:
- Moderate impact on dependencies
- Requires traceability review
- May cascade to design

**Key Questions**:
- What depends on this requirement?
- Does design still satisfy it?
- Are tests still valid?
- Does it affect non-functional targets?

**Risk Level**: Usually MEDIUM-HIGH

#### 3. Deleting a Requirement
**Typical Impact**:
- High impact on traceability
- Orphans dependent requirements
- May break design assumptions

**Key Questions**:
- What depends on this requirement?
- Is design affected?
- Are tests still valid?
- Is SYS-REQ trace lost?

**Risk Level**: Usually HIGH-CRITICAL

#### 4. Changing Architecture/Design
**Typical Impact**:
- High impact on implementation
- Affects multiple requirements
- Cascades to component design

**Key Questions**:
- What components are affected?
- What requirements change?
- What tests need update?
- Is modularity preserved?

**Risk Level**: Usually HIGH

#### 5. Updating Documentation
**Typical Impact**:
- Low-moderate impact if cosmetic
- Higher if content changes significantly
- May affect understanding

**Key Questions**:
- Is technical content correct?
- Are diagrams still accurate?
- Are examples still valid?
- Does clarity improve?

**Risk Level**: Usually LOW-MEDIUM

---

## ✅ Impact Analysis Checklist

Before implementing ANY change:

### Pre-Change Assessment
- [ ] Change clearly defined and justified
- [ ] Change type identified
- [ ] Scope boundaries clear
- [ ] Initial risk estimate made

### Traceability Review
- [ ] All affected requirements identified
- [ ] Traceability relationships reviewed
- [ ] No orphaned requirements expected
- [ ] Coverage impact assessed
- [ ] RTM changes planned

### Dependency Analysis
- [ ] Downstream requirements identified
- [ ] Component dependencies mapped
- [ ] Design implications considered
- [ ] Test impacts assessed
- [ ] Documentation cascade identified

### ASPICE Compliance Review
- [ ] Capability level maintained
- [ ] Process practices still met
- [ ] Requirements remain formal
- [ ] Design remains verifiable
- [ ] V-Model structure preserved

### Design Consistency Review
- [ ] Design patterns still applicable
- [ ] Component responsibilities maintained
- [ ] Interfaces remain valid
- [ ] Non-functional requirements met
- [ ] No technical debt introduced

### Documentation Review
- [ ] All affected docs identified
- [ ] Version numbers planned
- [ ] Diagrams need updates identified
- [ ] Change history documented
- [ ] Review process clear

### Effort & Risk Assessment
- [ ] Effort estimate provided
- [ ] Risk level assigned
- [ ] Mitigation strategies identified
- [ ] Approval gates clear
- [ ] Success criteria defined

### Final Validation
- [ ] Impact analysis complete
- [ ] Risk acceptable
- [ ] Resources available
- [ ] Schedule realistic
- [ ] Proceed decision made

---

## 🚦 Approval Gates by Risk Level

### LOW Risk Changes
**Approval**: Developer/Agent review only
- **Review time**: 30 minutes
- **Documentation**: Impact summary
- **Proceed**: Direct implementation

### MEDIUM Risk Changes
**Approval**: Technical Lead + Traceability review
- **Review time**: 1-2 hours
- **Documentation**: Full impact analysis
- **Proceed**: After traceability verification

### HIGH Risk Changes
**Approval**: Technical Lead + ASPICE compliance review
- **Review time**: 2-4 hours
- **Documentation**: Complete impact analysis with mitigation
- **Proceed**: After architecture review

### CRITICAL Risk Changes
**Approval**: Architecture review + stakeholder approval
- **Review time**: 4+ hours
- **Documentation**: Full impact analysis + risk register
- **Proceed**: After formal approval meeting

---

## 📝 Impact Analysis Report Template

```markdown
# Impact Analysis Report

**Change ID**: [ID]
**Date**: [Date]
**Analyst**: [Name]
**Status**: [Draft | In Review | Approved | Rejected]

## Executive Summary
[1-2 sentence overview of the change and its impact]

## Change Description
[What is changing and why?]

## Scope
[What documents/requirements/components affected?]

## Impact Assessment

### Traceability Impact: [LOW | MEDIUM | HIGH]
[Details on requirement mappings affected]

### Design Impact: [LOW | MEDIUM | HIGH]
[Details on architecture/component impacts]

### Testing Impact: [LOW | MEDIUM | HIGH]
[Details on test coverage/changes needed]

### ASPICE Compliance Impact: [MAINTAINED | AT RISK | IMPROVED]
[Details on capability level and process impacts]

### Documentation Impact: [MINIMAL | MODERATE | EXTENSIVE]
[List of documents needing updates]

## Risk Assessment
- **Overall Risk Level**: [LOW | MEDIUM | HIGH | CRITICAL]
- **Probability**: [Low | Medium | High]
- **Impact Severity**: [Low | Medium | High]
- **Mitigation**: [Strategy to reduce risk]

## Effort Estimate
- **Total Effort**: [X hours]
- **Timeline**: [Start-End dates]
- **Resources**: [Required skill/people]

## Dependencies
- **Blocked by**: [None | List items]
- **Blocks**: [None | List items]
- **Related to**: [None | List items]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## Approval
- [ ] Analysis complete
- [ ] Risk acceptable
- [ ] Proceed approved
```

---

## 🔄 Change Implementation Workflow

### Step 1: Create Impact Analysis
- Identify change type
- Assess all impact categories
- Complete checklist
- Calculate risk level

### Step 2: Review & Approval
- Route to appropriate reviewer(s)
- Presenter discusses analysis
- Risk assessment confirmed
- Approval granted or rejected

### Step 3: Implement Change
- Make planned modifications
- Update all affected documents
- Update version numbers
- Maintain traceability

### Step 4: Validation & Verification
- Verify traceability integrity
- Check ASPICE compliance
- Test in viewer if applicable
- Document results

### Step 5: Document & Close
- Update change history
- Archive impact analysis
- Mark change as complete
- Notify stakeholders

---

## 📚 Examples of Impact Analysis

### Example 1: Adding a New Performance Requirement

```
Change: Add requirement SWE-NF-P-005: "System shall support batch processing"

IMPACT ANALYSIS:

Scope: 
- File: software-requirements.md
- Section: Performance (SWE-NF-P)
- New: 1 requirement

Traceability:
- Maps to: SYS-NF-001 (Performance targets)
- Coverage: Remains 100%
- Risk: LOW

Dependencies:
- DepthEstimator component
- Could affect: SWE-F-D-006 (batch processing)
- No downstream cascade

ASPICE Impact:
- Maintains CL2-3
- Still follows PA SWE-REQ 1.2
- No compliance risk

Effort: 1 hour
Risk Level: LOW

Approval: Developer review sufficient
```

### Example 2: Changing Architecture (Adding Component)

```
Change: Add new component "FramePreprocessor" to architecture

IMPACT ANALYSIS:

Scope:
- File: system-architecture.md
- Diagrams: Architecture (add node)
- Components: 6 → 7 components
- Sections: Component descriptions

Traceability:
- May affect: SWE-F-I-005 (frame resolution support)
- Could break: Integration between FrameCapture and DepthEstimator
- Requires: RTM review
- Coverage: May drop if not traced properly
- Risk: MEDIUM

Dependencies:
- Data flow diagram affected
- Integration points changed
- Design patterns: Still applicable
- Tests: 3-4 tests may need updates

ASPICE Impact:
- PA SWE2 2.1: Architecture still clear
- PA SWE2 2.2: Component definitions needed
- May improve non-functional requirements
- Compliance: MAINTAINED (need to document)

Design Consistency:
- Modularity: Preserved
- Component responsibility: New component well-defined
- Interfaces: Need specification
- Risk: MEDIUM

Effort: 6 hours
Risk Level: MEDIUM

Approval: Technical lead review required
```

### Example 3: Correcting Requirement Description

```
Change: Update SWE-F-D-001 description for clarity

IMPACT ANALYSIS:

Scope:
- File: software-requirements.md
- Requirement: SWE-F-D-001
- Change: Clarify backend selection

Traceability:
- Maps to: SYS-F-002 (unchanged)
- Coverage: Remains 100%
- Risk: LOW

Dependencies:
- No downstream cascade
- No design impact
- No test impact
- Risk: LOW

ASPICE Impact:
- PA SWE-REQ 1.2: Improves clarity
- Maintains compliance
- Risk: NONE

Effort: 0.5 hours
Risk Level: LOW

Approval: No review needed (cosmetic fix)
```

---

## 🎯 Best Practices

1. **Do Analysis BEFORE Implementation**
   - Never skip impact analysis
   - Do it early in planning
   - Use it to guide decisions

2. **Be Thorough But Realistic**
   - Cover all impact areas
   - Don't over-analyze trivial changes
   - Adjust effort based on risk

3. **Maintain Traceability**
   - Always verify traceability impact
   - Update RTM immediately
   - Validate 100% coverage maintained

4. **Document Decisions**
   - Archive impact analysis
   - Record approval decision
   - Explain any deviations

5. **Learn from Changes**
   - Track actual vs. estimated effort
   - Note lessons learned
   - Improve process for next time

---

## 🔧 Tools & Integration

### With SKILLS.md
- Reference this framework in change tasks
- Include impact analysis in all workflows

### With ASPICE_ALIGNMENT.md
- Verify compliance impact
- Check capability level maintained

### With V-Model
- Ensure traceability preserved
- Maintain V-Model structure

### With Git/Version Control
- Include impact analysis in commit message
- Archive analysis with change
- Reference in code review

---

**Document Version**: 1.0  
**Last Updated**: May 2026  
**Status**: Active  
**Audience**: Developers, QA, Project Managers, AI Agents
