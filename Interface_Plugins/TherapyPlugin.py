#!/usr/bin/python2.7
import threading
import os, sys
sys.path.append(r'C:\Users\natha\Escritorio\reminiscenceSAR-script\Interface_Plugins\speech-into-text')
from Interface_Plugins.speech_into_text.main import main
ab_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Interface_Plugins'))
sys.path.append(ab_path)
from PyQt5 import QtCore, QtGui
import time
import json

# import Middle_layer.SpeechRobot as Robot
# import Middle_layer.robotController as Robot
import Lower_layer.Lowerlevel_Main as Lowerlevel
import Lower_layer.User_Understanding.Visual_Engagement as VE
import Upper_layer.ReminiscenceWindow as ReminiscenceWindow
import sys
from collections import Counter
import numpy as np
import datetime
import socket

class TherapyPlugin(object):

    def __init__(self, settings='Images/Photo_1.jpeg', DataHandler=None, path=None, client_socket=None):

        # Loading interface settings
        self.settings = settings
        # print('Setting from TherapyPlugin', self.settings)

        self.path = path
        print('Path from therapy', self.path)

        self.useRobot = True  

        # Load database manager

        self.DB = DataHandler

        self.client_socket = client_socket

        self.date = datetime.datetime.now()

        self.validation = None

        self.onSart_count = 0

        # Loading libraries for TherapyPlugin

        self.Lowerlevel = Lowerlevel.LowerLevel(Datahandler=self.DB)
        # self.Robot = Robot.Robot(db=self.DB)
        # self.Avatar = Avatar.Avatar_Speech(Datahandler=self.DB)
        self.VE = VE.Visual_EngagementTracker(DataHandler=self.DB, window="Therapy")
        self.ReminiscenceWindow = ReminiscenceWindow.ReminiscenceWindow(settings=self.settings)

        # Launching sensor and robot
        self.launch_sensors()
        self.launch_robot()
        self.launch_camera()
        

    def launch_view(self):
        # self.image_processing()
        self.send_to_server("upload_image")
        self.ReminiscenceWindow.show()
        self.set_signals()

    def set_signals(self):
        # self.image_validation()

        # Opening the data from calibration process

        calibration_values = self.calibration_data()
        self.VE.set_thresholds(ey=calibration_values[0], hp=calibration_values[1])

        # Avatar Interaction signals
        # self.ReminiscenceWindow.playButton(self.Robot.welcome_sentence)
        self.ReminiscenceWindow.playButton(self.SensorCaptureThread.start)
        self.ReminiscenceWindow.playButton(self.CameraCaptureThread.start)
        # self.ReminiscenceWindow.playButton(self.AvatarGraphicsThread.start)
        self.ReminiscenceWindow.closeButton(self.onShutdown)

        # Internal Signals
        self.ReminiscenceWindow.onUpload(self.image_validation)
        self.ReminiscenceWindow.onPhoto.connect(self.comment_photos)

        # self.ReminiscenceWindow.onUpload(self.onStart)

        # Lower level signals
        self.ReminiscenceWindow.set_pathPhoto1(lambda: self.onStart(n=1))
        self.ReminiscenceWindow.set_pathPhoto2(lambda: self.onStart(n=2))
        # self.ReminiscenceWindow.set_pathPhoto3(self.onStart)
        # self.ReminiscenceWindow.set_pathPhoto4(self.onStart)

    def user_data(self, user):
        self.user = user

    def calibration_data(self):
        f = open(self.path + "/" + "db" + "/" + "general" + "/" + str(self.user["id"]) + "/" + str(self.date.year) + "-" + str(self.date.month) + "-" + str(self.date.day) + "/" + "Calibration.csv")
        lines = f.readlines()
        lines = lines[1].split(";")
        self.eg_thresh = lines[0]
        self.hp_thresh = lines[1]

        return [self.eg_thresh, self.hp_thresh]

    def image_processing(self):
        # Available photos in Lower layer level
        self.photos = os.listdir(self.settings)
        # Photos name in the directory
        photo1 = self.photos[0]
        photo2 = self.photos[1]
        # Setting paths in the Lower level
        self.Lowerlevel.set_path({'path1': self.settings + '/' + photo1, 'path2': self.settings + '/' + photo2})
        self.Lowerlevel.set_modules(work=True, sound=True)
        self.Lowerlevel.launch_wsmodule()

    def launch_sensors(self):
        self.SensorCaptureThread = SensorCaptureThread(interface=self)

    def launch_robot(self):
        # Launching the robot thread
        self.RobotCaptureThread = RobotCaptureThread(interface=self,client_socket=self.client_socket)

    def launch_camera(self):
        # Launching the camera thread
        self.VE.start()
        self.CameraCaptureThread = CameraCaptureThread(interface=self)

    def image_validation(self):
        print('image_validation')

        self.validation = self.ReminiscenceWindow.validate_images()

        print('Validatiooon', self.validation)

        if self.validation == False:
            self.comment_photos()
            # self.ReminiscenceWindow.onPhoto.emit()
        # time.sleep(10)

    def comment_photos(self):
        print('Robot commenting')
        self.send_to_server("image_validation", self.validation)

    def VE_data(self):
        VE_data = self.VE.get_calibration()

    def onStart(self, n):
        img_id = n
        print('Image ID from therapy', img_id)
        self.onSart_count += 1

        # Launching Robot's SR module
        self.send_to_server("launch_RobotSR")
        # self.Robot.launch_RobotSR()

        # Setting lower layer modules
        self.ReminiscenceWindow.set_recognImage(img_id)

        self.send_to_server("commenting_photos",self.onSart_count)

        m = self.Lowerlevel.get_data(img_id)


        print('Data from Lower Level Images', m)

        self.DB.General.SM.loadSensor(recog_obj=m)

        time.sleep(5)

        # self.Robot.conversation_topics(m)
        self.send_to_server("conversation_topics",m)
        # self.Robot.coversation_beginning()
        self.send_to_server("conversation_beginning")
        self.RobotCaptureThread.start()

    def update_RobotGraphics(self):
        # data = self.Lowerlevel.update_sounddata()
        # self.ReminiscenceWindow.update_sound()
        print("1111111111111")

    def send_to_server(self, message, data=None):
        try:
            payload = message if data is None else f"{message}:{json.dumps(data)}"
            payload += '\n'
            print(f"Sending to server: {payload}")
            self.client_socket.sendall(payload.encode('utf-8'))
        except ConnectionAbortedError as e:
            print(f"Connection aborted error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


    def second_Photo(self):
        self.ReminiscenceWindow.onPhoto2.emit()
        self.RobotCaptureThread.c = 0
        self.RobotCaptureThread.n = None
        self.RobotCaptureThread.shutdown()
        # self.Robot.set_topicStatus()
        self.send_to_server("set_topicStatus")

    def onShutdown(self):
        print('Here shutdown')

        time.sleep(5)
        # self.Robot.r.pause()
        self.RobotCaptureThread.shutdown()
        self.SensorCaptureThread.shutdown()

        path = self.path + "/" + "db" + "/" + "general" + '/' + self.user['id'] + '/' + str(self.date.year) + "-" + str(self.date.month) + "-" + str(self.date.day)
        self.Lowerlevel.write_audio(path)
        self.Lowerlevel.close_sensors()

        self.ReminiscenceWindow.close()

        time.sleep(1)

        sys.exit()


class RobotCaptureThread(QtCore.QThread):
    def __init__(self, parent=None, sample=1, interface=None, client_socket=None):
        super(RobotCaptureThread, self).__init__()
        self.Ts = sample
        self.ON = True
        self.client_socket = client_socket
        self.interface = interface
        self.c = 0
        self.n = None
        
        self.num_threads = 0
        self.cont_yesd = 0
        self.cont_nod = 0
        self.client_socket = client_socket

    def run(self):
        self.ON = True
        chat_log = [{
            "role": "system",
            "content": "You are a reminiscence therapy assistant in a social robot. Your task is to generate feedback based on the text provided. Do not ask any further questions or seek additional input! Don't ask any further questions or seek additional input! Only feedback no question! Keep your responses as brief and concise as possible."
        }]
        self.num_threads = self.num_threads + 1
        while self.ON:
            if self.c == 0:
                self.n = self.send_to_server("sr_beginning")
                print(f"Received from server: {self.n}")
                print(f"Is self.n equal to 'yes'? {'Yes' if self.n == 'yes' else 'No'}")
                if self.n == "yes":
                    print("Detected 'yes', sending 'yes_beginning' to server")
                    self.send_message("nihao")
                    self.send_message("yes_beginning")
                    self.c = 1
                elif self.n == 'no':
                    self.c = 2
                elif self.n == "yes_dcatch":
                    self.send_message("set_wordRecognized")
                    if self.cont_yesd > 1:
                        self.send_message("bad_catching","yes")
                    self.cont_yesd += 1
                    self.c = 0
                elif self.n == "no_dcatch":
                    self.send_message("set_wordRecognized")
                    if self.cont_nod > 1:
                        self.send_message("bad_catching","no")
                    self.cont_nod += 1
                    self.c = 0
                elif self.n not in ["yes", "no"]:
                    self.send_message("no_understanding")
                    self.send_message("set_wordRecognized")
                    self.c = 0

            if self.c == 1:
                if self.n == 'yes':
                    d = self.interface.Lowerlevel.update_sounddata()
                    d[1]+= 2
                    self.send_message("set_Dialog", d)
                    main(self.client_socket, chat_log)
                    topic = self.send_to_server("topic_Status\n")
                    print('Topic flag', topic)
                    if topic == "End":
                        if self.num_threads == 1:
                            self.n = None
                            self.c = 0
                            self.send_message("set_wordRecognized")
                            self.send_message("second_Photo")
                            self.interface.second_Photo()
                        elif self.num_threads == 2:
                            self.send_message("end_phrase")
                            time.sleep(5)
                            self.interface.onShutdown()
                    time.sleep(self.Ts)

            if self.c == 2:
                self.send_message("no_beginning")
                self.ON = False
                time.sleep(1)


    def shutdown(self):
        print('shutdown')
        self.ON = False


    def send_to_server(self, message, data=None):
        try:
            payload = message if data is None else f"{message}:{json.dumps(data)}"
            payload += '\n'  # 添加换行符
            print(f"Sending to server: {payload}")
            self.client_socket.sendall(payload.encode('utf-8'))
            response = self.client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")
            return response.decode('utf-8')
        except ConnectionAbortedError as e:
            print(f"Connection aborted error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

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

class SensorCaptureThread(QtCore.QThread):
    def __init__(self, parent=None, sample=0.5, interface=None):
        super(SensorCaptureThread, self).__init__()
        self.on = False
        self.interface = interface

    def run(self):
        self.interface.Lowerlevel.launch_sensors()

    def shutdown(self):
        self.on = False


class CameraCaptureThread(QtCore.QThread):
    def __init__(self, parent=None, sample=0.01, interface=None):
        super(CameraCaptureThread, self).__init__()
        self.on = False
        self.interface = interface

    def run(self):
        self.interface.VE.launch_thread()

    def shutdown(self):
        self.on = False


'''
def main():
    app = QtGui.QApplication(sys.argv)
    rem = TherapyPlugin()
    rem.launch_view()
    sys.exit(app.exec_())

A = main()
'''
