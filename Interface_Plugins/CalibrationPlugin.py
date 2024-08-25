#!/usr/bin/python2.7
import threading
import os
import sys
from PyQt5 import QtCore, QtWidgets
ab_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Interface_Plugins'))
sys.path.append(ab_path)
from statistics import mean
# import Middle_layer.robotController as Robot
import Upper_layer.CalibrationWindow as CalibrationWindow
import Lower_layer.User_Understanding.Visual_Engagement as VE
import time
import json


class CalibrationPlugin(object):

    def __init__(self, DataHandler = None, client_socket=None):

        # load inf from the database manager

        self.dir = os.getcwd()
        self.database_path = self.dir + '/' + 'db' + '/' + 'general'
        self.DB = DataHandler

        self.client_socket = client_socket


        #loading GUI
        self.CalibrationWindow = CalibrationWindow.CalibrationWindow()

        # self.launchView()
    
        #loading Robot
        # self.Robot = Robot.Robot(db = self.DB)

        #loading VE module for calibration
        self.VE = VE.Visual_EngagementTracker(DataHandler = self.DB)
        #Setting go_on to true
        self.VE.start()
        self.CameraCaptureThread = CameraCaptureThread(interface = self)


        #Initialization calibration data
        self.calibration_data = 0

        self.gaze_cal_face = []
        self.headpose_cal_face = []

        self.gaze_cal_tablet = []
        self.headpose_cal_tablet = []



        self.data_calibrated = None



        self.average_gaze = 0
        self.average_headpose = 0
        


        
    def calibration(self):
        print('In calibration')

        self.send_to_server("start_calibration_face")

        self.CameraCaptureThread.start()
        time.sleep(2)

        for x in range(100):
            self.calibration_data = self.VE.get_calibration()
            print('data', self.calibration_data)
            self.gaze_cal_face.append(self.calibration_data[0])
            self.headpose_cal_face.append(self.calibration_data[1])

            if x == (50):
                print('Calibration Tablet')
                self.send_to_server("start_calibration_tablet")
                self.gaze_cal_tablet.append(self.calibration_data[0])
                self.headpose_cal_tablet.append(self.calibration_data[1])

            time.sleep(0.1)


        self.data_calibrated_face = {'gaze': self.gaze_cal_face, 'head_pose': self.headpose_cal_face}
        self.data_calibrated_tablet = {'gaze': self.gaze_cal_tablet, 'head_pose': self.headpose_cal_tablet}

        self.VE.pause()
        self.send_to_server("finish_calibration")
        self.CameraCaptureThread.shutdown()
        self.CalibrationWindow.onCalibration_end.emit()

        print('Tablet', self.data_calibrated_tablet)

        self.get_data()


    def get_data(self):


        #Getting Data from the face
        m = self.data_face()
        self.average_gaze = mean(m['gaze'])
        self.average_headpose = mean(m['head_pose'])

        t = self.data_tablet()
        self.average_gaze_t = mean(t['gaze'])
        self.average_headpose_t = mean(t['head_pose'])



        if self.average_gaze != 0 or self.average_headpose !=0 or self.average_gaze_t !=0 or self.average_headpose_t !=0:
            print(str(self.average_gaze)+","+str(self.average_headpose)+","+str(self.average_gaze_t)+","+ str(self.average_headpose_t))
            self.DB.General.SM.loadCalibration(ag = self.average_gaze, hp = self.average_headpose, ag_t = self.average_gaze_t, hp_t = self.average_headpose_t)


        else:
            print('No data Calibration')
            # self.Robot.no_calibration()
            self.send_to_server("no_calibration")
            self.VE.start()
            self.calibration()


    def data_tablet(self):

        return(self.data_calibrated_tablet)

    def data_face(self):

        return(self.data_calibrated_face)


    def shutdown(self):

        self.CalibrationWindow.close()

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


class CameraCaptureThread(QtCore.QThread):

    def __init__(self, parent = None, sample = 0.01, interface = None):
        super(CameraCaptureThread, self).__init__()
        self.on = False
        self.interface = interface

    def run(self):


        self.interface.VE.launch_thread()

    def shutdown(self):

        self.on = False

