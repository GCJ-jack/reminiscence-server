import os, sys

ab_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
print(ab_path)
sys.path.append(ab_path)
import threading
# import GUI elements
import Interface_Plugins.Upper_layer.MenuWindow as MenuWindow
import Interface_Plugins.Upper_layer.RegisterWindow as RegisterWindow
import Interface_Plugins.Upper_layer.ReminiscenceWindow as ReminiscenceWindow
import Interface_Plugins.Upper_layer.CalibrationWindow as CalibrationWindow
# import Plugins
import Interface_Plugins.TherapyPlugin as TherapyPlugin
import Interface_Plugins.MenuPlugin as MenuPlugin
import Interface_Plugins.RegisterPlugin as RegisterPlugin
import Interface_Plugins.CalibrationPlugin as CalibrationPlugin
import socket
import json

from PyQt5 import QtGui, QtCore, QtWidgets

import db.database as database

import time
import sys
import os

current_path = "Interface_Plugins/Upper_layer"


class MainController(object):

    def __init__(self):
        # Running file path
        self.dir = os.getcwd()
        print(self.dir)


        # Reminiscence Images Path
        self.imgDir = self.dir + '/' + 'Interface_Plugins' + '/' + 'Lower_layer' + '/' + 'Workspace_Understanding' + '/' + 'Images'
        self.database_path = self.dir + '/' + 'db' + '/' + 'general'

        db = database.database(self.database_path)

        # loading interface windows

        self.MenuWindow = MenuWindow.MenuWindow()

        self.ReminiscenceWindow = ReminiscenceWindow.ReminiscenceWindow(settings=self.imgDir)

        self.RegisterWindow = RegisterWindow.RegisterWindow()

        self.CalibrationWindow = CalibrationWindow.CalibrationWindow()

        # loading interface plugins

        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.1.179', 65432))

        self.MenuPlugin = MenuPlugin.MenuPlugin()

        self.RegisterPlugin = RegisterPlugin.RegisterPlugin(DataHandler=db,client_socket=self.client_socket)

        self.TherapyPlugin = TherapyPlugin.TherapyPlugin(settings=self.imgDir, DataHandler=db, path=ab_path, client_socket=self.client_socket)

        self.CalibrationPlugin = CalibrationPlugin.CalibrationPlugin(DataHandler=db, client_socket=self.client_socket)

        self.set_signals()

    def set_signals(self):
        self.TherapyPlugin.image_processing()

        self.MenuWindow.show()

        # Register Logics

        self.MenuWindow.registerButton(self.RegisterWindow.show)

        self.RegisterWindow.registerReminiscence(self.onLaunch_Therapy)

        self.RegisterWindow.registerReminiscence(self.MenuWindow.hideButton)

        self.RegisterWindow.registerButton(self.register_User)

        self.RegisterWindow.statisticsButton(self.CalibrationWindow.show)

        # MainMenu Logics

        self.MenuWindow.reminiscenceButton(self.onLaunch_Therapy)

        self.MenuWindow.reminiscenceButton(self.MenuWindow.hideButton)

        # Calibration Logics

        self.CalibrationWindow.reminiscenceButton(self.onLaunch_Therapy)
        self.CalibrationWindow.calibration(self.calibration)
        self.CalibrationWindow.onCalibration_end.connect(lambda: self.CalibrationWindow.calibration_charging(current_path))

    def calibration(self):
        self.CalibrationPlugin.calibration()
        self.CalibrationWindow.onCalibration_end.emit()

    def register_User(self):
        m = self.RegisterWindow.get_patient_data()

        self.RegisterPlugin.onDataReceived(m)

        self.TherapyPlugin.user_data(m)

    def onLaunch_Therapy(self):
        print('onLaunch_Therapy')

        self.TherapyPlugin.launch_view()


    # pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    menu = MainController()

    sys.exit(app.exec_())


a = main()