# #Object detection and person detection with
# #OpenCV and Deep Neural Networks

# import cv2
# import numpy as np
# import threading
# import time
# import os
# #path = os.path.abspath(os.path.join(os.path.dirname(__file__)))



# class Object_Detection(object):

#     def __init__(self, path = 'None'):

#         self.photoPath = path

#         self.path_other = os.path.abspath(os.curdir)
        
#         self.graph = self.path_other + '/Interface_Plugins/Lower_layer/Workspace_Understanding/models/frozen_inference_graph.pb'
#         self.config = self.path_other + '/Interface_Plugins/Lower_layer/Workspace_Understanding/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt.txt'
#         self.framework = 'TensorFlow'

#         self.detected_class = []

#         self.probabilities =[]

#         self.b_area = []

#         self.detected_class_sp = []

#         #path = os.path.abspath(__file__)
        

#         #loadinf COCO class names
#         print('Here path', path)

#         with open( self.path_other + '\Interface_Plugins\Lower_layer\Workspace_Understanding\models\object_detection_classes_coco.txt','r') as f:
#             self.class_names = f.read().split('\n')

#         # self.class_names = os.path.join(self.path_other, 'Interface_Plugins', 'Lower_layer', 'Workspace_Understanding', 'models', 'object_detection_classes_coco.txt')

#         self.COLORS = np.random.uniform(0, 255, size=(len(self.class_names), 3))

#     def loading_model(self):

#         # load the DNN model
#         model = cv2.dnn.readNet(model = self.graph, config = self.config, framework = self.framework)
#         # read the image from disk
#         self.image = cv2.imread(self.photoPath)
#         self.image_height, self.image_width, _ = self.image.shape

#         #print('size Photo 1', str(self.image_height) + " " + str(self.image_width))
#         #Creatinf a blob from image
#         blob = cv2.dnn.blobFromImage(image = self.image, size = (300,300), mean = (104,117,123),
#                                      swapRB = True)
#         #Create blob from image
#         model.setInput(blob)
#         #forwards pass through the model
#         self.output = model.forward()

#     def detection(self, n):

#         num = n
#         cont = 0

#         for detection in self.output[0, 0, :, :]:

#             confidence = detection[2]



#             if confidence > .4:
#                 class_id = detection[1]
#                 class_name = self.class_names[int(class_id)-1]
#                 color = self.COLORS[int(class_id)]
#                 box_x = detection[3] * self.image_width
#                 box_y = detection[4] * self.image_height
#                 box_width = detection[5] * self.image_width
#                 box_height = detection[6] * self.image_height
#                 box_area = (int(box_width)-int(box_x))*(int(box_height)-int(box_y))
#                 proportion = box_area/(float(self.image_width*self.image_height))
#                 cv2.rectangle(self.image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=2)
#                 cv2.putText(self.image, class_name + str(cont)+ "  " + str(box_area) + "  " + str(proportion),  (int(box_x), int(box_y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

#                 self.detected_class.append(class_name)
#                 self.detected_class_sp.append(class_name+ str(cont))
#                 self.probabilities.append(confidence)
#                 self.b_area.append((float(box_area))/(float(self.image_width*self.image_height)))

#                 cont += 1 
#                 #print(cont)




#         #print('from Obj', self.probabilities)
        


#         self.outputImage(num)

#     def launch_thread(self):

#         self.t = threading.Thread(target = self.detection)
#         self.t.start()

#     def getData(self):

#         a = self.detected_class_sp
#         b = self.probabilities
#         c = self.b_area

#         new_dict = {i:[j, k] for i, j, k in zip(a, b, c)}


#         #print(new_dict)

#         #return(self.detected_class)

#         return(self.detected_class, new_dict)

#     def outputImage(self, n):

#         cv2.imwrite(self.path_other +'/' + 'output' + str(n) + '.jpg', self.image)


# def main():

#     Objects = Object_Detection('Images/Street1.jpg')
#     Objects.loading_model()
#     #Objects.start()
#     Objects.detection(89)
#     m = Objects.getData()
#     print(m)


# A = main()
















import cv2
import numpy as np
import os


class Object_Detection:
    def __init__(self, path='None'):
        self.photoPath = path
        self.path_other = os.path.abspath(os.curdir)
        print('Current directory:', self.path_other)

        self.graph = self.path_other + '/Interface_Plugins/Lower_layer/Workspace_Understanding/models/frozen_inference_graph.pb'
        self.config = self.path_other + '/Interface_Plugins/Lower_layer/Workspace_Understanding/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt.txt'

        self.framework = 'TensorFlow'
        self.detected_class = []
        self.probabilities = []
        self.b_area = []
        self.detected_class_sp = []

        # 确认当前文件的绝对路径
        current_file_path = os.path.abspath(__file__)
        print('Current file path:', current_file_path)

        class_names_path = os.path.join(self.path_other, 'Interface_Plugins', 'Lower_layer', 'Workspace_Understanding', 'models', 'object_detection_classes_coco.txt')
                    
                    
        print('Attempting to open:', class_names_path)
        if not os.path.exists(class_names_path):
            print(f"File not found: {class_names_path}")
        else:
            with open(class_names_path, 'r') as file:
                class_names = file.read().strip().split('\n')
            print(f"Class names loaded: {class_names}")

        # 初始化为 None，以防止未定义错误
        self.class_names = None

        # 加载 COCO 类别名称
        try:
            with open(class_names_path, 'r') as f:
                self.class_names = f.read().split('\n')
                print('Class names loaded successfully.')
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            print(class_names_path)
        except Exception as e:
            print(f"An error occurred: {e}")

        # 检查 class_names 是否成功加载
        if self.class_names:
            self.COLORS = np.random.uniform(0, 255, size=(len(self.class_names), 3))
        else:
            print("Error: class names could not be loaded.")
            self.COLORS = []

        self.image = None
        self.output = None
        self.image_height = 0
        self.image_width = 0

    def loading_model(self):
        # 加载 DNN 模型

        print(f"Model path: {self.graph}")

        try:
            model = cv2.dnn.readNet(model=self.graph, config=self.config, framework=self.framework)
            print(f"Model loaded successfully from {self.graph} and {self.config}")
        except Exception as e:
            print(f"Error loading model: {e}")
            print(self.graph)
            return

        # 从磁盘读取图像
        image_path = os.path.join(self.path_other, self.photoPath)
        print(f"Attempting to read image: {image_path}")
        self.image = cv2.imread(image_path)

        if self.image is None:
            print(f"Error: Unable to load image at {image_path}")
            return

        self.image_height, self.image_width, _ = self.image.shape
        print(f"Image loaded successfully with shape: {self.image.shape}")

        # 创建图像的 blob
        try:
            blob = cv2.dnn.blobFromImage(image=self.image, size=(300, 300), mean=(104, 117, 123), swapRB=True)
            # 设置模型输入
            model.setInput(blob)
            # 前向传递通过模型
            self.output = model.forward()
            print("Model forward pass completed successfully.")
        except Exception as e:
            print(f"Error during model forward pass: {e}")
            self.output = None

    def detection(self, n):
        if self.output is None:
            print("Error: Model output is not available. Make sure the image is loaded and model is processed "
                  "correctly.")
            return

        num = n
        cont = 0

        for detection in self.output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > .4:
                class_id = detection[1]
                class_name = self.class_names[int(class_id) - 1] if self.class_names else "Unknown"
                color = self.COLORS[int(class_id)]
                box_x = detection[3] * self.image_width
                box_y = detection[4] * self.image_height
                box_width = detection[5] * self.image_width
                box_height = detection[6] * self.image_height
                box_area = (int(box_width) - int(box_x)) * (int(box_height) - int(box_y))
                cv2.rectangle(self.image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color,
                              thickness=2)
                cv2.putText(self.image, class_name + "  " + str(box_area) + "  ", (int(box_x), int(box_y - 5)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

                self.detected_class.append(class_name)
                self.detected_class_sp.append(class_name + str(cont))
                self.probabilities.append(confidence)
                self.b_area.append((float(box_area)) / (float(self.image_width * self.image_height)))

                cont += 1

        self.outputImage(num)

    def outputImage(self, n):
        output_path = os.path.join(self.path_other, 'output' + str(n) + '.jpg')
        cv2.imwrite(output_path, self.image)
        print(f"Output image saved at {output_path}")

    def getData(self):
        a = self.detected_class_sp
        b = self.probabilities
        c = self.b_area

        new_dict = {i: [j, k] for i, j, k in zip(a, b, c)}
        print(self.detected_class_sp, new_dict)
        return self.detected_class_sp, new_dict


# def main():

#     Objects = Object_Detection('Interface_Plugins\Lower_layer\Workspace_Understanding\Images\Street1.jpg')
#     Objects.loading_model()
#     #Objects.start()
#     Objects.detection(89)
#     m = Objects.getData()
#     print(m)


# A = main()
