# Changelog

All notable project changes are recorded here.

## 2026-05-14

### Changed

- Reorganized the project into clearer top-level folders:
  - `app/` for executable Python entry points.
  - `viewer/` for Flask viewer documentation and templates.
  - `requirements/` for dependency files.
  - `docs/aspice/` for ASPICE, impact-analysis, and agent-process documentation.
- Updated run commands and documentation references for the new layout:
  - `python app/depth_sandbox.py`
  - `python app/v_model_viewer.py`
  - `python -m pip install -r requirements/runtime.txt`
  - `python -m pip install -r requirements/viewer.txt`
- Added root agent guidance in `AGENTS.md` requiring impact analysis and a user-facing overview before project modifications.
- Updated calibration behavior so pressing `c` calibrates from the currently detected object/phone depth.
- Removed the fixed obstacle-risk ROI overlay and risk score from the live depth sandbox display.
- Changed calibration behavior so it is skipped when no object is detected instead of falling back to the removed ROI.
- Simplified the live display from four panels to three panels by removing the duplicate raw camera frame; the camera is now shown once with overlays.
- Routed `app/depth_sandbox.py` through the reusable perception orchestrator and added comma-separated detector selection such as `--object-detector depth-blob,yolo-phone`.
- Updated ASPICE requirements, architecture, viewer design page, and verification plan for the orchestrator traceability path.

### Added

- Added a reusable perception orchestrator module:
  - `app/perception_orchestrator.py`
  - Coordinates depth refresh, one or more object detectors, primary detection selection, and timing metadata.
  - Returns frame, depth, detections, primary detection, and timings so other apps can reuse the processing result.
- Added placeholder V-model documents for traceability and verification:
  - `docs/traceability/requirements-traceability-matrix.md`
  - `docs/verification/test-plan.md`
  - `docs/verification/acceptance-criteria.md`
- Added this changelog.

### Verification

- Ran stale-reference scans for old moved paths after the folder reorganization.
- Compiled `app/depth_sandbox.py` with the `depth-sandbox` Conda environment after the calibration and overlay changes.
- Compiled `app/depth_sandbox.py`, `app/perception_orchestrator.py`, and `app/v_model_viewer.py` with `py_compile`.
- Ran a no-camera orchestrator smoke check with a dummy depth estimator and depth-blob detector.
