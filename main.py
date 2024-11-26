import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
)
from main_window import MainWindow
from variables import WINDOW_ICON_PATH

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    label1 = QLabel("Meu texto teste")
    label1.setStyleSheet("font-size: 150px")
    window.addWidgetToVLayout(label1)

    # Criar o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    window.adjustFixedSize()
    window.show()
    app.exec()
