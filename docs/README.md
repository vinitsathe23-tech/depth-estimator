# Project Documentation

This directory contains the V-model, requirements, design, and ASPICE process documentation for the Monocular Depth Sandbox project.

## Structure

```text
docs/
  README.md
  aspice/
    ASPICE_ALIGNMENT.md
    ASPICE_IMPLEMENTATION_GUIDE.md
    ASPICE_V_MODEL_INDEX.md
    CHANGE_IMPACT_ANALYSIS.md
    SKILLS.md
  v-model/
    v-model-overview.md
  requirements/
    system-requirements.md
    software-requirements.md
  design/
    system-architecture.md
  traceability/
    requirements-traceability-matrix.md
  verification/
    test-plan.md
    acceptance-criteria.md
```

## Entry Points

- [ASPICE index](aspice/ASPICE_V_MODEL_INDEX.md)
- [Change impact analysis](aspice/CHANGE_IMPACT_ANALYSIS.md)
- [System requirements](requirements/system-requirements.md)
- [Software requirements](requirements/software-requirements.md)
- [Architecture and design](design/system-architecture.md)

The Flask viewer reads the markdown files from this `docs/` tree and renders them through `app/v_model_viewer.py`.
