import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
)
from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    label1 = QLabel("Meu texto teste")
    label1.setStyleSheet("font-size: 150px")
    window.vbox_layout.addWidget(label1)
    window.adjustFixedSize

    window.show()
    app.exec()
