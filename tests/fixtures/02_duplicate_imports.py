"""同一库多子模块、多次导入测试。"""
import numpy
import numpy.linalg as la
from numpy import zeros

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color


class Worker(QThread):
    status = pyqtSignal(str)

    def run(self):
        self.status.emit("ok")


def main():
    app = QApplication([])
    data = zeros((2, 2))
    print(la.norm(data))
    color = convert_color(sRGBColor(0.5, 0.5, 0.5), LabColor)
    print(delta_e_cie2000(color, color))
    return app
