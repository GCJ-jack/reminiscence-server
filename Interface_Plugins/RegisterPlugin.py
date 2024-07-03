import os
from urllib.request import DataHandler

from self import self

import Upper_layer.RegisterWindow as RegisterWindow
import sys


class RegisterPlugin(object):

    def __init__(self, DataHandler):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # loadinf databas manager
        self.DB = DataHandler
        # loading GUI
        self.RegisterWindow = RegisterWindow.RegisterWindow()

    def set_signals(self):
        pass

    def launchView(self):

        self.RegisterWindow.show()

    def onDataReceived(self, user):

        # user = self.RegisterWindow.get_patient_data()

        print('DATA OF THE USER', user)

        self.DB.General.register(user=user)
        # check the register status
        if self.DB.General.UserStatus['registered']:
            # emit registered signal
            self.RegisterWindow.onAlreadyRegistered.emit()

        else:
            self.RegisterWindow.onNotRegistered.emit()

        self.shutdown()

    def onEmptyData(self):

        print("Empty label")

    def shutdown(self):
        self.RegisterWindow.close()


