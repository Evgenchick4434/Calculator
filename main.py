import sys
from typing import Union, Optional
from operator import add, sub, mul, truediv
from decimal import *
import decimal

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase

from design import Ui_MainWindow

operations = {
    '+': add,
    '-': sub,
    '×': mul,
    '/': truediv
}
class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_max_len = self.ui.le_entry.maxLength()

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        #digits
        self.ui.btn_0.clicked.connect(lambda: self.add_digit('0'))
        self.ui.btn_1.clicked.connect(lambda: self.add_digit('1'))
        self.ui.btn_2.clicked.connect(lambda: self.add_digit('2'))
        self.ui.btn_3.clicked.connect(lambda: self.add_digit('3'))
        self.ui.btn_4.clicked.connect(lambda: self.add_digit('4'))
        self.ui.btn_5.clicked.connect(lambda: self.add_digit('5'))
        self.ui.btn_6.clicked.connect(lambda: self.add_digit('6'))
        self.ui.btn_7.clicked.connect(lambda: self.add_digit('7'))
        self.ui.btn_8.clicked.connect(lambda: self.add_digit('8'))
        self.ui.btn_9.clicked.connect(lambda: self.add_digit('9'))

        #actions
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_neg.clicked.connect(self.negate)
        self.ui.btn_backspace.clicked.connect(self.backspace)

        #math
        self.ui.btn_calc.clicked.connect(self.calculate)
        self.ui.btn_plus.clicked.connect(lambda: self.math_operation('+'))
        self.ui.btn_sub.clicked.connect(lambda: self.math_operation('-'))
        self.ui.btn_mul.clicked.connect(lambda: self.math_operation('×'))
        self.ui.btn_div.clicked.connect(lambda: self.math_operation('/'))
    def add_digit(self, btn_text: str) -> None:
        self.clear_temp_if_equality()
        if self.ui.le_entry.text() == '0':
            self.ui.le_entry.setText(btn_text)
        else:
            self.ui.le_entry.setText(self.ui.le_entry.text() + btn_text)

    def add_point(self) -> None:
        self.clear_temp_if_equality()
        if '.' not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')

    def negate(self):
        self.clear_temp_if_equality()
        entry = self.ui.le_entry.text()

        if '-' not in entry:
            if entry != '0':
                entry = '-' + entry
        else:
            entry = entry[1:]
        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.ui.le_entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.ui.le_entry.setMaxLength(self.entry_max_len)

        self.ui.le_entry.setText(entry)

    def backspace(self) -> None:
        self.clear_temp_if_equality()
        entry = self.ui.le_entry.text()
        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.ui.le_entry.setText('0')
            else:
                self.ui.le_entry.setText(entry[:-1])
        else:
            self.ui.le_entry.setText('0')

    def clear_all(self) -> None:
        self.ui.le_entry.setText('0')
        self.ui.lbl_temp.clear()
        self.disable_buttons(False)

    def clear_entry(self) -> None:
        self.clear_temp_if_equality()
        self.ui.le_entry.setText('0')
        self.disable_buttons(False)

    def clear_temp_if_equality(self) -> None:
        if self.get_math_sign() == '=':
            self.ui.lbl_temp.clear()

    @staticmethod
    def remove_trailing_zeros(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    def add_temp(self, math_sign: str):
        if not self.ui.lbl_temp.text() or self.get_math_sign() == '=':
            self.ui.lbl_temp.setText(self.remove_trailing_zeros(self.ui.le_entry.text())  + f' {math_sign} ')
            self.ui.le_entry.setText('0')

    def get_entry_num(self) -> Union[int, float, ]:
        entry = self.ui.le_entry.text().strip('.')

        return float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> Union[int, float, None]:
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip('.').split()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]:
        if self.ui.lbl_temp.text():
            return self.ui.lbl_temp.text().strip('.').split()[-1]

    def calculate(self) -> Optional[str]:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()

        if temp:
            try:
                result = self.remove_trailing_zeros(
                    str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num()))
                )
                self.ui.lbl_temp.setText(temp + self.remove_trailing_zeros(entry) + ' =')
                self.ui.le_entry.setText(result)
                return result
            except KeyError:
                pass
            except ZeroDivisionError:
                self.ui.le_entry.setText('Error')
                self.disable_buttons(True)

    def disable_buttons(self, disable: bool) -> None:
        self.ui.btn_1.setDisabled(disable)
        self.ui.btn_2.setDisabled(disable)
        self.ui.btn_3.setDisabled(disable)
        self.ui.btn_4.setDisabled(disable)
        self.ui.btn_5.setDisabled(disable)
        self.ui.btn_6.setDisabled(disable)
        self.ui.btn_7.setDisabled(disable)
        self.ui.btn_8.setDisabled(disable)
        self.ui.btn_9.setDisabled(disable)
        self.ui.btn_0.setDisabled(disable)
        self.ui.btn_mul.setDisabled(disable)
        self.ui.btn_backspace.setDisabled(disable)
        self.ui.btn_div.setDisabled(disable)
        self.ui.btn_neg.setDisabled(disable)
        self.ui.btn_calc.setDisabled(disable)
        self.ui.btn_plus.setDisabled(disable)
        self.ui.btn_sub.setDisabled(disable)
        self.ui.btn_point.setDisabled(disable)

        color = 'color: #888;' if disable else 'color: white;'
        self.change_buttons_color(color)

    def change_buttons_color(self, css_color: str) -> None:
        self.ui.btn_1.setStyleSheet(css_color)
        self.ui.btn_2.setStyleSheet(css_color)
        self.ui.btn_3.setStyleSheet(css_color)
        self.ui.btn_4.setStyleSheet(css_color)
        self.ui.btn_5.setStyleSheet(css_color)
        self.ui.btn_6.setStyleSheet(css_color)
        self.ui.btn_7.setStyleSheet(css_color)
        self.ui.btn_8.setStyleSheet(css_color)
        self.ui.btn_9.setStyleSheet(css_color)
        self.ui.btn_0.setStyleSheet(css_color)
        self.ui.btn_mul.setStyleSheet(css_color)
        self.ui.btn_backspace.setStyleSheet(css_color)
        self.ui.btn_div.setStyleSheet(css_color)
        self.ui.btn_neg.setStyleSheet(css_color)
        self.ui.btn_calc.setStyleSheet(css_color)
        self.ui.btn_plus.setStyleSheet(css_color)
        self.ui.btn_sub.setStyleSheet(css_color)
        self.ui.btn_point.setStyleSheet(css_color)

    def math_operation(self, math_sign: str):
        temp = self.ui.lbl_temp.text()

        if not temp:
            self.add_temp(math_sign)
        else:
            if self.get_math_sign() != math_sign:
                if self.get_math_sign() == '=':
                    self.add_temp(math_sign)
                else:
                    self.ui.lbl_temp.setText(temp[:-2] + f' {math_sign} ')
            else:
                self.ui.lbl_temp.setText(self.calculate() + f' {math_sign} ')



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
