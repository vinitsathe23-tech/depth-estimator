# Agent Guidelines

This project uses an ASPICE/V-model workflow. Any agent or developer modifying the project must begin with change impact analysis and give the user a concise overview before making changes.

## Required Pre-Change Workflow

Before editing code, documentation, templates, requirements, or configuration:

1. Read the relevant files and understand the requested change.
2. Perform impact analysis using [CHANGE_IMPACT_ANALYSIS.md](docs/aspice/CHANGE_IMPACT_ANALYSIS.md).
3. Give the user an overview that includes:
   - Requested change summary
   - Files, requirements, design components, and traceability links likely affected
   - Risk level: LOW, MEDIUM, HIGH, or CRITICAL
   - Expected documentation, test, and ASPICE/V-model impacts
   - Proposed implementation steps
4. Wait for user approval before making changes, unless the user has already explicitly asked to proceed with implementation.

## Impact Analysis Minimum Standard

Every change overview must cover:

- Direct scope impact
- Traceability impact
- Dependency impact
- ASPICE compliance impact
- Design and documentation consistency impact
- Testing or verification impact
- Effort and risk estimate

For small typo or formatting fixes, a brief impact summary is enough. For requirements, architecture, traceability, viewer behavior, or perception-pipeline changes, use a fuller analysis.

## Implementation Rules

- Keep changes focused and traceable to the approved request.
- Preserve requirement IDs and traceability mappings.
- Update related documentation when code or architecture behavior changes.
- Update the requirements traceability matrix when requirements are added, changed, deprecated, or remapped.
- Do not delete requirements; mark them deprecated and explain why.
- Verify markdown tables, Mermaid diagrams, and the Flask viewer when affected.
- Report what changed and what was verified after implementation.

## Approval Gates

- LOW risk: brief user approval or explicit implementation request is sufficient.
- MEDIUM risk: include traceability review in the overview.
- HIGH risk: include ASPICE and architecture impacts before proceeding.
- CRITICAL risk: require explicit user approval after a full impact report.
