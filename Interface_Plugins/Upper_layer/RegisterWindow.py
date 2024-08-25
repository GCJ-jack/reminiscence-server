import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ctypes
from time import strftime


class RegisterWindow(QtWidgets.QMainWindow):
    # signals Register Window

    onEmpty = QtCore.pyqtSignal()
    onData = QtCore.pyqtSignal()
    onAlreadyRegistered = QtCore.pyqtSignal()
    onNotRegistered = QtCore.pyqtSignal()

    def __init__(self):
        super(RegisterWindow, self).__init__()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Setting tools
        self.gxlabels = {}
        self.fontlabels = {}
        self.controlButtons = {}
        self.getData = {}

        # Setting the graphics modules
        self.init_ui(current_dir)

    def init_ui(self,current_path):
        # Set window title
        self.setWindowTitle("Reminisicence Interface")
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
        self.background.setPixmap(QtGui.QPixmap(os.path.join(current_path, "ImgGui/black_menu.png")))
        self.background.setScaledContents(True)

        # Graphics Labels

        # Label
        self.gxlabels["date"] = QtWidgets.QLabel(self)
        self.gxlabels["date"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.03), int(self.winsize_v * 0.08), int(self.winsize_h * 0.5),
                         int(self.winsize_v * 0.08)))
        icon_date = QtGui.QPixmap(os.path.join(current_path, "ImgGui/date_main.png"))
        icon_date = icon_date.scaled(int(self.winsize_h * 0.5), int(self.winsize_v * 0.08), QtCore.Qt.KeepAspectRatio,
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
        icon_hide = icon_hide.scaled(int(self.winsize_h * 0.04), int(self.winsize_v * 0.04), QtCore.Qt.KeepAspectRatio,
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

        # Minimenu

        self.gxlabels["mini_re"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_re"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.1), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_register = QtGui.QPixmap(os.path.join(current_path, "ImgGui/save_re.png"))
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

        self.gxlabels["mini_sun"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_sun"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.875), int(self.winsize_v * 0.905), int(self.winsize_h * 0.04),
                         int(self.winsize_v * 0.04)))
        icon_sun = QtGui.QPixmap(os.path.join(current_path, "ImgGui/sun_main.png"))
        icon_sun = icon_sun.scaled(int(self.winsize_h * 0.04), int(self.winsize_v * 0.04), QtCore.Qt.KeepAspectRatio,
                                   transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["mini_sun"].setPixmap(icon_sun)

        # Register icon

        self.gxlabels["register"] = QtWidgets.QLabel(self)
        self.gxlabels["register"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.2), int(self.winsize_v * 0.3), int(self.winsize_h * 0.4),
                         int(self.winsize_v * 0.4)))
        icon_re = QtGui.QPixmap(os.path.join(current_path, "ImgGui/re_rewindow.png"))
        icon_re = icon_re.scaled(int(self.winsize_h * 0.4), int(self.winsize_v * 0.4), QtCore.Qt.KeepAspectRatio,
                                 transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["register"].setPixmap(icon_re)

        # Data icons

        self.gxlabels["name"] = QtWidgets.QLabel(self)
        self.gxlabels["name"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.5), int(self.winsize_v * 0.35), int(self.winsize_h * 0.3),
                         int(self.winsize_v * 0.08)))
        icon_date = QtGui.QPixmap(os.path.join(current_path, "ImgGui/date_main.png"))
        icon_date = icon_date.scaled(int(self.winsize_h * 0.3), int(self.winsize_v * 0.08), QtCore.Qt.KeepAspectRatio,
                                     transformMode=QtCore.Qt.SmoothTransformation)
        self.gxlabels["name"].setPixmap(icon_date)

        self.fontlabels["name"] = QtWidgets.QLabel(self)
        self.fontlabels["name"].setText("Name:")
        self.fontlabels["name"].setStyleSheet("color:black;font:bold;font-size:18px; Sans Serif")
        self.fontlabels["name"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.55), int(self.winsize_v * 0.35), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.05)))

        self.gxlabels["age"] = QtWidgets.QLabel(self)
        self.gxlabels["age"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.5), int(self.winsize_v * 0.45), int(self.winsize_h * 0.3),
                         int(self.winsize_v * 0.08)))
        self.gxlabels["age"].setPixmap(icon_date)

        self.fontlabels["age"] = QtWidgets.QLabel(self)
        self.fontlabels["age"].setText("Age:")
        self.fontlabels["age"].setStyleSheet("color:black;font:bold;font-size:18px; Sans Serif")
        self.fontlabels["age"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.55), int(self.winsize_v * 0.42), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.08)))

        self.gxlabels["gender"] = QtWidgets.QLabel(self)
        self.gxlabels["gender"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.5), int(self.winsize_v * 0.55), int(self.winsize_h * 0.3),
                         int(self.winsize_v * 0.08)))
        self.gxlabels["gender"].setPixmap(icon_date)

        self.fontlabels["gender"] = QtWidgets.QLabel(self)
        self.fontlabels["gender"].setText("Gender:")
        self.fontlabels["gender"].setStyleSheet("color:black;font:bold;font-size:18px; Sans Serif")
        self.fontlabels["gender"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.55), int(self.winsize_v * 0.52), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.08)))

        self.gxlabels["ID"] = QtWidgets.QLabel(self)
        self.gxlabels["ID"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.5), int(self.winsize_v * 0.65), int(self.winsize_h * 0.3),
                         int(self.winsize_v * 0.08)))
        self.gxlabels["ID"].setPixmap(icon_date)

        self.fontlabels["ID"] = QtWidgets.QLabel(self)
        self.fontlabels["ID"].setText("ID:")
        self.fontlabels["ID"].setStyleSheet("color:black;font:bold;font-size:18px; Sans Serif")
        self.fontlabels["ID"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.55), int(self.winsize_v * 0.62), int(self.winsize_h * 0.3),
                         int(self.winsize_h * 0.08)))

        # Buttons

        self.controlButtons["close"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['close'].setIconSize(QSize(0, 0))
        self.controlButtons['close'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.945), int(self.winsize_v * 0.04), int(self.winsize_h * 0.035),
                         int(self.winsize_v * 0.045)))

        self.controlButtons["hide"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['hide'].setIconSize(QSize(0, 0))
        self.controlButtons['hide'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.895), int(self.winsize_v * 0.04), int(self.winsize_h * 0.035),
                         int(self.winsize_v * 0.045)))

        # Mini Buttons

        self.controlButtons["mini_re"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_re'].setIconSize(QSize(0, 0))
        self.controlButtons['mini_re'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.095), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.controlButtons["mini_rem"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_rem'].setIconSize(QSize(0, 0))
        self.controlButtons['mini_rem'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.395), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.controlButtons["mini_db"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_db'].setIconSize(QSize(0, 0))
        self.controlButtons['mini_db'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.695), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.controlButtons["mini_sta"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_sta'].setIconSize(QSize(0, 0))
        self.controlButtons['mini_sta'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.245), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.controlButtons["mini_avatar"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_avatar'].setIconSize(QSize(0, 0))
        self.controlButtons['mini_avatar'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.545), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        # Edit labels

        self.getData['name'] = QtWidgets.QLineEdit(self)
        self.getData['name'].setStyleSheet("font-size:18px; Sans Serif")
        self.getData['name'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.65), int(self.winsize_v * 0.353), int(self.winsize_h * 0.2),
                         int(self.winsize_h * 0.04)))

        self.getData['age'] = QtWidgets.QLineEdit(self)
        self.getData['age'].setStyleSheet("font-size:18px; Sans Serif")
        self.getData['age'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.65), int(self.winsize_v * 0.453), int(self.winsize_h * 0.2),
                         int(self.winsize_h * 0.04)))

        self.getData['ID'] = QtWidgets.QLineEdit(self)
        self.getData['ID'].setStyleSheet("font-size:18px; Sans Serif")
        self.getData['ID'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.65), int(self.winsize_v * 0.653), int(self.winsize_h * 0.2),
                         int(self.winsize_h * 0.04)))

        self.getData['gender'] = QtWidgets.QComboBox(self)
        self.getData['gender'].setStyleSheet("font-size:18px; Sans Serif")
        self.getData['gender'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.65), int(self.winsize_v * 0.553), int(self.winsize_h * 0.2),
                         int(self.winsize_h * 0.04)))
        self.getData['gender'].addItem("M")
        self.getData['gender'].addItem("F")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.set_time)
        self.timer.start(1000)

        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.9), int(self.winsize_v * 0.9), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.055)))
        self.lcd.display(strftime("%H" + ":" + "%M" + ":" + "%S"))
        self.lcd.setDigitCount(8)

        self.closeButton(self.confirm_close)
        self.hideButton()
        self.set_date()
        self.set_time()

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

    def set_date(self):
        today = QtCore.QDate.currentDate()
        self.currdate.setText(today.toString())

    def set_time(self):
        self.lcd.display(strftime("%H" + ":" + "%M" + ":" + "%S"))

    def get_patient_data(self):
        name = str(self.getData['name'].text())
        age = str(self.getData['age'].text())
        gender = str(self.getData['gender'].currentText())
        id_number = str(self.getData['ID'].text())
        self.patient = {'name': name, 'id': id_number, 'age': age, 'gender': gender}
        return self.patient

    def registerButton(self, f):
        self.controlButtons["mini_re"].clicked.connect(f)

    def avatarButton(self, f):
        self.controlButtons["mini_avatar"].clicked.connect(f)

    def statisticsButton(self, f):
        self.controlButtons["mini_sta"].clicked.connect(f)

    def dbButton(self, f):
        self.controlButtons["mini_db"].clicked.connect(f)

    def registerReminiscence(self, f):
        self.controlButtons["mini_rem"].clicked.connect(f)
        print('Register Reminisicence')

    def set_date(self):
        today = QtCore.QDate.currentDate()
        self.currdate.setText(today.toString())


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     GUI = RegisterWindow()
#     GUI.registerButton(GUI.get_patient_data)
#     GUI.show()
#     sys.exit(app.exec_())


# main()
