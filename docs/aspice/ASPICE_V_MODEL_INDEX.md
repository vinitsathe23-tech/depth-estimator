# ASPICE V-Model Documentation Index

**Project**: Monocular Depth Sandbox  
**Compliance Theme**: ASPICE / V-Model  
**Status**: Active  
**Version**: 1.1

## Start Here

| Need | File |
|---|---|
| Project overview and runtime commands | [README.md](../../README.md) |
| Fast viewer setup | [QUICK_START.md](../../QUICK_START.md) |
| Agent modification rules | [AGENTS.md](../../AGENTS.md) |
| Change impact analysis framework | [CHANGE_IMPACT_ANALYSIS.md](CHANGE_IMPACT_ANALYSIS.md) |
| ASPICE implementation guide | [ASPICE_IMPLEMENTATION_GUIDE.md](ASPICE_IMPLEMENTATION_GUIDE.md) |
| ASPICE alignment notes | [ASPICE_ALIGNMENT.md](ASPICE_ALIGNMENT.md) |
| Agent skills guide | [SKILLS.md](SKILLS.md) |
| Viewer guide | [viewer/README.md](../../viewer/README.md) |

## Project Structure

```text
monocular-depth-sandbox/
  README.md
  QUICK_START.md
  AGENTS.md
  app/
    depth_sandbox.py
    v_model_viewer.py
  viewer/
    README.md
    templates/
  requirements/
    runtime.txt
    gpu.txt
    viewer.txt
  docs/
    README.md
    aspice/
      ASPICE_ALIGNMENT.md
      ASPICE_IMPLEMENTATION_GUIDE.md
      ASPICE_V_MODEL_INDEX.md
      CHANGE_IMPACT_ANALYSIS.md
      SKILLS.md
    v-model/
    requirements/
    design/
    traceability/
    verification/
  data/
    input/
    output/
```

## V-Model Documents

| Area | File |
|---|---|
| V-Model lifecycle | [v-model-overview.md](../v-model/v-model-overview.md) |
| System requirements | [system-requirements.md](../requirements/system-requirements.md) |
| Software requirements | [software-requirements.md](../requirements/software-requirements.md) |
| Architecture and design | [system-architecture.md](../design/system-architecture.md) |

## Run Commands

Install viewer dependencies:

```powershell
python -m pip install -r requirements/viewer.txt
```

Start the ASPICE/V-model viewer:

```powershell
python app/v_model_viewer.py
```

Run the perception sandbox:

```powershell
python app/depth_sandbox.py --source 0 --backend pseudo
```

## Modification Rule

Before changing code, documentation, templates, requirements, or configuration, agents must perform impact analysis and give the user an overview of affected files, requirements, traceability links, risk level, and proposed steps. See [AGENTS.md](../../AGENTS.md) and [CHANGE_IMPACT_ANALYSIS.md](CHANGE_IMPACT_ANALYSIS.md).
