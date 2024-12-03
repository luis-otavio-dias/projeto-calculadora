from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QLineEdit,
)
from PySide6.QtCore import Qt, Slot
from variables import (
    SMALL_FONT_SIZE,
    MEDIUM_FONT_SIZE,
    MINIMUM_WIDTH,
    BIG_FONT_SIZE,
    TEXT_MARGIN,
)
from utils import isEmpty, isNumOrDot, isValidNumber


# Visualização da entrada de dados
class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [TEXT_MARGIN for any in range(4)]
        self.setStyleSheet(f"font-size: {BIG_FONT_SIZE}px")
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)


# Principais componentes da janela principal do programa
class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Título da janela
        self.setWindowTitle("Calculadora")

        # Layout básico
        self.central_widget = QWidget()
        self.vLayout = QVBoxLayout()
        self.central_widget.setLayout(self.vLayout)
        self.setCentralWidget(self.central_widget)

    # Última coisa a ser feita
    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)


# Classe Info para mostrar informações
class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f"font-size: {SMALL_FONT_SIZE}px;")
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


# Botoes
class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["", "0", ".", "="],
        ]

        self.display = display
        self.info = info
        self._equation = ""
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        # indexes, i e j
        # i row index; j column index
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")

                self.addWidget(button, i, j)
                buttonSlot = self._makeButtonDisplaySlot(
                    self._insertTextToDisplay,
                    button,
                )
                button.clicked.connect(buttonSlot)

    def _makeButtonDisplaySlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSLot(_):
            func(*args, **kwargs)

        return realSLot

    def _insertTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)
