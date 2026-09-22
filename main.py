import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from config import APP_NAME, ORGANIZATION_NAME
from gui import ColorDetectionWindow


def main() -> None:
    """Application entry point."""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setApplicationDisplayName(APP_NAME)

    window = ColorDetectionWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
