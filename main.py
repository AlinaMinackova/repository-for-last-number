import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.con = sqlite3.connect("coffee.db")
        self.pushButton.clicked.connect(self.update_result)
        self.pushButton_3.clicked.connect(self.add)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM coffee").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def add(self):
        self.window_2 = Window()
        self.window_2.show()


class Window(QMainWindow):
    def __init__(self, parent=None):
        self.modified = {}
        self.row = 0
        self.con = sqlite3.connect("coffee.db")
        super(Window, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.Pyui()

    def Pyui(self):
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.save_2)
        self.pushButton_2.clicked.connect(self.save_results)
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM coffee").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()
        self.row = item.row()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += " WHERE id = ?"
            print(que)
            cur.execute(que, (self.row + 1,))
            self.con.commit()
            self.modified.clear()
            self.row = 0
            self.destroy()

    def save_2(self):
        self.label_8.setText('')
        if not self.lineEdit_5.text().isdigit() or not self.lineEdit_6.text().isdigit():
            self.label_8.setText('Не все поля корректно заполнены')
        elif self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and self.lineEdit_3.text() != '' \
                and self.lineEdit_4.text() != '' and self.lineEdit_5.text() != '' and self.lineEdit_6.text() != '':
            con = sqlite3.connect('coffee.db')
            cur = con.cursor()
            cur.execute("""INSERT INTO coffee('title', 'roasting', 'type', 'taste', 'price', 'volume') 
            VALUES(?, ?, ?, ?, ?, ?)""",
                        (self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
                         self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text())).fetchall()
            con.commit()
            self.destroy()
        else:
            self.label_8.setText('Не все поля заполнены')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())