# System Requirements Specification (SYS-REQ)

**Document ID**: SYS-REQ-001  
**Version**: 1.0  
**Date**: May 2026  
**Status**: Active

## 1. Executive Summary

The Monocular Depth Sandbox is a real-time computer vision system designed for depth estimation and object detection. This document specifies system-level requirements covering functional capabilities, performance, usability, and quality attributes.

## 2. System Overview

The system processes video streams from webcams or files to:
- Estimate depth using AI models
- Detect specific objects (cell phones)
- Calibrate and estimate object distance
- Provide real-time visualization

## 3. System-Level Functional Requirements

| ID | Requirement | Description | Priority |
|----|----|---|---|
| **SYS-F-001** | Video Input Support | System shall support input from webcam (index 0-9) or video file paths | HIGH |
| **SYS-F-002** | Depth Estimation | System shall estimate depth map from input frame using one of: pseudo-depth (OpenCV) or AI model (Depth Anything v2) | HIGH |
| **SYS-F-003** | Object Detection | System shall detect objects in the frame using configurable detection backend (depth-blob or YOLO) | HIGH |
| **SYS-F-004** | Distance Calibration | System shall support one-point calibration to map relative depth to meters | MEDIUM |
| **SYS-F-005** | Position Estimation | System shall estimate 3D position (x, z) of detected object in meters | HIGH |
| **SYS-F-006** | Real-Time Visualization | System shall display: camera frame with detection overlay, depth heatmap, and top-down position plot | HIGH |
| **SYS-F-007** | Output Export | System shall save processed frames and position data to configurable output directory | MEDIUM |
| **SYS-F-008** | Configuration Management | System shall support runtime configuration via command-line arguments and config files | MEDIUM |

## 4. System-Level Non-Functional Requirements

| ID | Requirement | Description | Priority |
|----|----|---|---|
| **SYS-NF-001** | Latency | System shall process and display frames at ≥15 FPS on target GPU (RTX 4060 Ti) | HIGH |
| **SYS-NF-002** | Accuracy | Depth estimates shall have ±10% accuracy compared to ground truth within 5m range | MEDIUM |
| **SYS-NF-003** | Calibration Tolerance | System shall maintain distance estimates within ±5% after single-point calibration | MEDIUM |
| **SYS-NF-004** | Scalability | System shall handle video resolutions from 640x480 to 1920x1080 | MEDIUM |
| **SYS-NF-005** | Robustness | System shall handle missing depth information gracefully without crashing | HIGH |
| **SYS-NF-006** | Code Maintainability | Code shall be documented and modular for easy modification and extension | HIGH |
| **SYS-NF-007** | Portability | System shall run on Windows with Python 3.9+ and required GPU drivers | MEDIUM |
| **SYS-NF-008** | Memory Efficiency | System shall operate within 4GB GPU VRAM on target hardware | HIGH |

## 5. Quality Attributes

### 5.1 Performance
- Frame processing latency: <67ms (for 15 FPS)
- Model initialization time: <5s
- Memory footprint: <2GB system RAM, <4GB VRAM

### 5.2 Reliability
- System uptime: >99% during operational sessions
- Error recovery: Graceful degradation on missing/corrupted data
- Crash-free operation: >1 hour continuous runtime

### 5.3 Usability
- Command-line interface with clear help documentation
- Real-time visual feedback to user
- Configurable parameters without code modification

### 5.4 Maintainability
- Modular code structure (separation of concerns)
- Comprehensive code comments and docstrings
- Version control with meaningful commit messages

## 6. Constraints and Dependencies

### 6.1 Hardware Requirements
- GPU: NVIDIA RTX 4060 Ti or equivalent (for Depth Anything v2)
- RAM: Minimum 4GB
- Storage: Minimum 2GB for models and output

### 6.2 Software Dependencies
- Python 3.9+
- OpenCV 4.5+
- PyTorch 1.9+
- Transformers library
- CUDA 11.8+ (for GPU support)

### 6.3 Environmental Constraints
- Indoor/outdoor lighting: 100-500 lux (recommended)
- Temperature: 0-40°C operational
- Data privacy: Local processing only (no cloud upload)

## 7. Acceptance Criteria

The system shall be accepted when:
1. All HIGH priority functional requirements are implemented and verified
2. Frame processing achieves ≥15 FPS on target hardware
3. Distance calibration accuracy verified within ±5% tolerance
4. System runs for 1 hour without crashes
5. All critical bugs resolved
6. Documentation complete and reviewed

## 8. Use Cases

### UC-001: Real-Time Phone Detection and Distance Estimation
**Actor**: User  
**Precondition**: System initialized, camera available  
**Main Flow**:
1. User starts application with `--detector yolo-phone`
2. System captures frames from webcam
3. System displays depth, detections, and position
4. User performs one-point calibration using known distance
5. System estimates phone distance in meters
6. Position plot updates in real-time

**Postcondition**: User sees real-time position updates with distance estimates

### UC-002: Pseudo-Depth Baseline Testing
**Actor**: Developer  
**Precondition**: System initialized  
**Main Flow**:
1. Developer starts application with `--depth-backend pseudo`
2. System uses fast OpenCV-based depth estimation
3. System detects depth discontinuities (blobs)
4. Results displayed and saved to output directory

**Postcondition**: Baseline performance metrics captured

## 9. Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Model initialization timeout | High | Medium | Implement timeout handling with fallback to pseudo-depth |
| GPU memory exhaustion | High | Medium | Monitor VRAM usage, implement frame buffering limits |
| Poor lighting conditions | Medium | Medium | Add image enhancement preprocessing |
| Calibration drift | Medium | Low | Implement recalibration mechanism |

## 10. Definitions and Acronyms

| Term | Definition |
|------|-----------|
| **FOV** | Field of View (70° horizontal assumed) |
| **YOLO** | You Only Look Once (object detection model) |
| **RTM** | Requirement Traceability Matrix |
| **SWE** | Software Engineering (ASPICE process area) |
| **GPU** | Graphics Processing Unit |
| **VRAM** | Video RAM (GPU memory) |

---

**Approved By**: Architecture Team  
**Reviewed By**: QA Team  
**Next Review Date**: Q3 2026
