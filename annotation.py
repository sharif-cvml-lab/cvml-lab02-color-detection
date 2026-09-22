import cv2
import numpy as np


def annotate_detections(
    frame: np.ndarray,
    bboxes: list[tuple[int, int, int, int]],
    color: tuple[int, int, int] = (60, 220, 140),
    thickness: int = 2,
) -> np.ndarray:
    """Draw detection bounding boxes on a copy of the input frame."""
    output = frame.copy()

    for index, (x, y, width, height) in enumerate(bboxes, start=1):
        cv2.rectangle(output, (x, y), (x + width, y + height), color, thickness)
        cv2.putText(
            output,
            str(index),
            (x, max(20, y - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
            cv2.LINE_AA,
        )

    return output
