import requests
import sys
import os
from random import choice
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
from functions import get_coords, get_map, get_bbox_part

cities = ["Димитровград", "Санкт-Петербург", "Москва", "Красноярск", "Новосибирск",
          "Екатеринбург", "Казань", "Нижний Новгород", "Челябинск", "Самара", "Уфа",
          "Ростов-на-Дону", "Омск", "Краснодар", "Воронеж", "Пермь", "Волгоград", "Саратов",
          "Тюмень", "Тольятти"]

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.map_file = "map.png"
        self.initUI()

    def changeImage(self):
        city = choice(cities)
        type = choice(["map", "sat"])
        response = get_map({
            "bbox": get_bbox_part(get_coords(city, bbox=True), type),
            "l": type
        })

        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.image.setPixmap(QPixmap(self.map_file))

    def initUI(self):
        self.setFixedSize(*SCREEN_SIZE)
        self.setWindowTitle('Угадай-ка город')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)

        self.changeImage()

    def mousePressEvent(self, event):
        if event.button() in (1, 2):
            self.changeImage()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.changeImage()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
