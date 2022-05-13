# -*- coding: utf-8 -*-

from PIL import Image
import os
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog
import atmesk1


class MyWindow(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = atmesk1.Ui_Dialog()
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.ui.setupUi(self)

    def get_size(self, read_file):
        # 获取图像的宽和高
        image = Image.open(read_file)
        width, height = image.size
        return width, height

    def watermark(self, path, num, xs):

        img = []

        img.append(Image.open("./watermark-final/" + num[0] + '.png'))
        img.append(Image.open("./watermark-final/" + num[1] + '.png'))
        img.append(Image.open("./watermark-final/" + num[2] + '.png'))
        img.append(Image.open("./watermark-final/" + num[3] + '.png'))
        img.append(Image.open("./watermark-final/21at.png"))

        img[0] = img[0].transpose(Image.FLIP_TOP_BOTTOM)
        img[1] = img[1].transpose(Image.FLIP_TOP_BOTTOM)
        img[2] = img[2].transpose(Image.FLIP_TOP_BOTTOM)
        img[3] = img[3].transpose(Image.FLIP_TOP_BOTTOM)
        img[4] = img[4].transpose(Image.FLIP_TOP_BOTTOM)

        file_list = os.listdir(path)
        for file in file_list:
            cur_path = os.path.join(path, file)
            if not os.path.isdir(cur_path):
                continue
            tilelist = os.listdir(cur_path)
            all_tiles = []
            for tile in tilelist:
                if os.path.splitext(tile)[-1] == '.jpg':
                    tilepath = os.path.join(cur_path, tile)
                    all_tiles.append(tilepath)

            i = 0
            for tile in all_tiles:
                i += 1
                xs = int(xs)
                if i % xs > 0:
                    continue
                self.ui.textBrowser.append(tile + " add " + num)
                im = Image.open(tile)

                width = self.get_size(tile)[0]
                height = self.get_size(tile)[1]

                im.paste(img[0], (height // 5, width * 2 // 3), mask=img[0].split()[3])
                im.paste(img[1], (height // 5 + 10, width * 2 // 3), mask=img[1].split()[3])
                im.paste(img[2], (height // 5 + 20, width * 2 // 3), mask=img[2].split()[3])
                im.paste(img[3], (height // 5 + 30, width * 2 // 3), mask=img[3].split()[3])
                im.paste(img[4], (height // 5 + 80, width * 2 // 3), mask=img[4].split()[3])

                im.save(tile)

            all_tiles.clear()

        self.ui.textBrowser.append("watermark: success")

    def runmesk(self):
        xs = self.ui.spinBox.text()
        num = self.ui.lineEdit.text()
        path = self.ui.lineEdit_2.text()

        if num == '':
            self.ui.textBrowser.append("请将参数输入完全")
        else:
            self.ui.textBrowser.append("开始")
            self.watermark(path, num, xs)

    def choose(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
        self.ui.lineEdit_2.setText(directory)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
