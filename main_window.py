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
    negativePressed = Signal()
    eqPressed = Signal()
    delPressed = Signal()
    escPressed = Signal()
    imputPressed = Signal(str)
    operatorPressed = Signal(str)

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

    # entrada de dados pelo teclado
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isBackspace = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]
        isNegative = key in [KEYS.Key_N]
        isOperator = key in [
            KEYS.Key_Minus,
            KEYS.Key_Plus,
            KEYS.Key_Slash,
            KEYS.Key_Asterisk,
            KEYS.Key_P,
        ]

        if isNegative:
            self.negativePressed.emit()
            return event.ignore()

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()

        if isBackspace:
            self.delPressed.emit()
            return event.ignore()

        if isEsc:
            self.escPressed.emit()
            return event.ignore()

        if isOperator:
            if text.lower() == "p":
                text = "^"
            self.operatorPressed.emit(text)
            return event.ignore()

        # Não passar daqui
        if isEmpty(text):
            return event.ignore()

        if isNumOrDot(text):
            self.imputPressed.emit(text)
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

    # Ultima acao a ser feita
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
            ["N", "0", ".", "="],
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

    # Grid de botoes
    def _makeGrid(self):
        # botoes pressionados
        self.display.eqPressed.connect(self._equal)
        self.display.delPressed.connect(self.display.backspace)
        self.display.escPressed.connect(self._clear)
        self.display.imputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)
        self.display.negativePressed.connect(self._negativeNumber)

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
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClick(button, slot)

    # Acao ao clicar no botao
    def _connectButtonClick(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        # limpa o display
        if text == "C":
            self._connectButtonClick(button, self._clear)

        if text == "N":
            self._connectButtonClick(button, self._negativeNumber)

        # backspace
        if text in "◀":
            self._connectButtonClick(button, self.display.backspace)

        # operadores
        if text in "+-/*^":
            self._connectButtonClick(
                button, self._makeSlot(self._configLeftOp, text)
            )

        # igual
        if text in "=":
            self._connectButtonClick(button, self._equal)

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSLot(_):
            func(*args, **kwargs)

        return realSLot

    @Slot()
    def _negativeNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = float(displayText) * -1

        if number.is_integer():
            number = int(number)

        self.display.setText(str(number))

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)

    # reseta display e info
    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()

    # operador clicado
    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError("Nada foi digitado")
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = text
        self.equation = f"{self._left} {self._op} "

    @Slot()
    def _equal(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
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
            self._showError("Resultado é um número muito grande")

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
