import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from time import strftime


class CalibrationWindow(QtWidgets.QMainWindow):
    # Signals
    onCalibration_run = QtCore.pyqtSignal()
    onCalibration_end = QtCore.pyqtSignal()

    def __init__(self):
        super(CalibrationWindow, self).__init__()

        # Setting tools
        self.gxlabels = {}
        self.fontlabels = {}
        self.controlButtons = {}
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Settings the graphics modules
        self.init_ui(current_dir)

    def init_ui(self, current_path):
        # Set window title
        self.setWindowTitle("Calibration Window")

        # Get screen size
        screen = QtWidgets.QApplication.primaryScreen()
        size = screen.size()
        self.winsize_h = size.width()
        self.winsize_v = size.height()

        # Resize window
        self.resize(self.winsize_h, self.winsize_v)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Setting background image
        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.background.setPixmap(QtGui.QPixmap(os.path.join(current_path, "ImgGui/black_menu.png")))
        self.background.setScaledContents(True)

        # Graphics Labels
        # "Interface_Plugins/Upper_layer/ImgGui/date_main

        # Label
        self.gxlabels["date"] = QtWidgets.QLabel(self)
        self.gxlabels["date"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.03), int(self.winsize_v * 0.08), int(self.winsize_h * 0.5),
                         int(self.winsize_v * 0.08)))
        icon_date = QtGui.QPixmap(os.path.join(current_path, "ImgGui/date_main.png"))
        icon_date = icon_date.scaled(int(self.winsize_h * 0.5), int(self.winsize_v * 0.08), Qt.KeepAspectRatio,
                                     Qt.SmoothTransformation)
        self.gxlabels["date"].setPixmap(icon_date)

        self.currdate = QtWidgets.QLabel(self)
        self.currdate.setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.05), int(self.winsize_v * 0.07), int(self.winsize_h * 0.15),
                         int(self.winsize_v * 0.1)))
        self.currdate.setStyleSheet("color:white;font:bold;font-size:14px; Sans Serif")

        # Hide
        self.gxlabels["hide"] = QtWidgets.QLabel(self)
        self.gxlabels["hide"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.9), int(self.winsize_v * 0.04), int(self.winsize_h * 0.04),
                         int(self.winsize_v * 0.04)))
        icon_hide = QtGui.QPixmap(os.path.join(current_path, "ImgGui/hide_main.png"))
        icon_hide = icon_hide.scaled(int(self.winsize_h * 0.04), int(self.winsize_v * 0.04), Qt.KeepAspectRatio,
                                     Qt.SmoothTransformation)
        self.gxlabels["hide"].setPixmap(icon_hide)

        # Close
        self.gxlabels["close"] = QtWidgets.QLabel(self)
        self.gxlabels["close"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.95), int(self.winsize_v * 0.04), int(self.winsize_h * 0.04),
                         int(self.winsize_v * 0.04)))
        icon_close = QtGui.QPixmap(os.path.join(current_path, "ImgGui/close_main.png"))
        icon_close = icon_close.scaled(int(self.winsize_h * 0.04), int(self.winsize_v * 0.04), Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)
        self.gxlabels["close"].setPixmap(icon_close)

        # Minimenu
        self.gxlabels["mini_re"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_re"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.1), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_register = QtGui.QPixmap(os.path.join(current_path, "ImgGui/save_re.png"))
        icon_register = icon_register.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08), Qt.KeepAspectRatio,
                                             Qt.SmoothTransformation)
        self.gxlabels["mini_re"].setPixmap(icon_register)

        self.gxlabels["mini_sta"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_sta"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.25), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_statis = QtGui.QPixmap(os.path.join(current_path, "ImgGui/stati_menu.png"))
        icon_statis = icon_statis.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08), Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        self.gxlabels["mini_sta"].setPixmap(icon_statis)

        self.gxlabels["mini_rem"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_rem"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.4), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_r = QtGui.QPixmap(os.path.join(current_path, "ImgGui/rem_menu.png"))
        icon_r = icon_r.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08), Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        self.gxlabels["mini_rem"].setPixmap(icon_r)

        self.gxlabels["mini_avatar"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_avatar"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.55), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_avatar = QtGui.QPixmap(os.path.join(current_path, "ImgGui/avatar_menu.png"))
        icon_avatar = icon_avatar.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08), Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        self.gxlabels["mini_avatar"].setPixmap(icon_avatar)

        self.gxlabels["mini_db"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_db"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.7), int(self.winsize_v * 0.88), int(self.winsize_h * 0.08),
                         int(self.winsize_v * 0.08)))
        icon_db = QtGui.QPixmap(os.path.join(current_path, "ImgGui/db_menu.png"))
        icon_db = icon_db.scaled(int(self.winsize_h * 0.08), int(self.winsize_v * 0.08), Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)
        self.gxlabels["mini_db"].setPixmap(icon_db)

        self.gxlabels["mini_sun"] = QtWidgets.QLabel(self)
        self.gxlabels["mini_sun"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.875), int(self.winsize_v * 0.905), int(self.winsize_h * 0.04),
                         int(self.winsize_v * 0.04)))
        icon_sun = QtGui.QPixmap(os.path.join(current_path, "ImgGui/sun_main.png"))
        icon_sun = icon_sun.scaled(int(self.winsize_h * 0.04), int(self.winsize_v * 0.04), Qt.KeepAspectRatio,
                                   Qt.SmoothTransformation)
        self.gxlabels["mini_sun"].setPixmap(icon_sun)

        # Start Calibration labels
        self.gxlabels["calibration"] = QtWidgets.QLabel(self)
        self.gxlabels["calibration"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.4), int(self.winsize_v * 0.5), int(self.winsize_h * 0.2),
                         int(self.winsize_v * 0.1)))
        icon_db = QtGui.QPixmap(os.path.join(current_path, "ImgGui/calibration.png"))
        icon_db = icon_db.scaled(int(self.winsize_h * 0.2), int(self.winsize_v * 0.1), Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)
        self.gxlabels["calibration"].setPixmap(icon_db)

        self.gxlabels["calibration_white"] = QtWidgets.QLabel(self)
        self.gxlabels["calibration_white"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.7), int(self.winsize_v * 0.7), int(self.winsize_h * 0.15),
                         int(self.winsize_v * 0.05)))
        icon_db = QtGui.QPixmap(os.path.join(current_path, "ImgGui/calibration_charg.png"))
        icon_db = icon_db.scaled(int(self.winsize_h * 0.15), int(self.winsize_v * 0.05), Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)
        self.gxlabels["calibration_white"].setPixmap(icon_db)

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

        self.controlButtons["mini_avatar"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['mini_avatar'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['mini_avatar'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.545), int(self.winsize_v * 0.88), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.085)))

        self.controlButtons["calibration"] = QtWidgets.QCommandLinkButton(self)
        self.controlButtons['calibration'].setIconSize(QtCore.QSize(0, 0))
        self.controlButtons['calibration'].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.4), int(self.winsize_v * 0.5), int(self.winsize_h * 0.2),
                         int(self.winsize_v * 0.1)))

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.set_time)
        self.timer.start(1000)

        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.9), int(self.winsize_v * 0.9), int(self.winsize_h * 0.055),
                         int(self.winsize_v * 0.055)))
        self.lcd.display(strftime("%H" + ":" + "%M" + ":" + "%S"))
        self.lcd.setDigitCount(8)

        # self.set_signals()
        self.closeButton(self.confirm_close)
        self.hideButton()
        self.set_date()
        self.set_time()

    def set_signals(self):
        self.onCalibration_end.connect(self.calibration_charging)

    def closeButton(self, f):
        self.controlButtons["close"].clicked.connect(f)

    def statisticsButton(self, f):
        self.controlButtons["mini_sta"].clicked.connect(f)

    def reminiscenceButton(self, f):
        self.controlButtons["mini_rem"].clicked.connect(f)

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

    def calibration(self, f):
        print('calib defined')
        self.controlButtons["calibration"].clicked.connect(f)

    def calibration_charging(self, current_path):
        print('cambio a azul')
        self.gxlabels["calibration_blue"] = QtWidgets.QLabel(self)
        self.gxlabels["calibration_blue"].setGeometry(
            QtCore.QRect(int(self.winsize_h * 0.7), int(self.winsize_v * 0.7), int(self.winsize_h * 0.15),
                         int(self.winsize_v * 0.05)))
        icon_db = QtGui.QPixmap(os.path.join(current_path, "ImgGui/calibration_blue.png"))
        icon_db = icon_db.scaled(int(self.winsize_h * 0.15), int(self.winsize_v * 0.05), Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)
        self.gxlabels["calibration_blue"].setPixmap(icon_db)
        self.gxlabels["calibration_blue"].show()


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     GUI = CalibrationWindow()
#     GUI.show()
#     sys.exit(app.exec_())


# if __name__ == '__main__':
#     main()
