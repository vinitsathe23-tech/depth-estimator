from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import cv2
import numpy as np


YOLO_CONFIG_DIR = Path("data/yolo_config")
EPSILON = 1e-6
HORIZONTAL_FOV_DEG = 70.0
VALID_OBJECT_DETECTORS = ("none", "depth-blob", "yolo-phone")


@dataclass
class PerceptionResult:
    frame: np.ndarray
    depth: np.ndarray
    detections: list["DetectedObject"]
    primary_detection: "DetectedObject | None"
    timings_ms: dict[str, float]


class DetectedObject:
    def __init__(
        self,
        bbox: tuple[int, int, int, int],
        center: tuple[int, int],
        relative_depth: float,
        distance_m: float | None,
        x_m: float | None,
        label: str = "object",
        confidence: float | None = None,
    ) -> None:
        self.bbox = bbox
        self.center = center
        self.relative_depth = relative_depth
        self.distance_m = distance_m
        self.x_m = x_m
        self.label = label
        self.confidence = confidence


class DepthEstimator(Protocol):
    def estimate(self, frame: np.ndarray) -> np.ndarray:
        ...


class ObjectDetector(Protocol):
    name: str

    def detect(
        self,
        frame: np.ndarray,
        depth: np.ndarray,
        calibration_scale: float | None,
    ) -> list[DetectedObject]:
        ...


def parse_object_detectors(raw_detectors: str) -> tuple[str, ...]:
    detectors = tuple(name.strip() for name in raw_detectors.split(",") if name.strip())
    if not detectors:
        raise ValueError("--object-detector must include at least one detector name")

    invalid = sorted(set(detectors) - set(VALID_OBJECT_DETECTORS))
    if invalid:
        valid = ", ".join(VALID_OBJECT_DETECTORS)
        raise ValueError(f"Unknown object detector(s): {', '.join(invalid)}. Valid options: {valid}")

    if "none" in detectors and len(detectors) > 1:
        raise ValueError("--object-detector none cannot be combined with other detectors")

    return detectors


def estimate_distance_meters(relative_depth: float, calibration_scale: float | None) -> float | None:
    if calibration_scale is None:
        return None
    return calibration_scale / max(relative_depth, EPSILON)


def estimate_lateral_position_meters(
    center_x: int,
    image_width: int,
    distance_m: float | None,
) -> float | None:
    if distance_m is None:
        return None

    focal_px = (image_width / 2.0) / np.tan(np.deg2rad(HORIZONTAL_FOV_DEG) / 2.0)
    return ((center_x - (image_width / 2.0)) / focal_px) * distance_m


class PhoneDetector:
    def __init__(self, device: str = "auto", confidence: float = 0.35) -> None:
        YOLO_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("YOLO_CONFIG_DIR", str(YOLO_CONFIG_DIR.resolve()))

        try:
            import torch
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                "YOLO phone detection needs ultralytics and torch. "
                "Install the updated requirements.txt first."
            ) from exc

        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = YOLO("yolov8n.pt")
        self.device = 0 if device == "cuda" else device
        self.confidence = confidence

    def detect(self, frame: np.ndarray, depth: np.ndarray, calibration_scale: float | None) -> DetectedObject | None:
        results = self.model.predict(
            frame,
            imgsz=640,
            conf=self.confidence,
            verbose=False,
            device=self.device,
        )
        if not results:
            return None

        result = results[0]
        names = result.names
        best: tuple[float, tuple[int, int, int, int]] | None = None

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            class_name = str(names.get(class_id, class_id))
            if class_name != "cell phone":
                continue

            conf = float(box.conf[0].item())
            x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
            x1 = max(0, min(x1, frame.shape[1] - 1))
            x2 = max(0, min(x2, frame.shape[1] - 1))
            y1 = max(0, min(y1, frame.shape[0] - 1))
            y2 = max(0, min(y2, frame.shape[0] - 1))

            if x2 <= x1 or y2 <= y1:
                continue

            if best is None or conf > best[0]:
                best = (conf, (x1, y1, x2 - x1, y2 - y1))

        if best is None:
            return None

        confidence, bbox = best
        x, y, w, h = bbox
        center = (x + (w // 2), y + (h // 2))
        relative_depth = float(np.mean(depth[y : y + h, x : x + w]))
        distance_m = estimate_distance_meters(relative_depth, calibration_scale)
        x_m = estimate_lateral_position_meters(center[0], frame.shape[1], distance_m)

        return DetectedObject(
            bbox=bbox,
            center=center,
            relative_depth=relative_depth,
            distance_m=distance_m,
            x_m=x_m,
            label="phone",
            confidence=confidence,
        )


def detect_nearest_object(
    depth: np.ndarray,
    calibration_scale: float | None,
) -> DetectedObject | None:
    height, width = depth.shape
    depth_u8 = (depth * 255).astype(np.uint8)

    threshold_value = int(max(150, np.percentile(depth_u8, 88)))
    _, mask = cv2.threshold(depth_u8, threshold_value, 255, cv2.THRESH_BINARY)

    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates: list[tuple[float, np.ndarray]] = []

    min_area = max(300, int(width * height * 0.003))
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        if w < 12 or h < 12:
            continue
        candidate_depth = float(np.mean(depth[y : y + h, x : x + w]))
        candidates.append((candidate_depth, contour))

    if not candidates:
        return None

    _score, contour = max(candidates, key=lambda item: item[0])
    x, y, w, h = cv2.boundingRect(contour)
    center = (x + (w // 2), y + (h // 2))
    relative_depth = float(np.mean(depth[y : y + h, x : x + w]))
    distance_m = estimate_distance_meters(relative_depth, calibration_scale)
    x_m = estimate_lateral_position_meters(center[0], width, distance_m)

    return DetectedObject((x, y, w, h), center, relative_depth, distance_m, x_m)


class DepthBlobDetector:
    name = "depth-blob"

    def detect(
        self,
        frame: np.ndarray,
        depth: np.ndarray,
        calibration_scale: float | None,
    ) -> list[DetectedObject]:
        detected = detect_nearest_object(depth, calibration_scale)
        return [detected] if detected is not None else []


class YoloPhoneDetectorBackend:
    name = "yolo-phone"

    def __init__(self, device: str, confidence: float) -> None:
        self.detector = PhoneDetector(device=device, confidence=confidence)

    def detect(
        self,
        frame: np.ndarray,
        depth: np.ndarray,
        calibration_scale: float | None,
    ) -> list[DetectedObject]:
        detected = self.detector.detect(frame, depth, calibration_scale)
        return [detected] if detected is not None else []


def create_object_detectors(
    detector_names: tuple[str, ...],
    device: str,
    yolo_confidence: float,
) -> list[ObjectDetector]:
    detectors: list[ObjectDetector] = []
    for detector_name in detector_names:
        if detector_name == "none":
            continue
        if detector_name == "depth-blob":
            detectors.append(DepthBlobDetector())
        elif detector_name == "yolo-phone":
            detectors.append(YoloPhoneDetectorBackend(device=device, confidence=yolo_confidence))
        else:
            raise ValueError(f"Unknown object detector: {detector_name}")
    return detectors


class PerceptionOrchestrator:
    def __init__(
        self,
        estimator: DepthEstimator,
        detectors: list[ObjectDetector],
        depth_every: int,
        detect_every: int,
    ) -> None:
        self.estimator = estimator
        self.detectors = detectors
        self.depth_every = depth_every
        self.detect_every = detect_every
        self.frame_index = 0
        self.last_depth: np.ndarray | None = None
        self.last_detections_by_detector: dict[str, list[DetectedObject]] = {}

    def process_frame(self, frame: np.ndarray, calibration_scale: float | None) -> PerceptionResult:
        timings_ms: dict[str, float] = {}

        depth_start = time.perf_counter()
        if self.last_depth is None or self.frame_index % self.depth_every == 0:
            self.last_depth = self.estimator.estimate(frame)
        timings_ms["depth"] = (time.perf_counter() - depth_start) * 1000.0

        depth = self.last_depth
        detections: list[DetectedObject] = []
        for detector in self.detectors:
            detector_start = time.perf_counter()
            should_refresh = detector.name != "yolo-phone" or self.frame_index % self.detect_every == 0
            if should_refresh:
                self.last_detections_by_detector[detector.name] = detector.detect(
                    frame,
                    depth,
                    calibration_scale,
                )
            timings_ms[detector.name] = (time.perf_counter() - detector_start) * 1000.0
            detections.extend(self.last_detections_by_detector.get(detector.name, []))

        primary_detection = detections[0] if detections else None
        self.frame_index += 1

        return PerceptionResult(
            frame=frame,
            depth=depth,
            detections=detections,
            primary_detection=primary_detection,
            timings_ms=timings_ms,
        )
