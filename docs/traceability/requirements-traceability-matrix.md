# Requirements Traceability Matrix

The interactive viewer currently builds the software-to-system traceability matrix from references in:

- [system-requirements.md](../requirements/system-requirements.md)
- [software-requirements.md](../requirements/software-requirements.md)
- [system-architecture.md](../design/system-architecture.md)

When requirements are added, changed, deprecated, or remapped, update the source requirement tables first and then verify the generated traceability view with:

```powershell
python app/v_model_viewer.py
```

