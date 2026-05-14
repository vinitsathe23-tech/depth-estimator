from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Protocol

import cv2
import numpy as np


OUTPUT_DIR = Path("data/output")
YOLO_CONFIG_DIR = Path("data/yolo_config")
DEPTH_ANYTHING_MODEL_ID = "depth-anything/Depth-Anything-V2-Small-hf"
EPSILON = 1e-6
HORIZONTAL_FOV_DEG = 70.0


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


def parse_source(raw_source: str) -> int | str:
    """Allow webcam indices like 0 while keeping file paths as strings."""
    try:
        return int(raw_source)
    except ValueError:
        return raw_source


class PseudoDepthEstimator:
    def estimate(self, frame: np.ndarray) -> np.ndarray:
        return estimate_pseudo_depth(frame)


class DepthAnythingEstimator:
    def __init__(self, device: str = "auto") -> None:
        try:
            import torch
            import torch.nn.functional as F
            from PIL import Image
            from transformers import AutoImageProcessor, AutoModelForDepthEstimation
        except ImportError as exc:
            raise RuntimeError(
                "Depth Anything backend needs torch, Pillow, and transformers. "
                "Install the GPU setup from README.md first."
            ) from exc

        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.torch = torch
        self.interpolate = F.interpolate
        self.image_cls = Image
        self.device = torch.device(device)
        self.processor = AutoImageProcessor.from_pretrained(DEPTH_ANYTHING_MODEL_ID)
        self.model = AutoModelForDepthEstimation.from_pretrained(DEPTH_ANYTHING_MODEL_ID)
        self.model.to(self.device)
        self.model.eval()

        print(f"Depth Anything v2 Small loaded on {self.device}")

    def estimate(self, frame: np.ndarray) -> np.ndarray:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = self.image_cls.fromarray(rgb)

        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with self.torch.no_grad():
            outputs = self.model(**inputs)
            predicted_depth = outputs.predicted_depth

        prediction = self.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        )

        depth = prediction.squeeze().detach().cpu().numpy().astype(np.float32)
        return cv2.normalize(depth, None, 0.0, 1.0, cv2.NORM_MINMAX)


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


def estimate_pseudo_depth(frame: np.ndarray) -> np.ndarray:
    """Return a normalized depth-like map using cheap image cues.

    This is a runnable placeholder for a learned monocular depth model. Brighter,
    lower, and more textured regions are treated as more likely to be nearby.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    edges = cv2.Canny(gray, threshold1=40, threshold2=120)
    edges = cv2.GaussianBlur(edges, (11, 11), 0)

    height, width = gray.shape
    vertical_prior = np.linspace(0.15, 1.0, height, dtype=np.float32)[:, None]
    vertical_prior = np.repeat(vertical_prior, width, axis=1)

    brightness = gray.astype(np.float32) / 255.0
    texture = edges.astype(np.float32) / 255.0

    pseudo_depth = (0.45 * vertical_prior) + (0.35 * texture) + (0.20 * brightness)
    return cv2.normalize(pseudo_depth, None, 0.0, 1.0, cv2.NORM_MINMAX)


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
        roi_depth = float(np.mean(depth[y : y + h, x : x + w]))
        candidates.append((roi_depth, contour))

    if not candidates:
        return None

    _score, contour = max(candidates, key=lambda item: item[0])
    x, y, w, h = cv2.boundingRect(contour)
    center = (x + (w // 2), y + (h // 2))
    relative_depth = float(np.mean(depth[y : y + h, x : x + w]))
    distance_m = estimate_distance_meters(relative_depth, calibration_scale)
    x_m = estimate_lateral_position_meters(center[0], width, distance_m)

    return DetectedObject((x, y, w, h), center, relative_depth, distance_m, x_m)


def build_risk_overlay(
    frame: np.ndarray,
    depth: np.ndarray,
    calibration_scale: float | None,
    detected: DetectedObject | None,
) -> tuple[np.ndarray, float, float | None]:
    height, width = depth.shape

    roi_x1 = int(width * 0.35)
    roi_x2 = int(width * 0.65)
    roi_y1 = int(height * 0.60)
    roi_y2 = int(height * 0.95)

    roi = depth[roi_y1:roi_y2, roi_x1:roi_x2]
    risk = float(np.mean(roi))
    distance_m = estimate_distance_meters(risk, calibration_scale)

    overlay = frame.copy()
    color = (0, 220, 0)
    label = "LOW"
    if risk > 0.62:
        color = (0, 0, 255)
        label = "HIGH"
    elif risk > 0.48:
        color = (0, 180, 255)
        label = "MED"

    cv2.rectangle(overlay, (roi_x1, roi_y1), (roi_x2, roi_y2), color, 2)
    cv2.putText(
        overlay,
        f"Obstacle risk: {label} ({risk:.2f})",
        (24, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2,
        cv2.LINE_AA,
    )
    if distance_m is not None:
        cv2.putText(
            overlay,
            f"Estimated distance: {distance_m:.2f} m",
            (24, 76),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2,
            cv2.LINE_AA,
        )

    if detected is not None:
        x, y, w, h = detected.bbox
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.circle(overlay, detected.center, 5, (255, 255, 255), -1)
        label = detected.label
        if detected.confidence is not None:
            label = f"{label} {detected.confidence:.2f}"
        if detected.distance_m is not None and detected.x_m is not None:
            object_label = f"{label}: z={detected.distance_m:.2f}m x={detected.x_m:+.2f}m"
        else:
            object_label = f"{label}: relative depth {detected.relative_depth:.2f}"
        cv2.putText(
            overlay,
            object_label,
            (24, 112),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
    else:
        cv2.putText(
            overlay,
            "Distance: uncalibrated",
            (24, 76),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (220, 220, 220),
            2,
            cv2.LINE_AA,
        )
    return overlay, risk, distance_m


def draw_position_plot(detected: DetectedObject | None, height: int = 360, width: int = 360) -> np.ndarray:
    plot = np.full((height, width, 3), 24, dtype=np.uint8)

    origin = (width // 2, height - 36)
    max_distance_m = 5.0
    max_lateral_m = 2.5

    cv2.line(plot, (origin[0], 24), origin, (90, 90, 90), 1)
    cv2.line(plot, (24, origin[1]), (width - 24, origin[1]), (90, 90, 90), 1)

    for distance_m in range(1, int(max_distance_m) + 1):
        y = int(origin[1] - (distance_m / max_distance_m) * (height - 72))
        cv2.line(plot, (24, y), (width - 24, y), (55, 55, 55), 1)
        cv2.putText(plot, f"{distance_m}m", (28, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)

    cv2.circle(plot, origin, 7, (255, 255, 255), -1)
    cv2.putText(plot, "camera", (origin[0] - 34, origin[1] + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)

    if detected is not None and detected.distance_m is not None and detected.x_m is not None:
        clamped_z = min(max(detected.distance_m, 0.0), max_distance_m)
        clamped_x = min(max(detected.x_m, -max_lateral_m), max_lateral_m)
        px = int(origin[0] + (clamped_x / max_lateral_m) * ((width / 2) - 28))
        py = int(origin[1] - (clamped_z / max_distance_m) * (height - 72))

        cv2.circle(plot, (px, py), 10, (0, 220, 255), -1)
        cv2.line(plot, origin, (px, py), (0, 160, 255), 2)
        cv2.putText(plot, f"x {detected.x_m:+.2f}m", (18, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (230, 230, 230), 2)
        cv2.putText(plot, f"z {detected.distance_m:.2f}m", (18, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (230, 230, 230), 2)
        cv2.putText(plot, detected.label, (18, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (230, 230, 230), 2)
    else:
        cv2.putText(plot, "No calibrated object", (54, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (180, 180, 180), 2)

    return plot


def compose_view(
    frame: np.ndarray,
    depth: np.ndarray,
    overlay: np.ndarray,
    detected: DetectedObject | None,
) -> np.ndarray:
    depth_u8 = (depth * 255).astype(np.uint8)
    heatmap = cv2.applyColorMap(depth_u8, cv2.COLORMAP_TURBO)

    target_height = 360
    views = []
    position_plot = draw_position_plot(detected, target_height, 360)
    for image in (frame, heatmap, overlay, position_plot):
        scale = target_height / image.shape[0]
        resized = cv2.resize(image, (int(image.shape[1] * scale), target_height))
        views.append(resized)

    return np.hstack(views)


def save_snapshot(view: np.ndarray) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUT_DIR / f"depth_sandbox_{timestamp}.jpg"
    cv2.imwrite(str(path), view)
    return path


def create_estimator(backend: str, device: str) -> DepthEstimator:
    if backend == "pseudo":
        return PseudoDepthEstimator()
    if backend == "depth-anything":
        return DepthAnythingEstimator(device=device)
    raise ValueError(f"Unknown backend: {backend}")


def run(
    source: int | str,
    backend: str,
    device: str,
    depth_every: int,
    known_distance_m: float,
    object_detector: str,
    detect_every: int,
    yolo_confidence: float,
) -> None:
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Could not open source: {source}")

    estimator = create_estimator(backend, device)
    phone_detector = PhoneDetector(device=device, confidence=yolo_confidence) if object_detector == "yolo-phone" else None
    frame_index = 0
    last_depth: np.ndarray | None = None
    last_detected: DetectedObject | None = None
    calibration_scale: float | None = None

    print("Controls: q = quit, s = save snapshot, c = calibrate distance")
    print(f"Distance calibration target: {known_distance_m:.2f} m")

    while True:
        ok, frame = capture.read()
        if not ok:
            break

        if last_depth is None or frame_index % depth_every == 0:
            last_depth = estimator.estimate(frame)

        depth = last_depth
        if object_detector == "depth-blob":
            last_detected = detect_nearest_object(depth, calibration_scale)
        elif object_detector == "yolo-phone" and phone_detector is not None:
            if frame_index % detect_every == 0:
                last_detected = phone_detector.detect(frame, depth, calibration_scale)
        else:
            last_detected = None

        overlay, risk, _distance_m = build_risk_overlay(frame, depth, calibration_scale, last_detected)
        detected = last_detected
        view = compose_view(frame, depth, overlay, detected)
        frame_index += 1

        cv2.imshow("Monocular Depth Sandbox", view)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        if key == ord("s"):
            saved_path = save_snapshot(view)
            print(f"Saved {saved_path}")
        if key == ord("c"):
            calibration_scale = known_distance_m * max(risk, EPSILON)
            print(
                "Calibrated distance scale "
                f"using ROI depth {risk:.3f} at {known_distance_m:.2f} m"
            )

    capture.release()
    cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description="Real-time monocular depth sandbox.")
    parser.add_argument(
        "--source",
        default="0",
        help="Webcam index such as 0, or a path to a video file.",
    )
    parser.add_argument(
        "--backend",
        choices=("pseudo", "depth-anything"),
        default="pseudo",
        help="Depth backend. Use pseudo first, then depth-anything once dependencies are installed.",
    )
    parser.add_argument(
        "--device",
        default="auto",
        help="Torch device for Depth Anything: auto, cuda, or cpu.",
    )
    parser.add_argument(
        "--depth-every",
        type=int,
        default=3,
        help="Run learned depth every N frames and reuse the last depth map between runs.",
    )
    parser.add_argument(
        "--known-distance-m",
        type=float,
        default=1.0,
        help="Known distance for calibration. Put an object in the ROI at this distance and press c.",
    )
    parser.add_argument(
        "--object-detector",
        choices=("none", "depth-blob", "yolo-phone"),
        default="depth-blob",
        help="Object detector used for the bounding box and position plot.",
    )
    parser.add_argument(
        "--detect-every",
        type=int,
        default=3,
        help="Run YOLO every N frames and reuse the last phone detection between runs.",
    )
    parser.add_argument(
        "--yolo-confidence",
        type=float,
        default=0.35,
        help="YOLO confidence threshold for phone detection.",
    )
    args = parser.parse_args()

    if args.depth_every < 1:
        raise ValueError("--depth-every must be at least 1")

    if args.known_distance_m <= 0:
        raise ValueError("--known-distance-m must be positive")
    if args.detect_every < 1:
        raise ValueError("--detect-every must be at least 1")
    if not 0.0 < args.yolo_confidence <= 1.0:
        raise ValueError("--yolo-confidence must be in the range (0, 1]")

    run(
        parse_source(args.source),
        args.backend,
        args.device,
        args.depth_every,
        args.known_distance_m,
        args.object_detector,
        args.detect_every,
        args.yolo_confidence,
    )


if __name__ == "__main__":
    main()
