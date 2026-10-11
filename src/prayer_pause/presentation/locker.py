from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from prayer_pause.infrastructure.config_manager import ConfigManager
from prayer_pause.utils import Utils


# TODO: the lock screen should cover all the workspaces in hyprland and not just the one it got initialized in
class Locker(QWidget):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()

        # A plain QWidget ignores background rules from QSS unless this is set.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("Locker")

        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        # On some window managers on X11
        # you also have to pass `X11BypassWindowManagerHint` for
        # `WindowStaysOnTopHint` flag to work correctly.
        if Utils.get_display_manager() == "X11":
            flags = flags | Qt.WindowType.X11BypassWindowManagerHint
        self.setWindowFlags(flags)
        # Blocks keyboard/mouse inputs to other windows
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.is_locked = True
        self.config_manager = config_manager
        self.total_seconds = 0
        self.remaining_seconds = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self._countdown)

        self._build_ui()
        self._reset_countdown()

    @Slot(str)
    def exc(self, prayer_name: str):
        self._reset_countdown()
        self.timer.start(1000)
        self.title_label.setText(f"Device locked for {prayer_name} prayer")
        self.showFullScreen()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addStretch()

        self.title_label = QLabel("")
        self.title_label.setObjectName("Title")
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.countdown_label = QLabel("00:00")
        self.countdown_label.setObjectName("Countdown")
        layout.addWidget(self.countdown_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(32)

        # Drains from full to empty as the locker runs out.
        self.progress = QProgressBar()
        self.progress.setObjectName("Progress")
        self.progress.setTextVisible(False)
        self.progress.setFixedWidth(460)
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

    def _reset_countdown(self):
        self.is_locked = True
        self.total_seconds = self.config_manager.load().lock_duration_minutes * 60
        self.remaining_seconds = self.total_seconds
        self.progress.setRange(0, max(self.total_seconds, 1))
        self._update_countdown()

    def _countdown(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self._update_countdown()
        else:
            self.timer.stop()
            self.is_locked = False
            self.close()

    def _update_countdown(self):
        """Convert seconds into MM:SS format."""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60

        self.countdown_label.setText(f"{minutes:02}:{seconds:02}")
        self.progress.setValue(self.remaining_seconds)

    # --- Events ---

    def closeEvent(self, event):
        if self.is_locked:
            event.ignore()
        else:
            event.accept()

    def keyPressEvent(self, event):
        pass
