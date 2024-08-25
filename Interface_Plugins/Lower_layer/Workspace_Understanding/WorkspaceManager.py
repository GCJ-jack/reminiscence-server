import os
import sys
import operator

ab_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Workspace_Understanding'))
sys.path.append(ab_path)

# import Color_Detection as Color
import Object_DetectionPy27 as Object


class WorkspaceManager(object):
    def __init__(self, imgpath=None):
        # Extract Image path to pass both objects
        self.impath = imgpath['path1']
        self.impath1 = imgpath['path2']

        # Initialize Object Detection
        self.object = Object.Object_Detection(path=self.impath)
        self.object1 = Object.Object_Detection(path=self.impath1)

        self.go_On = None
        self.prob_kitchen = 0
        self.prob_dinner = 0
        self.prob_street = 0
        self.prob_book = 0
        self.prob_indoor = 0

    def launch_workspace(self):
        self.object.loading_model()
        self.object.detection(n=1)
        self.object1.loading_model()
        self.object1.detection(n=2)

    def data_extraction(self):
        self.object_data, self.properties = self.object.getData()
        self.object_data1, self.properties1 = self.object1.getData()
        self.data = {'Objects': self.object_data, 'Objects1': self.object_data1}

    def dictionary_dataCounts(self, n):
        print('n from dictionary', n)

        # Object Detection - Second Image

        # People Animals - Who topic
        persons = sum(1 for obj in self.data['Objects'] if 'person' in obj.lower())
        dog = sum(1 for obj in self.data['Objects'] if 'dog' in obj.lower())
        cat = sum(1 for obj in self.data['Objects'] if 'cat' in obj.lower())
        bird = sum(1 for obj in self.data['Objects'] if 'bird' in obj.lower())

        # Kitchen - Where Topic
        wine_glass = sum(1 for obj in self.data['Objects'] if 'wine glass' in obj.lower())
        fork = sum(1 for obj in self.data['Objects'] if 'fork' in obj.lower())
        spoon = sum(1 for obj in self.data['Objects'] if 'spoon' in obj.lower())
        knife = sum(1 for obj in self.data['Objects'] if 'knife' in obj.lower())
        plate = sum(1 for obj in self.data['Objects'] if 'plate' in obj.lower())
        cup = sum(1 for obj in self.data['Objects'] if 'cup' in obj.lower())
        oven = sum(1 for obj in self.data['Objects'] if 'oven' in obj.lower())

        # Dinner Place - Where Topic
        dining_table = sum(1 for obj in self.data['Objects'] if 'dining table' in obj.lower())

        # Street - Where Topic
        car = sum(1 for obj in self.data['Objects'] if 'car' in obj.lower())
        bus = sum(1 for obj in self.data['Objects'] if 'bus' in obj.lower())
        motorcycle = sum(1 for obj in self.data['Objects'] if 'motorcycle' in obj.lower())
        traffic_light = sum(1 for obj in self.data['Objects'] if 'traffic light' in obj.lower())
        stop_sign = sum(1 for obj in self.data['Objects'] if 'stop sign' in obj.lower())
        street_sign = sum(1 for obj in self.data['Objects'] if 'street sign' in obj.lower())

        # Birthday - When Topic
        cake = sum(1 for obj in self.data['Objects'] if 'cake' in obj.lower())

        # Library - Where Topic
        book = sum(1 for obj in self.data['Objects'] if 'book' in obj.lower())

        # Indoor Objects - Where Topic
        door = sum(1 for obj in self.data['Objects'] if 'door' in obj.lower())
        remote = sum(1 for obj in self.data['Objects'] if 'remote' in obj.lower())
        tv = sum(1 for obj in self.data['Objects'] if 'tv' in obj.lower())
        bed = sum(1 for obj in self.data['Objects'] if 'bed' in obj.lower())

        # Weather - Other Topics
        umbrella = sum(1 for obj in self.data['Objects'] if 'umbrella' in obj.lower())

        # Sports - Other Topics
        snowboards = sum(1 for obj in self.data['Objects'] if 'snowboard' in obj.lower())
        baseball_bat = sum(1 for obj in self.data['Objects'] if 'baseball bat' in obj.lower())
        skateboard = sum(1 for obj in self.data['Objects'] if 'skateboard' in obj.lower())
        tennis = sum(1 for obj in self.data['Objects'] if 'tennis racket' in obj.lower())

        self.image_context = {'Who': {'persons': persons, 'cat': cat, 'dog': dog, 'bird': bird},
                              'Kitchen': {'wine_glass': wine_glass, 'fork': fork, 'spoon': spoon, 'knife': knife,
                                          'plate': plate, 'cup': cup, 'oven': oven},
                              'Dinner_Place': {'dining_table': dining_table},
                              'Street': {'car': car, 'bus': bus, 'motorcycle': motorcycle,
                                         'traffic_light': traffic_light, 'stop_sign': stop_sign,
                                         'street_sign': street_sign},
                              'Birthday': {'cake': cake},
                              'Book': {'book': book},
                              'Indoor_space': {'door': door, 'remote': remote, 'tv': tv, 'bed': bed},
                              'Weather': {'umbrella': umbrella},
                              'Sports': {'snowboard': snowboards, 'baseball_bat': baseball_bat,
                                         'skateboard': skateboard, 'tennis': tennis}
                              }

        # Object Detection - Second Image

        # People Animals - Who topic
        # persons1 = self.data['Objects1'].count('person')
        persons1 = sum(1 for obj in self.data['Objects1'] if 'person' in obj.lower())
        # dog1 = self.data['Objects1'].count('dog')
        dog1 = sum(1 for obj in self.data['Objects1'] if 'dog' in obj.lower())
        cat1 = sum(1 for obj in self.data['Objects1'] if 'cat' in obj.lower())
        bird1 = sum(1 for obj in self.data['Objects1'] if 'bird' in obj.lower())

        # Kitchen - Where Topic
        wine_glass1 = sum(1 for obj in self.data['Objects1'] if 'wine glass' in obj.lower())
        fork1 = sum(1 for obj in self.data['Objects1'] if 'fork' in obj.lower())
        spoon1 = sum(1 for obj in self.data['Objects1'] if 'spoon' in obj.lower())
        knife1 = sum(1 for obj in self.data['Objects1'] if 'knife' in obj.lower())
        plate1 = sum(1 for obj in self.data['Objects1'] if 'plate' in obj.lower())
        cup1 = sum(1 for obj in self.data['Objects1'] if 'cup' in obj.lower())
        oven1 = sum(1 for obj in self.data['Objects1'] if 'oven' in obj.lower())

        # Dinner Place - Where Topic
        dining_table1 = sum(1 for obj in self.data['Objects1'] if 'dining table' in obj.lower())

        # Street - Where Topic
        car1 = sum(1 for obj in self.data['Objects1'] if 'car' in obj.lower())
        bus1 = sum(1 for obj in self.data['Objects1'] if 'bus' in obj.lower())
        motorcycle1 = sum(1 for obj in self.data['Objects1'] if 'motorcycle' in obj.lower())
        traffic_light1 = sum(1 for obj in self.data['Objects1'] if 'traffic light' in obj.lower())
        stop_sign1 = sum(1 for obj in self.data['Objects1'] if 'stop sign' in obj.lower())
        street_sign1 = sum(1 for obj in self.data['Objects1'] if 'street sign' in obj.lower())

        # Birthday - When Topic
        cake1 = sum(1 for obj in self.data['Objects1'] if 'cake' in obj.lower())

        # Library - Where Topic
        book1 = sum(1 for obj in self.data['Objects1'] if 'book' in obj.lower())

        # Indoor Objects - Where Topic
        door1 = sum(1 for obj in self.data['Objects1'] if 'door' in obj.lower())
        remote1 = sum(1 for obj in self.data['Objects1'] if 'remote' in obj.lower())
        tv1 = sum(1 for obj in self.data['Objects1'] if 'tv' in obj.lower())
        bed1 = sum(1 for obj in self.data['Objects1'] if 'bed' in obj.lower())

        # Weather - Other Topics
        umbrella1 = sum(1 for obj in self.data['Objects1'] if 'umbrella' in obj.lower())

        # Sports - Other Topics
        snowboards1 = sum(1 for obj in self.data['Objects1'] if 'snowboard' in obj.lower())
        baseball_bat1 = sum(1 for obj in self.data['Objects1'] if 'baseball bat' in obj.lower())
        skateboard1 = sum(1 for obj in self.data['Objects1'] if 'skateboard' in obj.lower())
        tennis1 = sum(1 for obj in self.data['Objects1'] if 'tennis racket' in obj.lower())
        self.image2_context = {'Who': {'persons': persons1, 'cat': cat1, 'dog': dog1, 'bird': bird1},
                               'Kitchen': {'wine_glass': wine_glass1, 'fork': fork1, 'spoon': spoon1, 'knife': knife1,
                                           'plate': plate1, 'cup': cup1, 'oven': oven1},
                               'Dinner_Place': {'dining_table': dining_table1},
                               'Street': {'car': car1, 'bus': bus1, 'motorcycle': motorcycle1,
                                          'traffic_light': traffic_light1, 'stop_sign': stop_sign1,
                                          'street_sign': street_sign1},
                               'Birthday': {'cake': cake1},
                               'Book': {'book': book1},
                               'Indoor_space': {'door': door1, 'remote': remote1, 'tv': tv1, 'bed': bed1},
                               'Weather': {'umbrella': umbrella1},
                               'Sports': {'snowboard': snowboards1, 'baseball_bat': baseball_bat1,
                                          'skateboard': skateboard1, 'tennis': tennis1}
                               }

        if n == 1:
            self.dataIm = self.image_context

        elif n == 2:
            self.dataIm = self.image2_context

    def who_abstraction(self):
        # Image 1 - Who topic
        person = [value for key, value in self.properties.items() if 'person' in key.lower()]
        person_new = [x for x in person if x[1] > 0.01]
        lperson_new = len(person_new)
        self.image_context['Who']['Person_main'] = lperson_new

        # Image 2 - Who topic
        person1 = [value for key, value in self.properties1.items() if 'person' in key.lower()]
        person_new1 = [x for x in person1 if x[1] > 0.01]
        lperson_new1 = len(person_new1)
        self.image2_context['Who']['Person_main'] = lperson_new1

    def where_abstraction(self):
        self.who_abstraction()

        # Image 1 - Where Topic
        self.kitchen = self.dataIm['Kitchen']
        self.dinnerPlace = self.dataIm['Dinner_Place']
        self.street = self.dataIm['Street']
        self.indoorSpace = self.dataIm['Indoor_space']

        self.whereVal_kitchen = [word for word, occurrences in self.kitchen.items() if occurrences > 0]
        self.whereVal_dinnerPlace = [word for word, occurrences in self.dinnerPlace.items() if occurrences > 0]
        self.whereVal_street = [word for word, occurrences in self.street.items() if occurrences > 0]
        self.whereVal_indoorSpace = [word for word, occurrences in self.indoorSpace.items() if occurrences > 0]

        if len(self.whereVal_kitchen) >= 3 and len(self.whereVal_dinnerPlace) == 0:
            if (any(i >= 2 for i in self.kitchen.values())):
                self.prob_kitchen = 0.9
            else:
                self.prob_kitchen = 0.8
        elif len(self.whereVal_kitchen) > 2 and len(self.whereVal_kitchen) < 3:
            if (any(i >= 2 for i in self.kitchen.values())):
                self.prob_kitchen = 0.7
            else:
                self.prob_kitchen = 0.5
        elif len(self.whereVal_kitchen) > 0 and len(self.whereVal_kitchen) <= 2:
            if (any(i >= 2 for i in self.kitchen.values())):
                self.prob_kitchen = 0.4
            else:
                self.prob_kitchen = 0.2

        # Identifying - dinner/eating place
        if len(self.whereVal_kitchen) >= 3 and len(self.whereVal_dinnerPlace) > 0:
            self.prob_dinner = 0.9
        if len(self.whereVal_dinnerPlace) > 0:
            self.prob_dinner = 0.5

        # Identifying - Street
        if len(self.whereVal_street) >= 4:
            if any(i >= 2 for i in self.street.values()):
                self.prob_street = 0.9
            else:
                self.prob_street = 0.8
        elif 2 < len(self.whereVal_street) < 4:
            if any(i >= 2 for i in self.street.values()):
                self.prob_street = 0.7
            else:
                self.prob_street = 0.5
        elif 0 < len(self.whereVal_street) <= 2:
            if any(i >= 2 for i in self.street.values()):
                self.prob_street = 0.4
            else:
                self.prob_street = 0.2

        # Identifying - Indoor Space
        if len(self.whereVal_indoorSpace) >= 3:
            if any(i >= 2 for i in self.indoorSpace.values()):
                self.prob_indoor = 0.9
            else:
                self.prob_indoor = 0.8
        elif 1 < len(self.whereVal_indoorSpace) < 3:
            if any(i >= 2 for i in self.indoorSpace.values()):
                self.prob_indoor = 0.7
            else:
                self.prob_indoor = 0.5
        elif 0 < len(self.whereVal_indoorSpace) <= 1:
            if any(i >= 2 for i in self.indoorSpace.values()):
                self.prob_indoor = 0.4
            else:
                self.prob_indoor = 0.2

        # Displaying probabilities
        self.dataIm['Kitchen'] = self.prob_kitchen
        self.dataIm['Dinner_Place'] = self.prob_dinner
        self.dataIm['Street'] = self.prob_street
        self.dataIm['Indoor_space'] = self.prob_indoor

        return self.dataIm

    def start(self):
        self.go_On = True

    def pause(self):
        self.go_On = False


# def main():
#     Workspace_manager = WorkspaceManager(imgpath={
#         'path1': r'Interface_Plugins\Lower_layer\Workspace_Understanding\Images\0.jpeg',
#         'path2': r'Interface_Plugins\Lower_layer\Workspace_Understanding\Images\00.jpeg'
#     })
#     Workspace_manager.launch_workspace()
#     Workspace_manager.data_extraction()
#     Workspace_manager.dictionary_dataCounts(n=1)
#     n = Workspace_manager.where_abstraction()
#     where = {'Kitchen': n['Kitchen'], 'Dinner_Place': n['Dinner_Place'], 'Street': n['Street'],
#              'Indoor_Space': n['Indoor_space']}
#     whereVal = [word for word, occurrences in where.items() if occurrences > 0]
#     print('Where Val', whereVal)
#     # calculating the maximum value in the dictionary
#     whereMax = max(where.items(), key=operator.itemgetter(1))[0]
#     print('Where Max', whereMax)

#     Workspace_manager.who_abstraction()


# if __name__ == "__main__":
#     main()
