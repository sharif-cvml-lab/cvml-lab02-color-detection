from dataclasses import dataclass

APP_NAME = "CVML Lab 02 - Color Detection"
ORGANIZATION_NAME = "Sharif CVML Lab"

CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
TARGET_FPS = 30

DEFAULT_LOWER_HSV = (160, 100, 100)
DEFAULT_UPPER_HSV = (10, 255, 255)
DEFAULT_MIN_AREA = 500
DEFAULT_KERNEL_SIZE = 5
DEFAULT_KERNEL_SHAPE = "rectangle"
DEFAULT_OPENING_ENABLED = True
DEFAULT_OPENING_ITERATIONS = 1
DEFAULT_CLOSING_ENABLED = True
DEFAULT_CLOSING_ITERATIONS = 1
DEFAULT_CAMERA_INDEX = 0
DEFAULT_THEME = "dark"

HSV_PRESETS = {
    "Red": ((160, 100, 100), (10, 255, 255)),
    "Green": ((35, 80, 100), (85, 255, 255)),
    "Blue": ((100, 100, 100), (130, 255, 255)),
    "Yellow": ((20, 100, 100), (35, 255, 255)),
}

KERNEL_SHAPES = {
    "rectangle": "Rectangle",
    "ellipse": "Ellipse",
    "cross": "Cross",
}


@dataclass(frozen=True)
class DetectionParameters:
    lower_hsv: tuple[int, int, int]
    upper_hsv: tuple[int, int, int]
    min_area: int
    kernel_size: int
    kernel_shape: str
    opening_enabled: bool
    opening_iterations: int
    closing_enabled: bool
    closing_iterations: int
