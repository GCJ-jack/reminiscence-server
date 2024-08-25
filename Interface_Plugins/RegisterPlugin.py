import os
from urllib.request import DataHandler

import Interface_Plugins.Upper_layer.RegisterWindow as RegisterWindow
import sys
import json


class RegisterPlugin(object):

    def __init__(self, DataHandler,client_socket=None):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # loadinf databas manager
        self.DB = DataHandler
        # loading GUI
        self.RegisterWindow = RegisterWindow.RegisterWindow()

        self.client_socket = client_socket

        self.send_message("introduction")


    def set_signals(self):
        pass

    def launchView(self):

        self.RegisterWindow.show()

    def send_message(self, message, data=None):
        try:
            payload = message if data is None else f"{message}:{json.dumps(data)}"
            payload += '\n'
            print(f"Sending to server: {payload}")
            self.client_socket.sendall(payload.encode('utf-8'))
        except ConnectionAbortedError as e:
            print(f"Connection aborted error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def onDataReceived(self, user):

        # user = self.RegisterWindow.get_patient_data()

        print('DATA OF THE USER', user)

        self.DB.General.register(user=user)

        # package the user information and command to the server

        self.send_message("register",user)
        self.send_message("finish_register")

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



# if __name__ == '__main__':
#     main()