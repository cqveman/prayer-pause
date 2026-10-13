from collections.abc import Callable
from datetime import date, datetime

from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QAction, QIcon, QPixmap, Qt
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
    def __init__(self, prayers: dict[str, dict[str,str]], config_manager: ConfigManager):  # fmt:skip
        super().__init__()

        self.today = date.today()
        self.prayers = prayers.get(self.today.strftime("%d-%m-%Y"), {})
        self.config_manager = config_manager

        self.setWindowTitle("Prayer Pause")
        self.setFixedSize(700, 370)

        self.container = QWidget()
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(16, 10, 16, 16)
        self.main_layout.setSpacing(8)

        self._build_background()
        self._build_clock()

        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(14)
        panels_layout.addWidget(self._prayers_panel(), 1)
        panels_layout.addWidget(self._settings_panel(), 1)

        self.main_layout.addLayout(panels_layout)
        self.setCentralWidget(self.container)

        self.container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.container.setFocus()

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._tick)
        self._tick()

    def _build_background(self):
        bg = QLabel(self.container)

        pad = 40
        size = QSize(self.width() + pad * 2, self.height() + pad * 2)
        bg.setGeometry(-pad, -pad, size.width(), size.height())

        bg.setPixmap(
            QPixmap(Utils.ASSETS_DIR / "bg.jpg").scaled(
                size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        blur = QGraphicsBlurEffect(bg)
        blur.setBlurRadius(10.0)
        blur.setBlurHints(QGraphicsBlurEffect.BlurHint.AnimationHint)
        bg.setGraphicsEffect(blur)

        dim = QWidget(self.container)
        dim.setObjectName("dim")
        dim.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        dim.setGeometry(0, 0, self.width(), self.height())

        # `dim` is lowered,
        # then `bg` is lowered further back sitting underneath `dim`
        dim.lower()
        bg.lower()

    # --- CLOCK ---

    def _build_clock(self):
        self.clock_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setObjectName("clock")
        self.main_layout.addWidget(self.clock_label)

    def _tick(self):
        now = datetime.now()
        text = f"{now.hour % 12 or 12}:{now.minute:02}:{now.second:02} {'AM' if now.hour < 12 else 'PM'}"
        if text != self.clock_label.text():
            self.clock_label.setText(text)

    # --- PANELS ---

    def _prayers_panel(self) -> QGroupBox:
        box = QGroupBox(title=self.today.strftime("%A, %d %B %Y").upper())

        form = QFormLayout(box)
        form.setVerticalSpacing(20)
        form.setContentsMargins(40, 10, 40, 30)

        for name, time in self.prayers.items():
            name_label = QLabel(name.upper())
            name_label.setObjectName("prayerName")

            time_label = QLabel(
                Utils.to_12h_time(time), alignment=Qt.AlignmentFlag.AlignRight
            )
            time_label.setObjectName("prayerTime")

            form.addRow(name_label, time_label)

        return box

    def _settings_panel(self) -> QGroupBox:
        box = QGroupBox(title="SETTINGS")

        config: dict[str, int] = self.config_manager.load(in_dict=True)
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
            spin.setFixedWidth(150)

            spin.valueChanged.connect(lambda value, k=key: self.config_manager.set(k, value))  # fmt:skip

            text = QLabel(label)
            text.setObjectName("settingLabel")

            # A layout to push the spinboxes to the right side of the form
            field = QHBoxLayout()
            field.setContentsMargins(0, 0, 0, 0)
            field.addStretch()
            field.addWidget(spin)

            form.addRow(text, field)

        return box

    def showEvent(self, event):
        super().showEvent(event)
        self._tick()
        self.clock_timer.start(250)

    def hideEvent(self, event):
        self.clock_timer.stop()
        super().hideEvent(event)


class Tray(QSystemTrayIcon):
    def __init__(self, create_window: Callable[[], Window]):
        super().__init__()

        self._create_window = create_window
        self.window = create_window()

        self.setToolTip("Prayer Pause")
        self.setContextMenu(self._build_menu())
        self.setIcon(QIcon(str(Utils.ASSETS_DIR / "icon.png")))

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
        # If the app is running for over a day, re-create it.
        # (so the prayer times gets updated to the current day)
        if self.window.today != date.today():
            self.window.deleteLater()
            self.window = self._create_window()

        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
