import cv2
import numpy as np


def detect_color_objects(
    frame: np.ndarray,
    lower_hsv: tuple[int, int, int],
    upper_hsv: tuple[int, int, int],
    min_area: int,
    kernel_size: int,
    kernel_shape: str,
    opening_enabled: bool,
    opening_iterations: int,
    closing_enabled: bool,
    closing_iterations: int,
    processing_outputs: dict[str, np.ndarray],
) -> list[tuple[int, int, int, int]]:
    """
    TODO: Implement the complete color-detection pipeline.

    IMPORTANT:
    - This is the only file students should modify.
    - Keep this function signature unchanged.
    - The function must return ONLY the list of detected bounding boxes.
    - Do not draw bounding boxes in this function; annotation is handled elsewhere.
    - Store both intermediate masks in processing_outputs so the GUI can display them:
          processing_outputs["raw_mask"] = raw binary color mask
          processing_outputs["final_mask"] = mask after the requested morphology

    Expected implementation sequence:
    1. Convert the BGR input frame to HSV using cv2.cvtColor(..., cv2.COLOR_BGR2HSV).
    2. Create the raw binary color mask with cv2.inRange().
       The Hue range can wrap around 179->0. When lower_hsv[0] > upper_hsv[0],
       create two masks ([H_min..179] and [0..H_max]) and combine them with
       cv2.bitwise_or(). Otherwise, one cv2.inRange() call is enough.
    3. Save the raw mask in processing_outputs["raw_mask"].
       Do this BEFORE any morphological operation.
    4. Create the morphology kernel with cv2.getStructuringElement().
       Map kernel_shape exactly as follows:
           "rectangle" -> cv2.MORPH_RECT
           "ellipse"   -> cv2.MORPH_ELLIPSE
           "cross"     -> cv2.MORPH_CROSS
       Use (kernel_size, kernel_size) as the kernel size.
    5. If opening_enabled is True, apply Opening with cv2.morphologyEx()
       and cv2.MORPH_OPEN, using opening_iterations.
    6. If closing_enabled is True, apply Closing with cv2.morphologyEx()
       and cv2.MORPH_CLOSE, using closing_iterations.
       Apply Opening first and Closing second.
    7. Save the resulting mask in processing_outputs["final_mask"].
    8. Find contours on the final mask using:
           cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    9. For each contour, calculate cv2.contourArea(). Keep only contours whose
       area is at least min_area. Convert each accepted contour to a bounding box
       with cv2.boundingRect() and append (x, y, w, h) to the detections list.
    10. Return the detections list.

    Keep the implementation deterministic: use only the parameters provided to
    the function and do not introduce global state or GUI code here.
    """
    processing_outputs["raw_mask"] = np.zeros(frame.shape[:2], dtype=np.uint8)
    processing_outputs["final_mask"] = np.zeros(frame.shape[:2], dtype=np.uint8)
    return []
