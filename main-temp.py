'''
Descripttion: 
version: 
Author: Cai Weichao
Date: 2023-02-10 14:39:54
LastEditors: Cai Weichao
LastEditTime: 2023-02-10 15:37:24
'''
from GUI.GUI import MainWindow
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import sys

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # 使得显示的UI与预览的一致
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
