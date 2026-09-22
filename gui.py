from __future__ import annotations

from PyQt6.QtCore import QSettings, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from config import (
    APP_NAME,
    DEFAULT_CAMERA_INDEX,
    DEFAULT_CLOSING_ENABLED,
    DEFAULT_CLOSING_ITERATIONS,
    DEFAULT_KERNEL_SHAPE,
    DEFAULT_KERNEL_SIZE,
    DEFAULT_LOWER_HSV,
    DEFAULT_MIN_AREA,
    DEFAULT_OPENING_ENABLED,
    DEFAULT_OPENING_ITERATIONS,
    DEFAULT_THEME,
    DEFAULT_UPPER_HSV,
    HSV_PRESETS,
    KERNEL_SHAPES,
    DetectionParameters,
)
from video_thread import VideoThread

DARK_STYLE = """
QMainWindow, QWidget {
    background: #11151b;
    color: #e7ebf0;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}
QFrame#Header, QFrame#SidebarCard, QFrame#VideoCard, QFrame#StatusBar {
    background: #171c23;
    border: 1px solid #28303a;
    border-radius: 12px;
}
QFrame#VideoCanvas {
    background: #0a0d11;
    border: 1px solid #303945;
    border-radius: 10px;
}
QLabel#Title {
    font-size: 22px;
    font-weight: 700;
}
QLabel#Subtitle, QLabel#Muted {
    color: #8e98a6;
}
QLabel#PanelTitle {
    font-size: 14px;
    font-weight: 700;
}
QLabel#Metric {
    color: #9aa6b4;
    font-size: 12px;
}
QLabel#MetricValue {
    font-size: 15px;
    font-weight: 700;
}
QLabel#ValueChip {
    background: #202833;
    border: 1px solid #364250;
    border-radius: 6px;
    padding: 2px 8px;
    min-width: 42px;
}
QPushButton {
    background: #212833;
    color: #eef2f6;
    border: 1px solid #35404d;
    border-radius: 8px;
    padding: 8px 12px;
}
QPushButton:hover {
    background: #2a3441;
    border-color: #4e6175;
}
QPushButton:pressed {
    background: #18202a;
}
QPushButton#accent {
    background: #3a7d67;
    border-color: #4c9b80;
    font-weight: 700;
}
QPushButton#accent:hover {
    background: #479276;
}
QPushButton#danger {
    background: #322126;
    border-color: #5d333d;
}
QCheckBox, QComboBox, QSpinBox {
    background: #1a2028;
    border: 1px solid #35404d;
    border-radius: 7px;
    padding: 6px;
}
QComboBox:hover, QSpinBox:hover {
    border-color: #4e6175;
}
QComboBox QAbstractItemView {
    background: #171c23;
    color: #eef2f6;
    selection-background-color: #315d50;
}
QSlider::groove:horizontal {
    height: 5px;
    background: #2b333d;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: #4d9d80;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #80c6ab;
    border: 1px solid #9ad9c0;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QGroupBox {
    border: 1px solid #28303a;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 700;
}
QGroupBox::title {
    left: 12px;
    padding: 0 6px;
}
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    width: 10px;
    background: transparent;
}
QScrollBar::handle:vertical {
    background: #313b47;
    border-radius: 5px;
    min-height: 30px;
}
"""

LIGHT_STYLE = """
QMainWindow, QWidget {
    background: #eef2f5;
    color: #1e2630;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}
QFrame#Header, QFrame#SidebarCard, QFrame#VideoCard, QFrame#StatusBar {
    background: #ffffff;
    border: 1px solid #d4dbe2;
    border-radius: 12px;
}
QFrame#VideoCanvas {
    background: #f7f9fb;
    border: 1px solid #cbd4dd;
    border-radius: 10px;
}
QLabel#Title {
    font-size: 22px;
    font-weight: 700;
}
QLabel#Subtitle, QLabel#Muted {
    color: #667485;
}
QLabel#PanelTitle {
    font-size: 14px;
    font-weight: 700;
}
QLabel#Metric {
    color: #657180;
    font-size: 12px;
}
QLabel#MetricValue {
    font-size: 15px;
    font-weight: 700;
}
QLabel#ValueChip {
    background: #f1f4f7;
    border: 1px solid #d2d9e0;
    border-radius: 6px;
    padding: 2px 8px;
    min-width: 42px;
}
QPushButton {
    background: #ffffff;
    color: #1e2630;
    border: 1px solid #cbd4dd;
    border-radius: 8px;
    padding: 8px 12px;
}
QPushButton:hover {
    background: #f3f6f8;
    border-color: #acbac7;
}
QPushButton#accent {
    background: #3f806b;
    border-color: #3f806b;
    color: white;
    font-weight: 700;
}
QPushButton#danger {
    background: #fff3f4;
    border-color: #e2b7bc;
}
QCheckBox, QComboBox, QSpinBox {
    background: #ffffff;
    border: 1px solid #cbd4dd;
    border-radius: 7px;
    padding: 6px;
}
QComboBox QAbstractItemView {
    background: white;
    color: #1e2630;
    selection-background-color: #d9ece5;
}
QSlider::groove:horizontal {
    height: 5px;
    background: #d9e0e6;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: #4a9c80;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #4a9c80;
    border: 1px solid #3f806b;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QGroupBox {
    border: 1px solid #d4dbe2;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 700;
}
QGroupBox::title {
    left: 12px;
    padding: 0 6px;
}
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    width: 10px;
    background: transparent;
}
QScrollBar::handle:vertical {
    background: #c0cad3;
    border-radius: 5px;
    min-height: 30px;
}
"""


class VideoLabel(QLabel):
    """Scalable image view that preserves the source aspect ratio."""

    def __init__(self):
        super().__init__()
        self._pixmap = QPixmap()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(260, 190)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_frame(self, image: QImage) -> None:
        self._pixmap = QPixmap.fromImage(image)
        self._refresh_pixmap()

    def clear_frame(self) -> None:
        self._pixmap = QPixmap()
        self.clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._refresh_pixmap()

    def _refresh_pixmap(self) -> None:
        if self._pixmap.isNull():
            return
        self.setPixmap(
            self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )


class ValueSlider(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(
        self,
        title: str,
        minimum: int,
        maximum: int,
        value: int,
        parent=None,
    ):
        super().__init__(parent)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(self._on_value_changed)

        self.title_label = QLabel(title)
        self.title_label.setMinimumWidth(92)

        self.value_label = QLabel()
        self.value_label.setObjectName("ValueChip")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(8)
        layout.addWidget(self.title_label)
        layout.addWidget(self.slider, 1)
        layout.addWidget(self.value_label)
        self._set_value_label(value)

    def _set_value_label(self, value: int) -> None:
        self.value_label.setText(str(value))

    def _on_value_changed(self, value: int) -> None:
        self._set_value_label(value)
        self.valueChanged.emit(value)

    def value(self) -> int:
        return self.slider.value()

    def setValue(self, value: int, emit: bool = True) -> None:
        if emit:
            self.slider.setValue(value)
        else:
            blocked = self.slider.blockSignals(True)
            self.slider.setValue(value)
            self.slider.blockSignals(blocked)
            self._set_value_label(value)

    def setEnabled(self, enabled: bool) -> None:
        super().setEnabled(enabled)
        self.slider.setEnabled(enabled)
        self.title_label.setEnabled(enabled)
        self.value_label.setEnabled(enabled)


class ColorDetectionWindow(QMainWindow):
    """Main UI for interactive HSV segmentation and morphology."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(QSize(1100, 720))
        self.resize(1500, 900)

        self.settings = QSettings()
        self.video_thread: VideoThread | None = None
        self._closing = False
        self.current_theme = self.settings.value("theme", DEFAULT_THEME)

        self._build_ui()
        self._restore_settings()
        self._apply_theme()
        self._start_video_thread()

    def _build_ui(self) -> None:
        central = QWidget()
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(14, 14, 14, 12)
        root_layout.setSpacing(12)

        header = QFrame()
        header.setObjectName("Header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 14, 18, 14)

        title_box = QVBoxLayout()
        title = QLabel("Color Detection Studio")
        title.setObjectName("Title")
        subtitle = QLabel("Real-time HSV segmentation, morphology, and bounding-box detection")
        subtitle.setObjectName("Subtitle")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header_layout.addLayout(title_box, 1)

        self.theme_button = QPushButton("☼ Light Mode")
        self.theme_button.clicked.connect(self._toggle_theme)
        self.fullscreen_button = QPushButton("Full Screen")
        self.fullscreen_button.clicked.connect(self._toggle_fullscreen)
        header_layout.addWidget(self.theme_button)
        header_layout.addWidget(self.fullscreen_button)
        root_layout.addWidget(header)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        video_side = QWidget()
        video_layout = QVBoxLayout(video_side)
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_layout.setSpacing(10)

        video_grid = QGridLayout()
        video_grid.setSpacing(10)
        self.original_panel = self._create_video_card("Original")
        self.raw_panel = self._create_video_card("Raw Mask")
        self.final_panel = self._create_video_card("Final Mask")
        video_grid.addWidget(self.original_panel, 0, 0)
        video_grid.addWidget(self.raw_panel, 0, 1)
        video_grid.addWidget(self.final_panel, 0, 2)
        for column in range(3):
            video_grid.setColumnStretch(column, 1)
        video_layout.addLayout(video_grid, 1)

        status = QFrame()
        status.setObjectName("StatusBar")
        status_layout = QHBoxLayout(status)
        status_layout.setContentsMargins(14, 8, 14, 8)
        self.status_label = QLabel("Starting camera...")
        self.status_label.setObjectName("Muted")
        self.detection_label = QLabel("Detections: 0")
        self.detection_label.setObjectName("MetricValue")
        self.fps_label = QLabel("FPS: --")
        self.fps_label.setObjectName("MetricValue")
        status_layout.addWidget(self.status_label, 1)
        status_layout.addWidget(self.detection_label)
        status_layout.addSpacing(18)
        status_layout.addWidget(self.fps_label)
        video_layout.addWidget(status)

        splitter.addWidget(video_side)
        splitter.addWidget(self._build_sidebar())
        splitter.setSizes([1120, 360])
        root_layout.addWidget(splitter, 1)
        self.splitter = splitter

        self.setCentralWidget(central)
        self.statusBar().hide()

        self._build_shortcuts()

    def _create_video_card(self, title: str) -> QFrame:
        card = QFrame()
        card.setObjectName("VideoCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("PanelTitle")
        layout.addWidget(title_label)

        canvas = QFrame()
        canvas.setObjectName("VideoCanvas")
        canvas_layout = QVBoxLayout(canvas)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        image = VideoLabel()
        image.setText("Waiting for camera...")
        canvas_layout.addWidget(image)
        layout.addWidget(canvas, 1)
        card.image = image
        return card

    def _build_sidebar(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(10)

        camera_box = QGroupBox("Camera")
        camera_layout = QVBoxLayout(camera_box)
        camera_row = QHBoxLayout()
        camera_row.addWidget(QLabel("Camera index"))
        self.camera_spin = QSpinBox()
        self.camera_spin.setRange(0, 9)
        self.camera_spin.setValue(DEFAULT_CAMERA_INDEX)
        self.camera_spin.valueChanged.connect(self._camera_index_changed)
        camera_row.addWidget(self.camera_spin)
        camera_layout.addLayout(camera_row)

        action_row = QHBoxLayout()
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self._toggle_pause)
        self.restart_button = QPushButton("Restart")
        self.restart_button.clicked.connect(self._restart_camera)
        action_row.addWidget(self.pause_button)
        action_row.addWidget(self.restart_button)
        camera_layout.addLayout(action_row)
        layout.addWidget(camera_box)

        color_box = QGroupBox("HSV Color Range")
        color_layout = QVBoxLayout(color_box)
        preset_row = QHBoxLayout()
        for name in HSV_PRESETS:
            button = QPushButton(name)
            button.clicked.connect(lambda checked=False, preset=name: self._apply_preset(preset))
            preset_row.addWidget(button)
        color_layout.addLayout(preset_row)

        self.h_min = ValueSlider("H min", 0, 179, DEFAULT_LOWER_HSV[0])
        self.s_min = ValueSlider("S min", 0, 255, DEFAULT_LOWER_HSV[1])
        self.v_min = ValueSlider("V min", 0, 255, DEFAULT_LOWER_HSV[2])
        self.h_max = ValueSlider("H max", 0, 179, DEFAULT_UPPER_HSV[0])
        self.s_max = ValueSlider("S max", 0, 255, DEFAULT_UPPER_HSV[1])
        self.v_max = ValueSlider("V max", 0, 255, DEFAULT_UPPER_HSV[2])
        self._add_control(color_layout, self.h_min)
        self._add_control(color_layout, self.s_min)
        self._add_control(color_layout, self.v_min)
        self._add_control(color_layout, self.h_max)
        self._add_control(color_layout, self.s_max)
        self._add_control(color_layout, self.v_max)
        layout.addWidget(color_box)

        detection_box = QGroupBox("Detection Filter")
        detection_layout = QVBoxLayout(detection_box)
        self.min_area = ValueSlider("Min area", 0, 20000, DEFAULT_MIN_AREA)
        detection_layout.addWidget(self.min_area)
        note = QLabel("Contours smaller than this area are ignored.")
        note.setObjectName("Muted")
        note.setWordWrap(True)
        detection_layout.addWidget(note)
        layout.addWidget(detection_box)

        morphology_box = QGroupBox("Morphology")
        morphology_layout = QVBoxLayout(morphology_box)

        kernel_row = QHBoxLayout()
        kernel_row.addWidget(QLabel("Kernel shape"))
        self.kernel_shape = QComboBox()
        for key, label in KERNEL_SHAPES.items():
            self.kernel_shape.addItem(label, key)
        self.kernel_shape.setCurrentIndex(self.kernel_shape.findData(DEFAULT_KERNEL_SHAPE))
        kernel_row.addWidget(self.kernel_shape, 1)
        morphology_layout.addLayout(kernel_row)

        self.kernel_size = ValueSlider("Kernel size", 1, 31, DEFAULT_KERNEL_SIZE)
        self.kernel_size.valueChanged.connect(self._snap_kernel_size)
        morphology_layout.addWidget(self.kernel_size)

        self.opening_enabled = QCheckBox("Apply Opening")
        self.opening_enabled.setChecked(DEFAULT_OPENING_ENABLED)
        self.opening_iterations = ValueSlider(
            "Opening iterations", 1, 5, DEFAULT_OPENING_ITERATIONS
        )
        self.opening_enabled.toggled.connect(self.opening_iterations.setEnabled)
        self.opening_iterations.setEnabled(DEFAULT_OPENING_ENABLED)
        morphology_layout.addWidget(self.opening_enabled)
        morphology_layout.addWidget(self.opening_iterations)

        self.closing_enabled = QCheckBox("Apply Closing")
        self.closing_enabled.setChecked(DEFAULT_CLOSING_ENABLED)
        self.closing_iterations = ValueSlider(
            "Closing iterations", 1, 5, DEFAULT_CLOSING_ITERATIONS
        )
        self.closing_enabled.toggled.connect(self.closing_iterations.setEnabled)
        self.closing_iterations.setEnabled(DEFAULT_CLOSING_ENABLED)
        morphology_layout.addWidget(self.closing_enabled)
        morphology_layout.addWidget(self.closing_iterations)

        morphology_note = QLabel(
            "Pipeline order: Raw Mask → Opening → Closing → Final Mask"
        )
        morphology_note.setObjectName("Muted")
        morphology_note.setWordWrap(True)
        morphology_layout.addWidget(morphology_note)
        layout.addWidget(morphology_box)

        bottom_row = QHBoxLayout()
        reset = QPushButton("Reset Defaults")
        reset.clicked.connect(self._reset_defaults)
        reset.setObjectName("accent")
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)
        quit_button.setObjectName("danger")
        bottom_row.addWidget(reset)
        bottom_row.addWidget(quit_button)
        layout.addLayout(bottom_row)

        hint = QLabel(
            "Shortcuts: Space = pause/resume · F11 = full screen · R = reset · Q = quit"
        )
        hint.setObjectName("Muted")
        hint.setWordWrap(True)
        layout.addWidget(hint)
        layout.addStretch(1)

        self._connect_controls()
        scroll.setWidget(content)
        return scroll

    def _connect_controls(self) -> None:
        controls = [
            self.h_min,
            self.s_min,
            self.v_min,
            self.h_max,
            self.s_max,
            self.v_max,
            self.min_area,
            self.kernel_size,
            self.opening_iterations,
            self.closing_iterations,
        ]
        for control in controls:
            control.valueChanged.connect(self._parameters_changed)
        self.kernel_shape.currentIndexChanged.connect(self._parameters_changed)
        self.opening_enabled.toggled.connect(self._parameters_changed)
        self.closing_enabled.toggled.connect(self._parameters_changed)

    def _add_control(self, layout: QVBoxLayout, control: QWidget) -> None:
        layout.addWidget(control)

    def _build_shortcuts(self) -> None:
        from PyQt6.QtGui import QKeySequence, QShortcut

        QShortcut(QKeySequence("Space"), self, activated=self._toggle_pause)
        QShortcut(QKeySequence("F11"), self, activated=self._toggle_fullscreen)
        QShortcut(QKeySequence("R"), self, activated=self._reset_defaults)
        QShortcut(QKeySequence("Q"), self, activated=self.close)

    def _start_video_thread(self) -> None:
        self._stop_video_thread()
        self.video_thread = VideoThread(self.camera_spin.value(), self)
        self.video_thread.set_parameters(self._current_parameters())
        self.video_thread.frame_ready.connect(self._update_frames)
        self.video_thread.camera_status.connect(self.status_label.setText)
        self.video_thread.start()
        self.pause_button.setText("Pause")

    def _stop_video_thread(self) -> None:
        if self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread = None

    def _restart_camera(self) -> None:
        self.status_label.setText("Restarting camera...")
        self._start_video_thread()

    def _camera_index_changed(self, _: int) -> None:
        if self.video_thread is not None:
            self.video_thread.set_camera_index(self.camera_spin.value())

    def _toggle_pause(self) -> None:
        if self.video_thread is None:
            return
        paused = self.pause_button.text() == "Pause"
        self.video_thread.set_paused(paused)
        self.pause_button.setText("Resume" if paused else "Pause")

    def _current_parameters(self) -> DetectionParameters:
        return DetectionParameters(
            lower_hsv=(self.h_min.value(), self.s_min.value(), self.v_min.value()),
            upper_hsv=(self.h_max.value(), self.s_max.value(), self.v_max.value()),
            min_area=self.min_area.value(),
            kernel_size=self.kernel_size.value(),
            kernel_shape=self.kernel_shape.currentData(),
            opening_enabled=self.opening_enabled.isChecked(),
            opening_iterations=self.opening_iterations.value(),
            closing_enabled=self.closing_enabled.isChecked(),
            closing_iterations=self.closing_iterations.value(),
        )

    def _parameters_changed(self, *_args) -> None:
        if self.video_thread is not None:
            self.video_thread.set_parameters(self._current_parameters())

    def _snap_kernel_size(self, value: int) -> None:
        if value % 2 == 0:
            self.kernel_size.setValue(max(1, value - 1), emit=False)
            self._parameters_changed()

    def _apply_preset(self, name: str) -> None:
        lower, upper = HSV_PRESETS[name]
        controls = [
            (self.h_min, lower[0]),
            (self.s_min, lower[1]),
            (self.v_min, lower[2]),
            (self.h_max, upper[0]),
            (self.s_max, upper[1]),
            (self.v_max, upper[2]),
        ]
        for control, value in controls:
            control.setValue(value, emit=False)
        self._parameters_changed()

    def _reset_defaults(self) -> None:
        self._apply_preset("Red")
        self.min_area.setValue(DEFAULT_MIN_AREA, emit=False)
        self.kernel_size.setValue(DEFAULT_KERNEL_SIZE, emit=False)
        self.kernel_shape.setCurrentIndex(self.kernel_shape.findData(DEFAULT_KERNEL_SHAPE))
        self.opening_enabled.setChecked(DEFAULT_OPENING_ENABLED)
        self.opening_iterations.setValue(DEFAULT_OPENING_ITERATIONS, emit=False)
        self.closing_enabled.setChecked(DEFAULT_CLOSING_ENABLED)
        self.closing_iterations.setValue(DEFAULT_CLOSING_ITERATIONS, emit=False)
        self.camera_spin.setValue(DEFAULT_CAMERA_INDEX)
        self.current_theme = DEFAULT_THEME
        self._apply_theme()
        self._parameters_changed()
        self.status_label.setText("Default settings restored")

    def _toggle_theme(self) -> None:
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme()

    def _apply_theme(self) -> None:
        is_dark = self.current_theme == "dark"
        self.setStyleSheet(DARK_STYLE if is_dark else LIGHT_STYLE)
        self.theme_button.setText("☼ Light Mode" if is_dark else "◐ Dark Mode")

    def _toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showMaximized()
            self.fullscreen_button.setText("Full Screen")
        else:
            self.showFullScreen()
            self.fullscreen_button.setText("Exit Full Screen")

    @staticmethod
    def _to_qimage(frame, grayscale: bool = False) -> QImage:
        if grayscale:
            height, width = frame.shape
            return QImage(
                frame.data,
                width,
                height,
                frame.strides[0],
                QImage.Format.Format_Grayscale8,
            ).copy()

        rgb = frame[:, :, ::-1].copy()
        height, width, channels = rgb.shape
        return QImage(
            rgb.data,
            width,
            height,
            width * channels,
            QImage.Format.Format_RGB888,
        ).copy()

    def _update_frames(self, original, raw_mask, final_mask, count: int, fps: float) -> None:
        if self._closing:
            return
        self.original_panel.image.set_frame(self._to_qimage(original))
        self.raw_panel.image.set_frame(self._to_qimage(raw_mask, grayscale=True))
        self.final_panel.image.set_frame(self._to_qimage(final_mask, grayscale=True))
        self.detection_label.setText(f"Detections: {count}")
        self.fps_label.setText(f"FPS: {fps:.1f}")

    def _restore_settings(self) -> None:
        self.camera_spin.setValue(
            self.settings.value("camera_index", DEFAULT_CAMERA_INDEX, type=int)
        )

        lower = [
            self.settings.value(f"hsv/lower_{axis}", value, type=int)
            for axis, value in zip(("h", "s", "v"), DEFAULT_LOWER_HSV)
        ]
        upper = [
            self.settings.value(f"hsv/upper_{axis}", value, type=int)
            for axis, value in zip(("h", "s", "v"), DEFAULT_UPPER_HSV)
        ]
        for control, value in zip(
            (self.h_min, self.s_min, self.v_min, self.h_max, self.s_max, self.v_max),
            (*lower, *upper),
        ):
            control.setValue(value, emit=False)

        self.min_area.setValue(
            self.settings.value("min_area", DEFAULT_MIN_AREA, type=int), emit=False
        )
        kernel = self.settings.value("kernel_size", DEFAULT_KERNEL_SIZE, type=int)
        self.kernel_size.setValue(kernel if kernel % 2 else kernel - 1, emit=False)
        shape = self.settings.value("kernel_shape", DEFAULT_KERNEL_SHAPE)
        index = self.kernel_shape.findData(shape)
        if index >= 0:
            self.kernel_shape.setCurrentIndex(index)

        self.opening_enabled.setChecked(
            self.settings.value("opening_enabled", DEFAULT_OPENING_ENABLED, type=bool)
        )
        self.opening_iterations.setValue(
            self.settings.value("opening_iterations", DEFAULT_OPENING_ITERATIONS, type=int),
            emit=False,
        )
        self.closing_enabled.setChecked(
            self.settings.value("closing_enabled", DEFAULT_CLOSING_ENABLED, type=bool)
        )
        self.closing_iterations.setValue(
            self.settings.value("closing_iterations", DEFAULT_CLOSING_ITERATIONS, type=int),
            emit=False,
        )

        geometry = self.settings.value("window/geometry")
        state = self.settings.value("window/state")
        splitter_state = self.settings.value("window/splitter")
        if geometry:
            self.restoreGeometry(geometry)
        if state:
            self.restoreState(state)
        if splitter_state:
            self.splitter.restoreState(splitter_state)

    def _save_settings(self) -> None:
        self.settings.setValue("theme", self.current_theme)
        self.settings.setValue("camera_index", self.camera_spin.value())
        lower = self._current_parameters().lower_hsv
        upper = self._current_parameters().upper_hsv
        for axis, value in zip(("h", "s", "v"), lower):
            self.settings.setValue(f"hsv/lower_{axis}", value)
        for axis, value in zip(("h", "s", "v"), upper):
            self.settings.setValue(f"hsv/upper_{axis}", value)
        parameters = self._current_parameters()
        self.settings.setValue("min_area", parameters.min_area)
        self.settings.setValue("kernel_size", parameters.kernel_size)
        self.settings.setValue("kernel_shape", parameters.kernel_shape)
        self.settings.setValue("opening_enabled", parameters.opening_enabled)
        self.settings.setValue("opening_iterations", parameters.opening_iterations)
        self.settings.setValue("closing_enabled", parameters.closing_enabled)
        self.settings.setValue("closing_iterations", parameters.closing_iterations)
        self.settings.setValue("window/geometry", self.saveGeometry())
        self.settings.setValue("window/state", self.saveState())
        self.settings.setValue("window/splitter", self.splitter.saveState())
        self.settings.sync()

    def closeEvent(self, event) -> None:
        self._closing = True
        self._save_settings()
        self._stop_video_thread()
        event.accept()
