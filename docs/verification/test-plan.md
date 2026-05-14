# Verification Test Plan

This placeholder tracks the planned right side of the V-model. Add unit, integration, and system test cases here as the prototype matures.

## Current Verification Commands

```powershell
python -m py_compile app/depth_sandbox.py app/perception_orchestrator.py app/v_model_viewer.py
```

## Planned Orchestrator Smoke Tests

- Start with `--object-detector depth-blob` and verify the reusable orchestrator returns a primary detection for the existing overlay path.
- Start with `--object-detector yolo-phone` and verify YOLO detection refreshes according to `--detect-every`.
- Start with `--object-detector depth-blob,yolo-phone` and verify multiple detectors can be configured while the UI still renders the primary detection.
- Start with `--object-detector none` and verify no-detection handling remains graceful.
