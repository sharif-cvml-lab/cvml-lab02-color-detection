import threading
import time

import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal

from annotation import annotate_detections
from color_detection import detect_color_objects
from config import CAPTURE_HEIGHT, CAPTURE_WIDTH, DetectionParameters, TARGET_FPS


class VideoThread(QThread):
    """Capture webcam frames and run color detection off the GUI thread."""

    frame_ready = pyqtSignal(object, object, object, int, float)
    camera_status = pyqtSignal(str)

    def __init__(self, camera_index: int = 0, parent=None):
        super().__init__(parent)
        self._camera_index = camera_index
        self._parameters = DetectionParameters(
            lower_hsv=(160, 100, 100),
            upper_hsv=(10, 255, 255),
            min_area=500,
            kernel_size=5,
            kernel_shape="rectangle",
            opening_enabled=True,
            opening_iterations=1,
            closing_enabled=True,
            closing_iterations=1,
        )
        self._lock = threading.Lock()
        self._running = threading.Event()
        self._running.set()
        self._paused = False
        self._last_camera_message = ""

    def set_parameters(self, parameters: DetectionParameters) -> None:
        with self._lock:
            self._parameters = parameters

    def set_camera_index(self, camera_index: int) -> None:
        with self._lock:
            self._camera_index = camera_index

    def set_paused(self, paused: bool) -> None:
        with self._lock:
            self._paused = paused

    def _snapshot(self) -> tuple[DetectionParameters, int, bool]:
        with self._lock:
            return self._parameters, self._camera_index, self._paused

    def _emit_camera_status(self, message: str) -> None:
        if message != self._last_camera_message:
            self._last_camera_message = message
            self.camera_status.emit(message)

    def run(self) -> None:
        cap = None
        opened_index = None
        frame_period = 1.0 / TARGET_FPS

        try:
            while self._running.is_set():
                parameters, requested_index, paused = self._snapshot()

                if cap is None or opened_index != requested_index:
                    if cap is not None:
                        cap.release()
                    cap = cv2.VideoCapture(requested_index)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)
                    opened_index = requested_index

                    if not cap.isOpened():
                        self._emit_camera_status(
                            f"Camera {requested_index} is unavailable. Retrying..."
                        )
                        cap.release()
                        cap = None
                        time.sleep(1.0)
                        continue

                    self._emit_camera_status(f"Camera {requested_index} connected")

                loop_started = time.perf_counter()
                ret, frame = cap.read()

                if not ret:
                    self._emit_camera_status("Camera frame read failed. Reconnecting...")
                    cap.release()
                    cap = None
                    opened_index = None
                    time.sleep(0.25)
                    continue

                if paused:
                    self._emit_camera_status("Camera paused")
                    time.sleep(frame_period)
                    continue

                processing_outputs: dict[str, np.ndarray] = {}
                bboxes = detect_color_objects(
                    frame=frame,
                    lower_hsv=parameters.lower_hsv,
                    upper_hsv=parameters.upper_hsv,
                    min_area=parameters.min_area,
                    kernel_size=parameters.kernel_size,
                    kernel_shape=parameters.kernel_shape,
                    opening_enabled=parameters.opening_enabled,
                    opening_iterations=parameters.opening_iterations,
                    closing_enabled=parameters.closing_enabled,
                    closing_iterations=parameters.closing_iterations,
                    processing_outputs=processing_outputs,
                )

                raw_mask = processing_outputs.get(
                    "raw_mask", np.zeros(frame.shape[:2], dtype=np.uint8)
                )
                final_mask = processing_outputs.get(
                    "final_mask", np.zeros(frame.shape[:2], dtype=np.uint8)
                )
                annotated = annotate_detections(frame, bboxes)

                elapsed = time.perf_counter() - loop_started
                fps = 1.0 / elapsed if elapsed > 0 else TARGET_FPS
                self.frame_ready.emit(annotated, raw_mask, final_mask, len(bboxes), fps)

                time.sleep(max(0.0, frame_period - elapsed))
        finally:
            if cap is not None:
                cap.release()
            self._emit_camera_status("Camera stopped")

    def stop(self) -> None:
        self._running.clear()
        self.wait()
