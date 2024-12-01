import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from main_window import MainWindow, Info, ButtonsGrid
from variables import WINDOW_ICON_PATH
from display import Display
from styles import setupTheme

if __name__ == "__main__":
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    # Cria o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info("x ^ n")
    window.addWidgetToVLayout(info)

    # Definindo display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid
    buttonsGrid = ButtonsGrid()
    window.vLayout.addLayout(buttonsGrid)

    # Executa a aplicação
    window.adjustFixedSize()
    window.show()
    app.exec()
