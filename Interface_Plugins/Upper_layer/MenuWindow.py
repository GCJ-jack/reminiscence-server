import os
import sys
import platform

import self
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ctypes
from time import strftime


class MenuWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MenuWindow, self).__init__()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 设置基础路径

        # Setting tools
        self.gxlabels = {}
        self.fontlabels = {}
        self.controlButtons = {}

        # Setting the graphics modules
        self.init_ui(current_dir)

        # Setting the signals of the GUI
        self.set_signals()

    def init_ui(self, current_path):
        # Set window title
        self.setWindowTitle("Reminisicence Interface")
        image_path = os.path.join(current_path, "ImgGui/black_menu.png")
        # Set window size
        if sys.platform == "win32":
            self.user32 = ctypes.windll.user32
            self.screensize = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1)
        else:
            self.screensize = QtWidgets.QDesktopWidget().screenGeometry().width(), QtWidgets.QDesktopWidget().screenGeometry().height()
        # Resize window
        self.winsize_h = int(self.screensize[0])
        self.winsize_v = int(self.screensize[1])
        self.resize(self.winsize_h, self.winsize_v)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Setting background image
        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.background.setPixmap(QtGui.QPixmap(image_path))
        self.background.setScaledContents(True)

        # Graphics Labels

        # Label
        self.gxlabels["date"] = QtWidgets.QLabel(self)
        self.gxlabels["date"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.03), int(self.winsize_v * 0.08), int(self.winsize_h * 0.5),
                         int(self.winsize_v * 0.08)))
        icon_date = QtGui.QPixmap(os.path.join(current_path, "ImgGui/date_main.png"))
        icon_date = icon_date.scaled(int(self.winsize_h * 0.5), int(self.winsize_v * 0.08),
                                     QtCore.Qt.KeepAspectRatio,
                                     transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["date"].setPixmap(icon_date)

        self.currdate = QtWidgets.QLabel(self)
        self.currdate.setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.05), int(self.winsize_v * 0.07), int(self.winsize_h * 0.15),
                         int(self.winsize_v * 0.1)))
        self.currdate.setStyleSheet("color:white;font:bold;font-size:14px; Sans Serif")

        # Reniniscence Title

        self.gxlabels["WinName"] = QtWidgets.QLabel(self)
        self.gxlabels["WinName"].setText("Reminisicence Interface")
        self.gxlabels["WinName"].setStyleSheet("color:white;font:bold;font-size:18px; Sans Serif")
        self.gxlabels["WinName"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.4), int(self.winsize_v * 0.04), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.05)))

        # Hide

        self.gxlabels["hide"] = QtWidgets.QLabel(self)
        self.gxlabels["hide"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.9), int(self.winsize_v * 0.04), int(self.winsize_h * 0.04),
                         int(self.winsize_v * 0.04)))
        icon_hide = QtGui.QPixmap(os.path.join(current_path, "ImgGui/hide_main.png"))
        icon_hide = icon_hide.scaled(int(self.winsize_h * 0.04), int(self.winsize_v * 0.04),
                                     QtCore.Qt.KeepAspectRatio,
                                     transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["hide"].setPixmap(icon_hide)

        # Close

        self.gxlabels["close"] = QtWidgets.QLabel(self)
        self.gxlabels["close"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.95), int(self.winsize_v * 0.04), int(self.winsize_h * 0.04),
                         int(self.winsize_v * 0.04)))
        icon_close = QtGui.QPixmap(os.path.join(current_path, "ImgGui/close_main.png"))
        icon_close = icon_close.scaled(int(self.winsize_h * 0.04), int(self.winsize_v * 0.04),
                                       QtCore.Qt.KeepAspectRatio,
                                       transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["close"].setPixmap(icon_close)

        # Register

        self.gxlabels["register"] = QtWidgets.QLabel(self)
        self.gxlabels["register"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.22), int(self.winsize_v * 0.35), int(self.winsize_h * 0.17),
                         int(self.winsize_v * 0.17)))
        icon_register = QtGui.QPixmap(os.path.join(current_path, "ImgGui/register_menu.png"))
        icon_register = icon_register.scaled(int(self.winsize_h * 0.17), int(self.winsize_v * 0.17),
                                             QtCore.Qt.KeepAspectRatio,
                                             transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["register"].setPixmap(icon_register)

        self.fontlabels["register"] = QtWidgets.QLabel(self)
        self.fontlabels["register"].setText("Register")
        self.fontlabels["register"].setStyleSheet("color:white;font-size:17px; Sans Serif")
        self.fontlabels["register"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.24), int(self.winsize_v * 0.5), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.05)))

        # AvatarSett

        self.gxlabels["avatar"] = QtWidgets.QLabel(self)
        self.gxlabels["avatar"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.45), int(self.winsize_v * 0.35), int(self.winsize_h * 0.17),
                         int(self.winsize_v * 0.17)))
        icon_avatar = QtGui.QPixmap(os.path.join(current_path, "ImgGui/avatar_menu.png"))
        icon_avatar = icon_avatar.scaled(int(self.winsize_h * 0.17), int(self.winsize_v * 0.17),
                                         QtCore.Qt.KeepAspectRatio,
                                         transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["avatar"].setPixmap(icon_avatar)

        self.fontlabels["avatar"] = QtWidgets.QLabel(self)
        self.fontlabels["avatar"].setText("Avatar Settings")
        self.fontlabels["avatar"].setStyleSheet("color:white;font-size:17px; Sans Serif")
        self.fontlabels["avatar"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.46), int(self.winsize_v * 0.5), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.05)))

        # Statistics

        self.gxlabels["statistics"] = QtWidgets.QLabel(self)
        self.gxlabels["statistics"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.67), int(self.winsize_v * 0.35), int(self.winsize_h * 0.17),
                         int(self.winsize_v * 0.17)))
        icon_statis = QtGui.QPixmap(os.path.join(current_path, "ImgGui/stati_menu.png"))
        icon_statis = icon_statis.scaled(int(self.winsize_h * 0.17), int(self.winsize_v * 0.17),
                                         QtCore.Qt.KeepAspectRatio,
                                         transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["statistics"].setPixmap(icon_statis)

        self.fontlabels["statistics"] = QtWidgets.QLabel(self)
        self.fontlabels["statistics"].setText("Statistics")
        self.fontlabels["statistics"].setStyleSheet("color:white;font-size:17px; Sans Serif")
        self.fontlabels["statistics"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.69), int(self.winsize_v * 0.5), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.05)))

        # Database

        self.gxlabels["db"] = QtWidgets.QLabel(self)
        self.gxlabels["db"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.32), int(self.winsize_v * 0.60), int(self.winsize_h * 0.17),
                         int(self.winsize_v * 0.17)))
        icon_db = QtGui.QPixmap(os.path.join(current_path, "ImgGui/db_menu.png"))
        icon_db = icon_db.scaled(int(self.winsize_h * 0.17), int(self.winsize_v * 0.17), QtCore.Qt.KeepAspectRatio,
                                 transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["db"].setPixmap(icon_db)

        self.fontlabels["db"] = QtWidgets.QLabel(self)
        self.fontlabels["db"].setText("Database")
        self.fontlabels["db"].setStyleSheet("color:white;font-size:17px; Sans Serif")
        self.fontlabels["db"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.34), int(self.winsize_v * 0.75), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.05)))

        # Reminiscence

        self.gxlabels["rem"] = QtWidgets.QLabel(self)
        self.gxlabels["rem"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.58), int(self.winsize_v * 0.60), int(self.winsize_h * 0.17),
                         int(self.winsize_v * 0.17)))
        icon_r = QtGui.QPixmap(os.path.join(current_path, "ImgGui/rem_menu.png"))
        icon_r = icon_r.scaled(int(self.winsize_h * 0.17), int(self.winsize_v * 0.17), QtCore.Qt.KeepAspectRatio,
                               transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["rem"].setPixmap(icon_r)

        self.fontlabels["rem"] = QtWidgets.QLabel(self)
        self.fontlabels["rem"].setText("Reminisicence Session")
        self.fontlabels["rem"].setStyleSheet("color:white;font-size:17px; Sans Serif")
        self.fontlabels["rem"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.57), int(self.winsize_v * 0.75), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.05)))

        # Minimenu

        self.gxlabels["mini_re"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_re"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.1), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_register = QtGui.QPixmap(os.path.join(current_path, "ImgGui/register_menu.png"))
        icon_register = icon_register.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08),
                                             QtCore.Qt.KeepAspectRatio,
                                             transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["mini_re"].setPixmap(icon_register)

        self.gxlabels["mini_sta"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_sta"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.25), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_statis = QtGui.QPixmap(os.path.join(current_path, "ImgGui/stati_menu.png"))
        icon_statis = icon_statis.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08),
                                         QtCore.Qt.KeepAspectRatio,
                                         transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["mini_sta"].setPixmap(icon_statis)

        self.gxlabels["mini_rem"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_rem"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.4), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_r = QtGui.QPixmap(os.path.join(current_path, "ImgGui/rem_menu.png"))
        icon_r = icon_r.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08), QtCore.Qt.KeepAspectRatio,
                               transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["mini_rem"].setPixmap(icon_r)

        self.gxlabels["mini_avatar"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_avatar"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.55), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_avatar = QtGui.QPixmap(os.path.join(current_path, "ImgGui/avatar_menu.png"))
        icon_avatar = icon_avatar.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08),
                                         QtCore.Qt.KeepAspectRatio,
                                         transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["mini_avatar"].setPixmap(icon_avatar)

        self.gxlabels["mini_db"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_db"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.7), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_db = QtGui.QPixmap(os.path.join(current_path, "ImgGui/db_menu.png"))
        icon_db = icon_db.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08), QtCore.Qt.KeepAspectRatio,
                                 transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["mini_db"].setPixmap(icon_db)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.set_time)
        self.timer.start(1000)

        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.9), int(self.winsize_v * 0.9), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.055)))
        self.lcd.display(strftime("%H" + ":" + "%M" + ":" + "%S"))
        self.lcd.setDigitCount(8)

        self.gxlabels["mini_sun"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_sun"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.875), int(self.winsize_v * 0.905), int(self.winsize_h * 0.04),
                         int(self.winsize_v * 0.04)))
        icon_sun = QtGui.QPixmap(os.path.join(current_path, "ImgGui/sun_main.png"))
        icon_sun = icon_sun.scaled(int(self.winsize_h * 0.04), int(self.winsize_v * 0.04),
                                   QtCore.Qt.KeepAspectRatio,
                                   transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["mini_sun"].setPixmap(icon_sun)

        # Buttons

        self.controlButtons["close"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['close'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['close'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.945), int(self.winsize_v * 0.04), int(self.winsize_h * 0.035),
                         int(self.winsize_v * 0.045)))

        self.controlButtons["hide"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['hide'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['hide'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.895), int(self.winsize_v * 0.04), int(self.winsize_h * 0.035),
                         int(self.winsize_v * 0.045)))

        self.controlButtons["register"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['register'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['register'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.215), int(self.winsize_v * 0.345), int(self.winsize_h * 0.11),
                         int(self.winsize_v * 0.18)))

        self.controlButtons["avatar"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['avatar'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['avatar'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.445), int(self.winsize_v * 0.345), int(self.winsize_h * 0.11),
                         int(self.winsize_v * 0.18)))

        self.controlButtons["statistics"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['statistics'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['statistics'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.665), int(self.winsize_v * 0.345), int(self.winsize_h * 0.11),
                         int(self.winsize_v * 0.18)))

        self.controlButtons["db"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['db'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['db'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.315), int(self.winsize_v * 0.595), int(self.winsize_h * 0.11),
                         int(self.winsize_v * 0.18)))

        self.controlButtons["rem"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['rem'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['rem'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.575), int(self.winsize_v * 0.595), int(self.winsize_h * 0.11),
                         int(self.winsize_v * 0.18)))

        # Mini Buttons

        self.controlButtons["mini_re"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_re'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['mini_re'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.095), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.controlButtons["mini_rem"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_rem'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['mini_rem'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.395), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.controlButtons["mini_db"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_db'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['mini_db'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.695), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.controlButtons["mini_sta"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_sta'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['mini_sta'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.245), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.gxlabels["mini_sun"].setPixmap(icon_sun)

        self.controlButtons["mini_avatar"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_avatar'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['mini_avatar'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.545), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.closeButton(self.confirm_close)
        self.hideButton()
        self.set_date()
        self.set_time()
        self.show()

    def set_signals(self):
        pass

    def closeButton(self, f):
        self.controlButtons["close"].clicked.connect(f)

    def confirm_close(self):
        choice = QtWidgets.QMessageBox.question(self, 'Close?',
                                                "Are you sure you want to close",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def hideButton(self):
        self.controlButtons["hide"].clicked.connect(self.showMinimized)

    def registerButton(self, f):
        print('here')
        self.controlButtons["register"].clicked.connect(f)
        self.controlButtons["mini_re"].clicked.connect(f)

    def avatarButton(self, f):
        self.controlButtons["avatar"].clicked.connect(f)
        self.controlButtons["mini_avatar"].clicked.connect(f)

    def statisticsButton(self, f):
        self.controlButtons["statistics"].clicked.connect(f)
        self.controlButtons["mini_sta"].clicked.connect(f)

    def dbButton(self, f):
        self.controlButtons["db"].clicked.connect(f)
        self.controlButtons["mini_db"].clicked.connect(f)

    def reminiscenceButton(self, f):
        self.controlButtons["rem"].clicked.connect(f)
        self.controlButtons["mini_rem"].clicked.connect(f)

    # self.hide()

    def set_date(self):
        today = QtCore.QDate.currentDate()
        self.currdate.setText(today.toString())

    def set_time(self):
        self.lcd.display(strftime("%H" + ":" + "%M" + ":" + "%S"))


def main():
    app = QtWidgets.QApplication(sys.argv)
    GUI = MenuWindow()
    GUI.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
