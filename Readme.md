# Lab02_ColorDetection

Welcome to the second assignment of the Computer Vision and Machine Learning lab course!

This project provides a real-time PyQt6 application for color segmentation and object detection using OpenCV. The goal of this lab is to understand HSV color thresholding, binary masks, morphological operations, contour analysis, and bounding boxes through an interactive webcam application.

## 🎯 Assignment Objectives

In this lab, you will complete one specific image-processing function located in `color_detection.py`:

```python
detect_color_objects(...)
```

Students should modify only `color_detection.py`. Do not modify `main.py`, `gui.py`, `video_thread.py`, `annotation.py`, `config.py`, or any other project file.

The expected processing pipeline is:

```text
Camera Frame
     ↓
BGR → HSV
     ↓
Color Thresholding
     ↓
Raw Mask
     ↓
Opening (optional)
     ↓
Closing (optional)
     ↓
Final Mask
     ↓
Contour Detection
     ↓
Bounding Boxes
```


## ✨ Features

- Real-time webcam color detection with PyQt6.
- Three synchronized views: **Original**, **Raw Mask**, and **Final Mask**.
- Live HSV controls with visible current values.
- Red, green, blue, and yellow quick presets.
- Configurable minimum contour area.
- Configurable morphology kernel shape: rectangle, ellipse, or cross.
- Configurable odd kernel size and opening/closing iteration counts.
- Opening and closing can be enabled independently.
- Bounding-box annotation is implemented outside the student function.
- Dark mode and light mode.
- Full-screen mode and responsive scaling.
- High-DPI support for modern displays.
- Camera pause, restart, and camera-index selection.
- Settings are restored automatically between sessions.
- Reset-to-default button.
- FPS and detection-count indicators.

## 🛠️ Setup & Installation

1. Clone the repository and navigate to the project directory.

2. Create a virtual environment (recommended):

```bash
python -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## 🎮 Using the Application

### HSV controls

Use the six HSV sliders to define the color range. The numerical value next to every slider always shows the current setting.

Hue uses OpenCV's range `0..179`, while Saturation and Value use `0..255`.

The implementation must support Hue wrap-around. This is required for colors such as red, whose useful Hue range can cross the `179 → 0` boundary.

### Morphology controls

The application shows the mask immediately after color thresholding as **Raw Mask**. After that, the configured morphology pipeline is applied and displayed as **Final Mask**.

The application currently applies operations in this fixed order:

1. Opening
2. Closing

Students can experiment with:

- Kernel shape
- Kernel size
- Opening enabled/disabled
- Opening iterations
- Closing enabled/disabled
- Closing iterations

Observe how each change affects noise, holes, object boundaries, and the final detections.

### Detection filter

`Min area` removes contours that are too small to be considered detected objects.

## 📂 Repository Structure

```text
cvml-lab02-color-detection/
├── .gitignore
├── Readme.md
├── requirements.txt
├── main.py
├── gui.py
├── video_thread.py
├── annotation.py
├── config.py
└── color_detection.py      # The only file students should modify
```

### Module responsibilities

- `main.py` — application entry point only.
- `gui.py` — PyQt6 user interface, controls, themes, persistence, and rendering.
- `video_thread.py` — camera capture and real-time processing loop.
- `annotation.py` — bounding-box visualization.
- `config.py` — constants, presets, and shared parameter definitions.
- `color_detection.py` — the student implementation of the color-detection algorithm.

## ⌨️ Keyboard Shortcuts

- `Space` — Pause / Resume
- `F11` — Full Screen / Windowed
- `R` — Reset Defaults
- `Q` — Quit
