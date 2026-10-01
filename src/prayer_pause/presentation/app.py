from collections.abc import Callable
from datetime import date
from typing import ClassVar

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QPixmap, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QGraphicsBlurEffect,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QSpinBox,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from prayer_pause.infrastructure.config_manager import ConfigManager
from prayer_pause.utils import Utils


class Window(QMainWindow):
    BLUR: ClassVar = QGraphicsBlurEffect()
    BLUR.setBlurRadius(float(10))
    BLUR.setBlurHints(QGraphicsBlurEffect.BlurHint.AnimationHint)

    def __init__(self, prayers: dict[str, str], config_manager: ConfigManager):
        super().__init__()

        self.prayers = prayers
        self.config_manager = config_manager

        self.setWindowTitle("Prayer Pause")
        self.setFixedSize(700, 370)

        self.container = QWidget()
        self.main_layout = QVBoxLayout(self.container)
        self._build_background()

        panels_layout = QHBoxLayout()
        panels_layout.addWidget(self._prayers_panel())
        panels_layout.addWidget(self._settings_panel())

        self.main_layout.addLayout(panels_layout)
        self.setCentralWidget(self.container)

    def _build_background(self):
        date_label = QLabel(
            text=date.today().strftime("%A, %d %B %Y").upper(),
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        date_label.setObjectName("date")
        self.main_layout.addWidget(date_label)

        bg = QLabel(self.container)

        pad = 40
        pad_size = QSize(self.width() + pad * 2, self.height() + pad * 2)
        bg.setGeometry(-pad, -pad, pad_size.width(), pad_size.height())

        bg.setPixmap(
            QPixmap(Utils.ASSETS_DIR / "bg.jpg").scaled(
                pad_size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        bg.lower()  # Make it appear behind widgets
        bg.setGraphicsEffect(Window.BLUR)

    def _prayers_panel(self) -> QGroupBox:
        box = QGroupBox(title="PRAYER TIMES")

        form = QFormLayout(box)
        form.setVerticalSpacing(20)
        form.setContentsMargins(40, 10, 40, 30)

        for name, time in self.prayers.items():
            form.addRow(name.upper(), QLabel(text=Utils.to_12h_time(time), alignment=Qt.AlignmentFlag.AlignRight))  # fmt: skip

        return box

    def _settings_panel(self) -> QGroupBox:
        box = QGroupBox(title="SETTINGS")

        config: dict[str, int] = self.config_manager.load(in_dict=True)  # pyright: ignore[reportAssignmentType]
        lables = [Utils.format_config_key(key) for key in config]
        values = [value for value in config.values()]

        form = QFormLayout(box)
        form.setVerticalSpacing(10)
        form.setContentsMargins(20, 10, 20, 20)

        for key, label, value, low, high in zip(
            config,
            lables,
            values,
            Utils.MIN_VALUES,
            Utils.MAX_VALUES,
        ):
            spin = QSpinBox(
                value=value,
                minimum=low,
                maximum=high,
                suffix=" min",
            )

            spin.lineEdit().setReadOnly(True)
            spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

            spin.valueChanged.connect(lambda value, k=key: self.config_manager.set(k, value))  # fmt: skip
            form.addRow(label, spin)

        return box


class Tray(QSystemTrayIcon):
    def __init__(self, create_window: Callable[[], Window]):
        super().__init__()

        self.window = create_window()

        self.setToolTip("Prayer Pause")
        self.setContextMenu(self._build_menu())

    def _build_menu(self) -> QMenu:
        menu = QMenu()

        show_action = QAction("Show", self)
        show_action.triggered.connect(self._show_window)
        menu.addAction(show_action)

        menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)  # pyright: ignore[reportOptionalMemberAccess]
        menu.addAction(quit_action)

        return menu

    def _show_window(self):
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
