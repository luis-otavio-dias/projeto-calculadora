import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from main_window import MainWindow, Info, Button, ButtonsGrid
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

    buttonsGrid.addWidget(Button("0"), 0, 0)
    buttonsGrid.addWidget(Button("1"), 0, 1)
    buttonsGrid.addWidget(Button("2"), 0, 2)
    buttonsGrid.addWidget(Button("3"), 1, 0)
    buttonsGrid.addWidget(Button("4"), 1, 1)
    buttonsGrid.addWidget(Button("5"), 1, 2)
    buttonsGrid.addWidget(Button("6"), 2, 0)
    buttonsGrid.addWidget(Button("8"), 2, 1)
    buttonsGrid.addWidget(Button("9"), 2, 2)

    # Executa a aplicação
    window.adjustFixedSize()
    window.show()
    app.exec()
