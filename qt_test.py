from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPixmap
from PySide6.QtCore import Qt, QRect, QPointF
import sys


class TestWidget(QWidget):

    def __init__(self, parent=None, num_strings=10):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.draw(painter)

    def draw(self, painter):
        width = self.width()
        dotRadius = width / 80
        painter.setBrush(QColor("#fa990f"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(0.5 * width, 0.5 * self.height()), dotRadius, dotRadius)


class TestWidget2(QGraphicsView):
    def __init__(self):
        super().__init__()
        # self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw other shapes (example line)
        painter.drawLine(50, 50, 350, 50)

        # Create a pixmap to draw the disk
        disk_size = 100
        pixmap = QPixmap(disk_size * 2, disk_size * 2)
        pixmap.fill(QColor(0, 0, 0, 50))

        # Draw the disk onto the pixmap
        disk_painter = QPainter(pixmap)
        disk_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        disk_painter.setBrush(QColor("blue"))
        disk_painter.setPen(Qt.PenStyle.NoPen)
        disk_painter.drawEllipse(QRect(disk_size // 2, disk_size // 2, disk_size, disk_size))
        disk_painter.end()

        # Apply shadow effect
        from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsBlurEffect

        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(pixmap)
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(15)
        item.setGraphicsEffect(blur)
        scene.addItem(item)

        # Render the scene with the shadow to a new pixmap
        shadow_pixmap = QPixmap(pixmap.size())
        shadow_pixmap.fill(QColor(0, 0, 0, 50))
        shadow_painter = QPainter(shadow_pixmap)
        scene.render(shadow_painter)
        shadow_painter.end()

        # Draw the shadowed disk onto the widget
        painter.drawPixmap(150, 150, shadow_pixmap)

        painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setWindowState(Qt.WindowState.WindowFullScreen)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.testWidget = TestWidget()
        main_layout.addWidget(self.testWidget)

        self.testWidget2 = TestWidget2()
        main_layout.addWidget(self.testWidget2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
