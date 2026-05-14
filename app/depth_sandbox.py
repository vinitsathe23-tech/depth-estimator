from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

try:
    from perception_orchestrator import (
        DepthEstimator,
        DetectedObject,
        EPSILON,
        PerceptionOrchestrator,
        create_object_detectors,
        parse_object_detectors,
    )
except ImportError:
    from app.perception_orchestrator import (
        DepthEstimator,
        DetectedObject,
        EPSILON,
        PerceptionOrchestrator,
        create_object_detectors,
        parse_object_detectors,
    )


OUTPUT_DIR = Path("data/output")
DEPTH_ANYTHING_MODEL_ID = "depth-anything/Depth-Anything-V2-Small-hf"


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


def build_detection_overlay(
    frame: np.ndarray,
    detected: DetectedObject | None,
) -> np.ndarray:
    overlay = frame.copy()

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
            (24, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
    else:
        cv2.putText(
            overlay,
            "No detected object",
            (24, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (220, 220, 220),
            2,
            cv2.LINE_AA,
        )
    return overlay


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
    depth: np.ndarray,
    overlay: np.ndarray,
    detected: DetectedObject | None,
) -> np.ndarray:
    depth_u8 = (depth * 255).astype(np.uint8)
    heatmap = cv2.applyColorMap(depth_u8, cv2.COLORMAP_TURBO)

    target_height = 360
    views = []
    position_plot = draw_position_plot(detected, target_height, 360)
    for image in (overlay, heatmap, position_plot):
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
    detector_names = parse_object_detectors(object_detector)
    detectors = create_object_detectors(detector_names, device, yolo_confidence)
    orchestrator = PerceptionOrchestrator(
        estimator=estimator,
        detectors=detectors,
        depth_every=depth_every,
        detect_every=detect_every,
    )
    calibration_scale: float | None = None

    print("Controls: q = quit, s = save snapshot, c = calibrate distance")
    print(f"Distance calibration target: {known_distance_m:.2f} m")
    print(f"Object detectors: {', '.join(detector_names)}")

    while True:
        ok, frame = capture.read()
        if not ok:
            break

        result = orchestrator.process_frame(frame, calibration_scale)
        detected = result.primary_detection
        overlay = build_detection_overlay(result.frame, detected)
        view = compose_view(result.depth, overlay, detected)

        cv2.imshow("Monocular Depth Sandbox", view)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        if key == ord("s"):
            saved_path = save_snapshot(view)
            print(f"Saved {saved_path}")
        if key == ord("c"):
            if detected is not None:
                calibration_depth = max(detected.relative_depth, EPSILON)
                calibration_scale = known_distance_m * calibration_depth
                print(
                    "Calibrated distance scale "
                    f"using detected {detected.label} depth {calibration_depth:.3f} "
                    f"at {known_distance_m:.2f} m"
                )
            else:
                print("Calibration skipped: no detected object. Wait for a box, then press c.")

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
        help="Known distance for calibration. Put a detected object at this distance and press c.",
    )
    parser.add_argument(
        "--object-detector",
        default="depth-blob",
        help="Object detector(s) used for the bounding box and position plot: none, depth-blob, yolo-phone, or comma-separated combinations.",
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
