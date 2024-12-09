from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QLineEdit,
    QMessageBox,
)
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QKeyEvent
from variables import (
    SMALL_FONT_SIZE,
    MEDIUM_FONT_SIZE,
    MINIMUM_WIDTH,
    BIG_FONT_SIZE,
    TEXT_MARGIN,
)
from utils import isEmpty, isNumOrDot, isValidNumber
import math


# Visualização da entrada de dados
class Display(QLineEdit):
    eqRequested = Signal()

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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]

        if isEnter:
            print(f"Enter pressionado, sinal enviado de {type(self).__name__}")
            self.eqRequested.emit()
            return event.ignore()


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

    def makeMsgBox(self):
        return QMessageBox(self)


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

    # Estilo dos botoes
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


# Funcionalidade dos botoes
class ButtonsGrid(QGridLayout):
    def __init__(
        self, display: Display, info: Info, window: MainWindow, *args, **kwargs
    ) -> None:
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
        self.window = window
        self._equation = ""
        self._equationInitialValue = "0"
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    # Getter e setter
    # Altera a Info() acima do display
    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def apagando(self):
        print(f"Sinal recebido em 'apagando' {type(self).__name__}")

    # Grid de botoes
    def _makeGrid(self):
        self.display.eqRequested.connect(self.apagando)

        # indexes, i e j
        # i row index; j column index
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                # Estilo dos botoes especiais
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertTextToDisplay, button)
                self._connectButtonClick(button, slot)

    # Acao ao clicar no botao
    def _connectButtonClick(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        # limpa o display
        if text == "C":
            self._connectButtonClick(button, self._clear)

        # backspace
        if text in "◀":
            self._connectButtonClick(button, self.display.backspace)

        # operadores
        if text in "+-/*^":
            self._connectButtonClick(
                button, self._makeSlot(self._operatorClicked, button)
            )

        # igual
        if text in "=":
            self._connectButtonClick(button, self._equal)

    def _makeSlot(self, func, *args, **kwargs):
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

    # reseta display e info
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()

    # operador clicado
    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError("Nada foi digitado")
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = buttonText
        self.equation = f"{self._left} {self._op} "

    def _equal(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showInfo("Conta incompleta")
            return

        self._right = float(displayText)
        self.equation = f"{self._left} {self._op} {self._right}"
        result = "error"

        try:
            if "^" in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError("Impossível dividir por zero")
        except OverflowError:
            print("Resultado é um número muito grande")

        self.display.clear()
        self.info.setText(f"{self.equation} = {result}")
        self._left = result
        self._right = None

        if result == "error":
            self._left = None

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()

    # Tentativa de evitar uso de 'eval()'
    #     if self._op == "+":
    #         result = self._sum(self._left, self._right)
    #     if self._op == "-":
    #         result = self._less(self._left, self._right)
    #     if self._op == "*":
    #         result = self._multiply(self._left, self._right)
    #     if self._op == "/":
    #         result = self._divide(self._left, self._right)

    #     if not isValidNumber(result):
    #         self._clear()
    #         self.info.setText(f"{self._equationInitialValue}")

    #     self.display.clear()
    #     self.info.setText(f"{self.equation} = {result}")
    #     self._left = result
    #     self._right = None

    # # soma
    # def _sum(self, leftNum, rightNum) -> str:
    #     n1, n2 = float(leftNum), float(rightNum)
    #     result = n1 + n2
    #     return str(result)

    # # menos
    # def _less(self, leftNum, rightNum):
    #     n1, n2 = float(leftNum), float(rightNum)
    #     result = n1 - n2
    #     return str(result)

    # def _multiply(self, leftNum, rightNum):
    #     n1, n2 = float(leftNum), float(rightNum)
    #     result = n1 * n2
    #     return str(result)

    # def _divide(self, leftNum, rightNum):
    #     n1, n2 = float(leftNum), float(rightNum)

    #     try:
    #         result = n1 / n2
    #     except ZeroDivisionError:
    #         return "Cannot divide by 0"

    #     return str(result)
