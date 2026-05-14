# Software Requirements Specification (SWE-REQ)

**Document ID**: SWE-REQ-001  
**Version**: 1.0  
**Date**: May 2026  
**Status**: Active

## 1. Introduction

This document specifies software requirements derived from system requirements. It focuses on software-specific functional and non-functional requirements for the Monocular Depth Sandbox application.

## 2. Software Functional Requirements

### 2.1 Input Management (SWE-REQ-I)

| ID | Requirement | Traceability |
|----|----|---|
| **SWE-F-I-001** | Parse and validate video source input (webcam index or file path) | SYS-F-001 |
| **SWE-F-I-002** | Open and validate video capture from webcam using camera index | SYS-F-001 |
| **SWE-F-I-003** | Open and validate video file from file path | SYS-F-001 |
| **SWE-F-I-004** | Handle input errors gracefully (camera not available, file not found) | SYS-NF-005 |
| **SWE-F-I-005** | Support configurable frame resolution and capture rate | SYS-NF-004 |

### 2.2 Depth Estimation (SWE-REQ-D)

| ID | Requirement | Traceability |
|----|----|---|
| **SWE-F-D-001** | Implement pseudo-depth backend using OpenCV edge/corner detection | SYS-F-002 |
| **SWE-F-D-002** | Implement AI-based depth backend using Depth Anything v2 Small | SYS-F-002 |
| **SWE-F-D-003** | Load and cache depth model on first use to minimize latency | SYS-NF-001 |
| **SWE-F-D-004** | Normalize depth output to 0-1 range for consistent processing | SYS-F-002 |
| **SWE-F-D-005** | Handle GPU/CPU fallback if model unavailable | SYS-NF-005 |
| **SWE-F-D-006** | Support batch processing for multiple frames | SYS-NF-001 |

### 2.3 Object Detection (SWE-REQ-OD)

| ID | Requirement | Traceability |
|----|----|---|
| **SWE-F-OD-001** | Implement depth-blob detector using contour analysis on normalized depth | SYS-F-003 |
| **SWE-F-OD-002** | Implement YOLO-based phone detector with class filtering | SYS-F-003 |
| **SWE-F-OD-003** | Load YOLO model from Ultralytics configuration | SYS-F-003 |
| **SWE-F-OD-004** | Return detection as: bounding box, center point, confidence | SYS-F-003 |
| **SWE-F-OD-005** | Handle no-detection case gracefully | SYS-NF-005 |
| **SWE-F-OD-006** | Support confidence threshold filtering | SYS-F-003 |

### 2.4 Distance Estimation (SWE-REQ-DE)

| ID | Requirement | Traceability |
|----|----|---|
| **SWE-F-DE-001** | Extract relative depth value from detection region (average, min, median) | SYS-F-002, SYS-F-003 |
| **SWE-F-DE-002** | Perform one-point calibration: map relative depth to known distance in meters | SYS-F-004 |
| **SWE-F-DE-003** | Calculate 3D position (x lateral, z forward) from depth and detection center | SYS-F-005 |
| **SWE-F-DE-004** | Apply field-of-view calculation to convert pixel offset to meters | SYS-F-005 |
| **SWE-F-DE-005** | Store calibration state for persistence across frames | SYS-F-004 |
| **SWE-F-DE-006** | Support recalibration on demand | SYS-F-004 |

### 2.5 Visualization (SWE-REQ-V)

| ID | Requirement | Traceability |
|----|----|---|
| **SWE-F-V-001** | Display original frame in main output panel | SYS-F-006 |
| **SWE-F-V-002** | Display depth heatmap with color gradient (dark=near, bright=far) | SYS-F-006 |
| **SWE-F-V-003** | Display detection bounding box and center marker on original frame | SYS-F-006 |
| **SWE-F-V-004** | Display distance estimate overlay on detection panel | SYS-F-006 |
| **SWE-F-V-005** | Display top-down position plot with object trajectory | SYS-F-006 |
| **SWE-F-V-006** | Update visualization at same rate as frame capture (no lag) | SYS-NF-001 |
| **SWE-F-V-007** | Support window resizing without losing display quality | SYS-F-006 |

### 2.6 Data Output (SWE-REQ-O)

| ID | Requirement | Traceability |
|----|----|---|
| **SWE-F-O-001** | Save processed frame snapshots to output directory | SYS-F-007 |
| **SWE-F-O-002** | Save position data (timestamp, x, z, confidence) to CSV or JSON | SYS-F-007 |
| **SWE-F-O-003** | Create timestamped output files to avoid overwriting | SYS-F-007 |
| **SWE-F-O-004** | Implement optional video output (MP4/AVI) with overlays | SYS-F-007 |

### 2.7 Configuration & CLI (SWE-REQ-C)

| ID | Requirement | Traceability |
|----|----|---|
| **SWE-F-C-001** | Parse command-line arguments for video source, detector, depth backend | SYS-F-008 |
| **SWE-F-C-002** | Support configuration file for persistent settings (YAML/JSON) | SYS-F-008 |
| **SWE-F-C-003** | Provide comprehensive help and usage documentation | SYS-NF-006 |
| **SWE-F-C-004** | Support runtime calibration trigger (keyboard input) | SYS-F-004 |
| **SWE-F-C-005** | Allow output directory configuration via CLI or config file | SYS-F-007 |

## 3. Software Non-Functional Requirements

### 3.1 Performance

| ID | Requirement | Target | Traceability |
|----|----|---|---|
| **SWE-NF-P-001** | Frame processing latency | <67ms per frame | SYS-NF-001 |
| **SWE-NF-P-002** | Model load time | <5 seconds | SYS-NF-001 |
| **SWE-NF-P-003** | Memory per frame | <50MB system, <500MB GPU | SYS-NF-008 |
| **SWE-NF-P-004** | CPU usage (idle frame) | <5% | SYS-NF-008 |

### 3.2 Code Quality

| ID | Requirement | Description | Traceability |
|----|----|---|---|
| **SWE-NF-Q-001** | Modular architecture | Separate depth, detector, calibration modules | SYS-NF-006 |
| **SWE-NF-Q-002** | Type annotations | Use Python type hints on all functions | SYS-NF-006 |
| **SWE-NF-Q-003** | Documentation | Docstrings on all public functions/classes | SYS-NF-006 |
| **SWE-NF-Q-004** | Error handling | Try/except blocks with informative messages | SYS-NF-005 |
| **SWE-NF-Q-005** | Logging | Structured logging at INFO/DEBUG/ERROR levels | SYS-NF-006 |

### 3.3 Reliability

| ID | Requirement | Description | Traceability |
|----|----|---|---|
| **SWE-NF-R-001** | No crashes | Handle all exceptions gracefully | SYS-NF-005 |
| **SWE-NF-R-002** | Robustness | Operate with missing/degraded depth data | SYS-NF-005 |
| **SWE-NF-R-003** | Recovery | Attempt automatic model reload on first failure | SYS-NF-005 |

## 4. Software Design Constraints

- Python 3.9+ only
- OpenCV backend for frame capture (cross-platform)
- PyTorch for deep learning models (GPU-accelerated)
- No external APIs or cloud services
- Local file I/O only

## 5. Software Interface Requirements

### 5.1 External Interfaces
- Webcam interface via OpenCV
- File system for config/output
- GPU via CUDA/PyTorch

### 5.2 Internal Module Interfaces
- `FrameCapture` → `DepthEstimator` (frame → depth map)
- `DepthEstimator` + `FrameCapture` → `ObjectDetector` (frame + depth → detections)
- `ObjectDetector` + `DepthMap` → `CalibrationEngine` (detection + depth → position)
- All modules → `Visualizer` (data → display)

## 6. Traceability Summary

**Total SWE Requirements**: 43  
**Mapped to SYS Requirements**: 100%  
**High Priority**: 28  
**Medium Priority**: 15

---

**Approved By**: Software Lead  
**Reviewed By**: Architecture Team  
**Next Review Date**: Q3 2026
