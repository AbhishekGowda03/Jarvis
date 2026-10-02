
import sys
import math
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QApplication, QWidget


class JarvisWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.resize(150, 170)
        self.angle = 0
        self.drag_position = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.angle = (self.angle + 2) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = 75
        center_y = 70

        # Outer glow
        gradient = QRadialGradient(center_x, center_y, 65)
        gradient.setColorAt(0, QColor(0, 160, 255, 45))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(10, 5, 130, 130)

        # Rotating rings
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.angle)

        for radius, width in [(48, 2), (38, 3), (27, 1)]:
            pen = QPen(QColor(0, 190, 255, 220), width)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawArc(
                -radius, -radius,
                radius * 2, radius * 2,
                20 * 16, 250 * 16
            )

        painter.restore()

        # Center orb
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 145, 255, 230))
        painter.drawEllipse(60, 55, 30, 30)

        painter.setBrush(QColor(180, 240, 255))
        painter.drawEllipse(68, 63, 14, 14)

        # Microphone button
        painter.setPen(QPen(QColor(0, 190, 255), 2))
        painter.setBrush(QColor(10, 25, 45, 230))
        painter.drawEllipse(56, 132, 38, 30)

        painter.setPen(QColor(180, 230, 255))
        painter.drawText(56, 153, 38, 10,
                         Qt.AlignmentFlag.AlignCenter, "MIC")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

    def mouseReleaseEvent(self, event):
        self.drag_position = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = JarvisWidget()
    widget.show()
    sys.exit(app.exec())
