from math import ceil

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QRect, QPointF
import sys

from fretboard.fretboard import *
from fretboard.notes_utils import convert_int_note_to_str

# Static objects
initial_key = "E"
keys: list[str] = convert_int_notes_to_str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], as_sharps=True)
fretboard = Fretboard.init_as_pedal_steel_e9()
tuning = fretboard.get_tuning_as_str()
num_strings = len(tuning)


def generate_scale(key: str):
    start_fret = 0
    end_fret = 12
    fretboard_data = fretboard.generate_major_scale_as_integers(key, start_fret, end_fret)

    pedals_to_apply = None
    fretboard_data = fretboard.convert_fretboard_scale_to_intervals(key, fretboard_data, pedals_to_apply)

    return fretboard_data


class FretboardWidget(QWidget):

    num_strings: int = 10
    string_spacing: float = 0
    num_frets: int = 12 + 1  # include zero fret
    fretboard_data = None

    def __init__(self, parent=None, num_strings=10):
        super().__init__(parent)
        self.num_strings = num_strings
        self.fretboard_data = generate_scale(initial_key)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.drawFretboard(painter, tuning)
        self.drawNotes(painter, self.fretboard_data)

    def get_fret_spacing(self) -> float:
        return self.width() / (self.num_frets + 1 - 1)

    def get_fret_offset(self) -> float:
        return self.width() / 30

    def drawFretboard(self, painter, tuning: list[str]):
        # Draw fretboard
        painter.fillRect(self.rect(), QColor("#a57a39"))

        width = self.width()
        height = self.height()

        fret_spacing = self.get_fret_spacing()
        fret_penWidth = width / 150
        fret_offset = self.get_fret_offset()

        # Draw zero fret
        r = self.rect()
        painter.fillRect(QRect(0, 0, int(fret_spacing + fret_penWidth / 2 - fret_offset), height), QColor("#000000"))

        # Draw frets
        pen1 = QPen(QColor("#d7d6d6"), fret_penWidth)
        pen2 = QPen(QColor("#686868"), fret_penWidth * 0.5)
        for i in range(self.num_frets):
            x = (i + 1) * fret_spacing - fret_offset
            if i > 0:  # skip zero fret
                painter.setPen(pen1)
                painter.drawLine(x, 0, x, height)
            painter.setPen(pen2)
            painter.drawLine(x + pen1.width() / 2, 0, x + pen1.width() / 2, height)

        # Draw fretboard dots
        painter.setBrush(QColor("#383530"))
        painter.setPen(Qt.PenStyle.NoPen)
        dotRadius = width / 70
        x = 3.5 * fret_spacing - fret_offset
        painter.drawEllipse(QPointF(x, height / 2), dotRadius, dotRadius)
        x = 5.5 * fret_spacing - fret_offset
        painter.drawEllipse(QPointF(x, height / 2), dotRadius, dotRadius)
        x = 7.5 * fret_spacing - fret_offset
        painter.drawEllipse(QPointF(x, height / 2), dotRadius, dotRadius)
        x = 9.5 * fret_spacing - fret_offset
        painter.drawEllipse(QPointF(x, height / 2), dotRadius, dotRadius)
        x = 12.5 * fret_spacing - fret_offset
        painter.drawEllipse(QPointF(x, height / 3), dotRadius, dotRadius)
        painter.drawEllipse(QPointF(x, 2 * height / 3), dotRadius, dotRadius)

        # Draw strings
        self.string_spacing = 1.08 * height / (self.num_strings + 1)
        string_penWidth = width / 400
        pen1 = QPen(QColor("#c8bb93"), string_penWidth)
        pen2 = QPen(QColor("#958963"), string_penWidth * 0.2)
        for i in range(self.num_strings):
            if i < 3:
                actual_string_penWidth = 3 / 5 * fret_penWidth
                pen1.setWidth(int(3 / 5 * string_penWidth))
                pen2.setWidth(int(3 / 5 * string_penWidth * 0.2))
            elif i < 5:
                pen1.setWidth(int(4 / 5 * string_penWidth))
                pen2.setWidth(int(4 / 5 * string_penWidth * 0.2))
            else:
                pen1.setWidth(int(string_penWidth))
                pen2.setWidth(int(string_penWidth * 0.2))

            painter.setPen(pen1)
            y = (i + 1) * self.string_spacing - 0.04 * height
            painter.drawLine(0, y, width, y)
            painter.setPen(pen2)
            painter.drawLine(0, y + pen1.width() / 2, width, y + pen1.width() / 2)

        # Draw open notes
        fontSize: int = ceil(0.0283 * height)
        font = QFont("Arial", fontSize)
        painter.setFont(font)
        pen = QPen(QColor("white"))
        painter.setPen(pen)
        for i in range(self.num_strings):
            y = (i + 1) * self.string_spacing - 0.04 * height - 0.005 * height
            painter.drawText(0, y, list(reversed(tuning))[i])

    def drawNotes(self, painter, fretboard_data):
        width = self.width()
        height = self.height()
        shadow_offset = QPointF(width * 0.0005, height * 0.005)
        dotRadius = width / 80
        fontSize: int = ceil(height * 0.0326)

        for string_i, string_data in enumerate(reversed(fretboard_data)):
            for note_i, string_note in enumerate(string_data):
                if string_note != None:
                    y = (string_i + 1) * self.string_spacing - 0.04 * height
                    x = (note_i + 1) * self.get_fret_spacing() - self.get_fret_offset()

                    # draw shadow
                    # more shadow to fake blur
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(QColor(0, 0, 0, 10))
                    painter.drawEllipse(QPointF(x, y) + shadow_offset, dotRadius * 1.3, dotRadius * 1.3)
                    painter.setBrush(QColor(0, 0, 0, 10))
                    painter.drawEllipse(QPointF(x, y) + shadow_offset, dotRadius * 1.15, dotRadius * 1.15)
                    painter.setBrush(QColor(0, 0, 0, 25))
                    painter.drawEllipse(QPointF(x, y) + shadow_offset, dotRadius, dotRadius)

                    # dot
                    painter.setBrush(QColor("#fa990f"))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(QPointF(x, y), dotRadius, dotRadius)

                    # str
                    font = QFont("Tahoma", fontSize)  # 30
                    font.setBold(True)
                    painter.setFont(font)
                    pen = QPen(QColor("black"))
                    painter.setPen(pen)
                    painter.drawText(x - 0.5 * dotRadius, y + 0.6 * dotRadius, string_note)

        return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setWindowState(Qt.WindowState.WindowFullScreen)

        # Central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove outer margins
        main_layout.setSpacing(0)  # Remove spacing between widgets
        self.setCentralWidget(central_widget)

        # Add fretboard
        self.fretboard = FretboardWidget(None, num_strings)
        self.fretboard.setFixedHeight(int(self.height() * 0.85))
        main_layout.addWidget(self.fretboard)

        # Bottom layout
        bottom_bar = QWidget()
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(10, 10, 10, 10)
        bottom_layout.setSpacing(20)  # Space between dropdowns
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Dropdown buttons
        fontSize: int = ceil(self.height() * 0.0326)
        font = QFont("Arial", fontSize)
        font.setBold(True)
        self.dropdown = QComboBox()
        self.dropdown.addItems(keys)
        self.dropdown.setFixedSize(int(self.width() * 0.05), int(self.height() * 0.05))
        self.dropdown.setFont(font)
        self.dropdown.setCurrentIndex(keys.index(initial_key))
        self.dropdown.currentIndexChanged.connect(lambda index: self.on_key_change(index))
        bottom_layout.addWidget(self.dropdown)

        self.dropdown2 = QComboBox()
        self.dropdown2.addItems(["Major", "Pentatonic Major"])
        self.dropdown2.setFixedSize(int(self.width() * 0.25), int(self.height() * 0.05))
        self.dropdown2.setFont(font)
        self.dropdown2.setCurrentIndex(0)
        self.dropdown2.currentIndexChanged.connect(self.on_mode_change)
        bottom_layout.addWidget(self.dropdown2)

        main_layout.addWidget(bottom_bar)

    def on_key_change(self, key_index: int):
        key = convert_int_note_to_str(key_index, True)
        self.fretboard.fretboard_data = generate_scale(key)
        self.update()
        return

    def on_mode_change(self):
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
