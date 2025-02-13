#!/usr/bin/python2.7
import sys
import time
import functools
import threading
from .resources import P_SpeechRecog as p_sr
from .resources import P_SoundDetect as p_sd
from .resources import dialogs as Dialogs
import logging
import operator


class Robot(object):

    def __init__(self, settings={'IpRobot': "10.34.59.28",
                                 'port': 9559,
                                 'name': 'Aba',
                                 'MotivationTime': 5,
                                 'BorgTime': 3,
                                 'useMemory': False
                                 },
                 db=None,
                 controller=None,
                 ):

        # loading settings
        self.settings = settings
        # loading event handler
        self.DB = db
        # loading resources as dialogs
        self.dialogs = Dialogs.Dialogs()

        self.word_recognized = None

        self.who_recognized = None

        self.cc = 0
        self.flag = 2
        self.y = 0
        self.cont = 1

        self.cont1 = 0

        self.who = 0

        self.last_value = False

        self.onVoice = False

        self.change = 0

        self.person_topic = 0

        self.sound_data = []

        self.flag_topic = "Who"

        self.voice_act = 0

        self.voice_deac = 0

        self.flag_0 = False

        self.prob_kitchen = 0

        self.prob_dinner = 0

        self.prob_street = 0

        self.prob_book = 0

        self.prob_indoor = 0

        self.first = 0

        self.answer = None

        self.me_flag = False

        self.launch_robot()

    def launch_robot(self):

        # load dialogs
        self.dialogs.load_dialogs()
        print('Creating session from Robot Model Source')
        self.session = qi.Session()
        self.connect_session()

        # launching robot services
        self.get_services()
        # self.getBehaviors()
        # launching face tracking service for the robot
        self.face_tracking()

    def connect_session(self):

        print(self.settings['IpRobot'])

        print("tcp://" + self.settings['IpRobot'] + ":" + str(self.settings['port']))

        self.robotIp = self.settings['IpRobot']
        self.port = str(self.settings['port'])

        try:
            self.session.connect("tcp://" + self.robotIp + ":" + str(self.port))

        except RuntimeError:

            print("Can't connect to Naoqi at ip")

    def get_services(self):

        # Get the service ALMemory
        self.memory = self.session.service("ALMemory")
        self.subscriber = self.memory.subscriber("WordRecognized")
        # Get the service TexttoSpeech
        self.tts = self.session.service("ALTextToSpeech")
        # Get the robot's preprogrammed dialogues durind Autonomus Life

        self.autonomus = self.session.service("ALAutonomousLife")
        # print('AL dialogs', self.AlDialog.getLoadedTopics("English"))
        self.blinking = self.session.service("ALAutonomousBlinking")

        # Get the service SpeechRecognition
        self.asr = self.session.service("ALSpeechRecognition")
        # Get the service Motion
        self.motion = self.session.service("ALMotion")
        # Get the service Tracking
        self.tracker = self.session.service("ALTracker")
        # Get the service Animated Speech
        self.animated = self.session.service("ALAnimatedSpeech")
        self.animatedconfig = {"bodyLanguageMode": "contextual"}
        # Get service Behaviors
        self.behaviors = self.session.service("ALBehaviorManager")
        self.autonomuslife_off()  # Turning off
        self.blinking_behaviour()
        # Loading Pepper SpeechRecognizer
        self.r = p_sr.SpeechRecognizer()
        self.r.start()
        # self.r.launch_thread()
        # Loading Pepper SoundDetector
        self.d = p_sd.Sound_Detector()

    def launch_RobotSR(self):

        self.r.launch_thread()

    def no_calibration(self):

        self.animated.say("Something wrong happpened with the calibration")

    def calibration_face(self):

        s = self.dialogs.calibrationFace()
        self.animated.say(s, self.animatedconfig)
        time.sleep(0.1)

    def calibration_tablet(self):

        s = self.dialogs.calibrationTablet()
        self.animated.say(s, self.animatedconfig)
        time.sleep(0.1)

    def getBehaviors(self):

        # print(\1)

        names = self.behaviors.getRunningBehaviors()
        print("Running Behaviors")

        if len(names) > 0:

            if (self.behaviors.isBehaviorRunning(names[0])):
                self.behaviors.stopBehavior(names[0])
                time.sleep(0.1)
            else:
                print('Behaviors already stopped')

        else:
            print('Not running behaviors')

        names_default = self.behaviors.getDefaultBehaviors()
        # print(\1)
        # print(\1)

        names_bha = self.behaviors.getInstalledBehaviors()

    # print(\1)
    # print(\1)

    def autonomuslife_off(self):

        self.autoState = self.autonomus.getState()
        if self.autoState != "disabled":
            self.autonomus.setState("disabled")

        self.motion.wakeUp()
        self.motion.setBreathConfig([["Bpm", 6], ["Amplitude", 0.9]])
        self.motion.setBreathEnabled("Arms", True)

    def blinking_behaviour(self):

        self.blinking.setEnabled(True)

    def face_tracking(self):

        targetName = "Face"
        faceWidth = 0.1
        self.tracker.registerTarget(targetName, faceWidth)
        self.tracker.track(targetName)

    # To stop face tracking
    # self.tracker.stopTracker()
    # self.tracker.unregisterAllTargets()

    def welcome_sentence(self):

        s = self.dialogs.start_welcome_sentence()
        self.animated.say(s, self.animatedconfig)
        time.sleep(0.1)

        s = self.dialogs.welcome_sentence2
        self.animated.say(s, self.animatedconfig)
        time.sleep(0.1)

        s = self.dialogs.welcome_sentence3
        self.animated.say(s, self.animatedconfig)
        time.sleep(0.1)

    def image_validation(self, m):

        if m == True:
            self.DB.General.SM.loadEvent(t="AvatarTalking", c="ImageValidation", v="False-start")
            s = self.dialogs.image_validationbad
            self.animated.say(s)
            time.sleep(0.1)
            s = self.dialogs.image_validationbad1
            self.animated.say(s)
            self.DB.General.SM.loadEvent(t="AvatarTalking", c="ImageValidation", v="False-end")


        else:
            self.DB.General.SM.loadEvent(t="AvatarTalking", c="ImageValidation", v="True-start")
            s = self.dialogs.image_validationgreat
            self.animated.say(s)
            time.sleep(3)
            s = self.dialogs.image_validationgreat1
            self.animated.say(s)
            time.sleep(0.1)
            self.DB.General.SM.loadEvent(t="AvatarTalking", c="ImageValidation", v="True-end")
            s = self.dialogs.choose_photo
            self.animated.say(s)
        # self.DB.General.SM.loadEvent(t = "AvatarTalking", c = "ImageSelection", v ="True")

    def set_petrecognized(self, num_dog, num_cat):

        print('dog', num_dog)
        print('cat', num_cat)

        if ((num_dog > 0) and (num_cat > 0)):

            s = self.dialogs.get_petWho()
            s = s.replace('XX', str(num_dog))
            s = s.replace('SS', str(num_cat))
            self.animated.say(s)

            time.sleep(0.5)

        elif num_dog == 1 and num_cat == 0:

            s = self.dialogs.get_dogWho()
            self.animated.say(s)


        elif num_dog > 1 and num_cat == 0:
            s = self.dialogs.dog_whos
            self.animated.say(s)

        elif num_dog == 0 and num_cat == 1:

            s = self.dialogs.cat_who
            self.animated.say(s)

        elif num_dog == 0 and num_cat > 1:

            s = self.dialogs.cat_whos
            self.animated.say(s)

    def questions_pet(self, num_dog, num_cat, cont):

        if ((num_dog > 0) and (num_cat > 0)):

            if cont == 2:
                s = self.dialogs.petQ1
                self.animated.say(s)
                time.sleep(0.5)

            if cont == 3:
                s = self.dialogs.petQ1
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 4:

                s = self.dialogs.petQ2
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 6:

                s = self.dialogs.petQ3
                self.animated.say(s)
                time.sleep(0.5)


            elif cont == 5:
                s = self.dialogs.petQ4
                self.animated.say(s)
                time.sleep(0.5)
                self.whoVal.remove('dog')
                self.whoVal.remove('cat')




        elif num_dog == 1 and num_cat == 0:

            if cont == 2:
                s = self.dialogs.dogQ1
                self.animated.say(s)
                time.sleep(0.5)

            if cont == 3:

                s = self.dialogs.dogQ2
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 4:

                s = self.dialogs.dogQ3
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 5:

                s = self.dialogs.dogQ4
                self.animated.say(s)
                time.sleep(0.5)
                self.whoVal.remove('dog')




        elif num_dog > 1 and num_cat == 0:

            if cont == 2:
                s = self.dialogs.petQ1
                self.animated.say(s)
                time.sleep(0.5)

            if cont == 3:

                s = self.dialogs.dogsQ1
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 4:

                s = self.dialogs.dogsQ2
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 6:

                s = self.dialogs.dogsQ3
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 5:
                s = self.dialogs.dogsQ4
                self.animated.say(s)
                time.sleep(0.5)
                self.whoVal.remove('dog')




        elif num_dog == 0 and num_cat == 1:

            if cont == 2:
                s = self.dialogs.catQ1
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 3:

                s = self.dialogs.catQ2
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 4:

                s = self.dialogs.catQ3
                self.animated.say(s)
                time.sleep(0.5)


            elif cont == 5:
                s = self.dialogs.catQ4
                self.animated.say(s)
                time.sleep(0.5)
                self.whoVal.remove('cat')



        elif num_dog == 0 and num_cat > 1:

            if cont == 2:

                s = self.dialogs.catsQ1
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 3:

                s = self.dialogs.catQ2
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 4:

                s = self.dialogs.catsQ3
                self.animated.say(s)
                time.sleep(0.5)

            elif cont == 5:
                s = self.dialogs.catsQ4
                self.animated.say(s)
                time.sleep(0.5)
                self.whoVal.remove('cat')

    def set_personrecognized(self, num, main):

        if num == 1:

            s = self.dialogs.get_person_sentence()
            s = s.replace('XX', str(num))
            self.animated.say(s)

            time.sleep(0.5)
            s = self.dialogs.get_whoquestion()
            self.animated.say(s)

        else:

            if main < num:

                if main == 1:

                    s = self.dialogs.get_person_sentence()
                    s = s.replace('XX', str(main))
                    self.animated.say(s)

                    time.sleep(0.5)
                    s = self.dialogs.get_whoquestion()
                    self.animated.say(s)

                else:
                    s = self.dialogs.get_mainpeople()
                    self.animated.say(s)
                    time.sleep(0.5)
                    s = self.dialogs.get_whoquestions()
                    self.animated.say(s)

            if main == num:
                s = self.dialogs.get_numpersons_sentence()
                s = s.replace('XX', str(num))
                self.animated.say(s)

                time.sleep(0.5)

                s = self.dialogs.get_whoquestions()
                self.animated.say(s)

    def commenting_photos(self, n):

        print('Commenting the photos')

        if n == 1:

            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Commenting_photos- start")
            s = self.dialogs.commenting_photo
            self.animated.say(s)
            time.sleep(0.1)

            s = self.dialogs.analizing_photo
            self.animated.say(s)
            time.sleep(0.1)
            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Commenting_photos- end")

        elif n > 1:

            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Commenting_2ndphoto- start")

            # self.animated.say("This second photo also looks good. Let's talk!")

            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Commenting_2ndphoto- end")

    def coversation_beginning(self):

        # print('In coversation_beginning')
        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Yes_Starting - start")
        self.animated.say("Please say yes if you want to continue, if you don't please say no")
        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Yes_Starting - end")

    def conversation_topics(self, m):

        # print(m)
        # Who topic
        self.who = m['Who']

        # print('Who', self.who)
        # print('Len Who', len(self.who))

        self.whoVal = [word for word, occurrences in self.who.items() if occurrences > 0]
        print('WhoVal', self.whoVal)

        # Where topic

        self.kitchen = m['Kitchen']
        self.dinnerPlace = m['Dinner_Place']
        self.street = m['Street']
        self.indoorSpace = m['Indoor_space']
        self.where = {'Kitchen': self.kitchen, 'Dinner_Place': self.dinnerPlace, 'Street': self.street,
                      'Indoor_Space': self.indoorSpace}
        self.whereVal = [word for word, occurrences in self.where.items() if occurrences > 0]
        # calculating the maximun value in the dictionary
        self.whereMax = max(self.where.iteritems(), key=operator.itemgetter(1))[0]

        # print(self.where)
        # print(self.whereVal)

        # When topic
        self.birthday = m['Birthday']
        self.whenVal = [word for word, occurrences in self.birthday.items() if occurrences > 0]

        # Other topic
        self.weather = m['Weather']
        self.sports = m['Sports']
        self.book = m['Book']

        self.otherTopics_weather = [word for word, occurrences in self.weather.items() if occurrences > 0]
        self.otherTopics_sports = [word for word, occurrences in self.sports.items() if occurrences > 0]
        self.otherTopics_book = [word for word, occurrences in self.book.items() if occurrences > 0]

    def no_understanding(self):

        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="No_understanding - start")
        self.animated.say('Im sorry I dont understand, can you say it in a different way?')
        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="No_understanding - end")

    def sr_beginning(self):

        # print('Speech Recognizer beginning')
        # Speech recognition implementation
        while (self.word_recognized == None):
            self.word_recognized = self.r.getData()

        print('WordRecognized', self.word_recognized)
        return (self.word_recognized)

    def sr_yes(self):

        while (self.who_recognized == None):
            self.who_recognized = self.r.getData()

        return (self.who_recognized)

    def bad_catching(self, word):

        if word == 'yes':
            s = self.dialogs.yes_nocatch()
            self.animated.say(s)

        if word == 'no':
            s = self.dialogs.no_nocatch()
            self.animated.say(s)

    def set_wordRecognized(self):

        print('Settings')

        self.word_recognized = None
        self.r.setData()

    def no_beginning(self):

        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="No_beginning - start")

        s = self.dialogs.no_begin()
        print(s)
        self.animated.say(s)
        time.sleep(0.1)
        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="No_beginning - end")

    def yes_beginning(self):
        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Yes_beginning - start")
        s = self.dialogs.yes_bsentence()
        print(s)
        self.animated.say(s)
        time.sleep(0.3)
        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Yes_beginning - end")

    def second_Photo(self):

        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Second_Photo - start")

        self.animated.say('Was interesting talk about this photo, how about if you chose the other one ?')

        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Second_Photo - end")

    def set_Dialog(self, data):

        # print('-----------Not Talkiiiiiiing--------')
        self.onVoice = False
        self.y = self.y + 1

        # [change, voice_act, voice_deac] = self.test(data)

        active = data[0]

        self.flag = data[1]
        print('flag', self.flag)
        print('Topic flag', self.flag_topic)
        print('CONTADOR.......', self.cont)
        print('y', self.y)

        if self.y == 1:

            if (len(self.whoVal) > 0):

                if ("persons" in self.whoVal):

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog",
                                                 v="Persons recognized - Initialization - start")

                    self.set_personrecognized(self.who['persons'], self.who['Person_main'])
                    time.sleep(1)

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog",
                                                 v="Persons recognized - Initialization - end")


                elif ("dog" in self.whoVal) or ("cat" in self.whoVal):

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog",
                                                 v="Pets recognized - Initialization - start")

                    self.set_petrecognized(self.who['dog'], self.who['cat'])
                    self.questions_pet(self.who['dog'], self.who['cat'], self.cont)
                    time.sleep(1)

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog",
                                                 v="Pets recognized - Initialization - end")

            elif (len(self.whereVal) > 0 and self.flag_topic == 'Where'):

                # print( 'Aqui en la primera vez')

                self.first = True

                if (self.whereMax == "Kitchen"):

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Kitchen - Initialization - start")

                    s = self.dialogs.kitchenq1
                    self.animated.say(s)
                    time.sleep(1)

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Kitchen - Initialization - end")

                elif (self.whereMax == "Dinner_Place"):

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog",
                                                 v="Dinner_Place - Initialization - start")

                    s = self.dialogs.dinner_placeq1
                    self.animated.say(s)
                    time.sleep(1)

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Dinner_Place - Initialization - end")

                elif (self.whereMax == "Street"):

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Street - Initialization - start")
                    s = self.dialogs.streetq1
                    self.animated.say(s)
                    time.sleep(1)
                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Street - Initialization - end")


                elif (self.whereMax == "Indoor_Space"):

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog",
                                                 v="Indoor_Space - Initialization - start")
                    s = self.dialogs.indoorq1
                    self.animated.say(s)
                    time.sleep(1)
                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Indoor_Space - Initialization - end")

                else:

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog",
                                                 v="Not recognized - Initialization - start")

                    s = self.dialogs.whereNo
                    self.animated.say(s)
                    time.sleep(1)
                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog",
                                                 v="Not recognized - Initialization - end")

                    self.cont = 2

        # else:

        # self.DB.General.SM.loadEvent(t = "AvatarTalking", c = "Dialog", v ="When")
        # s = self.dialogs.get_When1()
        # print(s)
        # self.animated.say(s)

        if self.flag == 2 and self.y > 1:

            self.cont = self.cont + 1
            self.cont1 = 0

            # print('CONTADOR.......', self.cont)

            if self.flag_topic == "Who":

                if (len(self.whoVal) > 0):

                    if ("persons" in self.whoVal):

                        # Questions regarding WHO

                        if self.cont == 2:

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Persons-q2 - start")

                            if self.who['Person_main'] == 1:
                                s = self.dialogs.get_connectiveWho1()
                                self.animated.say(s)
                                self.answer = self.sr_yes()
                                print(self.answer)
                                if self.answer == 'yes':
                                    print('aqui')
                                    self.me_flag = True
                                    s = self.dialogs.get_connectiveMe1()
                                    self.animated.say(s)

                                else:
                                    s = self.dialogs.get_connectiveWho2()
                                    self.animated.say(s)


                            else:
                                s = self.dialogs.get_connectiveWhos1()
                                self.animated.say(s)
                            # print('plural1')

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Persons-q2 - end")

                            time.sleep(1)


                        elif self.cont == 3:

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Persons-q3 - start")

                            if self.who['Person_main'] == 1:

                                if not self.me_flag:
                                    print('Im here')
                                    s = self.dialogs.get_connectiveWho3()
                                    self.animated.say(s)
                                    self.whoVal.remove('persons')
                                    self.whoVal.remove('Person_main')
                                    # self.flag_topic = "When"
                                    self.cont = 1
                                elif self.me_flag:
                                    print('I enter here in Me')
                                    s = self.dialogs.get_connectiveMe2()
                                    self.animated.say(s)
                                    self.whoVal.remove('persons')
                                    self.whoVal.remove('Person_main')
                                    # self.flag_topic = "When"
                                    self.cont = 1

                            else:
                                s = self.dialogs.get_connectiveWhos2()
                                self.animated.say(s)

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Persons-q3 - end")

                            time.sleep(1)



                        elif self.cont == 4:

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Persons-q4 -start")

                            if self.who['Person_main'] == 1:

                                if not self.me_flag:
                                    s = self.dialogs.get_connectiveWho3()
                                    self.animated.say(s)
                                    self.whoVal.remove('persons')
                                    self.whoVal.remove('Person_main')
                                    self.cont = 1

                            else:
                                s = self.dialogs.get_connectiveWhos3()
                                self.animated.say(s)
                                self.whoVal.remove('persons')
                                self.whoVal.remove('Person_main')
                                self.cont = 1

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Persons-q4 - end")

                            time.sleep(1)


                    elif ("dog" in self.whoVal) or ("cat" in self.whoVal):

                        if self.cont == 2:
                            # print('Dog 1')

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Animals-q1 - start")

                            self.set_petrecognized(self.who['dog'], self.who['cat'])
                            self.questions_pet(self.who['dog'], self.who['cat'], self.cont)

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Animals-q1 - end")

                            time.sleep(1)

                        if self.cont == 3:
                            # print('Dog 2')

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Animals-q2 - start")

                            self.questions_pet(self.who['dog'], self.who['cat'], self.cont)

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Animals-q2 - end")

                            time.sleep(1)

                        if self.cont == 4:
                            # print('Dog 3')

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Animals-q3 - start")

                            self.questions_pet(self.who['dog'], self.who['cat'], self.cont)

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Animals-q3 - end")

                            time.sleep(1)

                        if self.cont == 5:
                            # print('Dog 4')

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Animals-q4 - start")

                            self.questions_pet(self.who['dog'], self.who['cat'], self.cont)

                            self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Animals-q4 - end")

                            time.sleep(1)

                            self.cont = 1

                            self.flag_topic = 'When'

                        # self.y = 0



                else:

                    # Cannot see people in the photos, let me ask another question

                    self.flag_topic = "When"
                # self.cont = 1
                # self.y = 0

            if self.flag_topic == "When":

                if self.cont == 2:
                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="When-q1 - start")

                    if (len(self.whenVal) > 0):
                        s = self.dialogs.get_Birthday()
                        self.animated.say()
                        self.whenVal.remove('Birthday')
                        time.sleep(1)


                    else:
                        s = self.dialogs.get_When1()
                        self.animated.say(s)
                        # time.sleep(4)
                        time.sleep(1)

                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="When-q1 - end")

                if self.cont == 3:
                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="When-q2 - start")
                    s = self.dialogs.get_When2()
                    self.animated.say(s)
                    self.flag_topic = "Where"
                    self.cont = 1
                    self.y = 0
                    # time.sleep(4)
                    time.sleep(1)
                    self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="When-q2 - end")

            if self.flag_topic == "Where":

                # time.sleep(2)

                if (len(self.whereVal) > 0):

                    if self.cont == 2:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q2 - start")

                        s = self.dialogs.get_whereq()
                        self.animated.say(s)

                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q2 - end")
                        time.sleep(1)

                    if self.cont == 3:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q3 - start")
                        s = self.dialogs.get_where1q()
                        self.animated.say(s)
                        time.sleep(1)
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q3 - end")
                        self.flag_topic = "Other"
                        self.cont = 1


                else:

                    if self.cont == 2:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q1n - start")

                        s = 'Oh, I cannot tell where the photo was taken. Where was it?'
                        print(s)
                        self.animated.say(s)
                        time.sleep(1)
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q1n - end")

                    if self.cont == 3:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q2n - start")
                        s = self.dialogs.get_whereq()
                        self.animated.say(s)
                        time.sleep(1)
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q1n - end")

                    if self.cont == 4:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q3 - start")
                        s = self.dialogs.get_where1q()
                        self.animated.say(s)
                        time.sleep(2)
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Where-q3 - end")
                        self.flag_topic = "Other"
                        self.cont = 1

            if self.flag_topic == "Other":

                if (len(self.otherTopics_book) > 0):

                    if self.cont == 2:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_bookq1 - start")

                        # print('Book 1 Aqui')

                        s = self.dialogs.otherBook
                        self.animated.say(s)
                        time.sleep(1)

                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_bookq1 - end")

                    if self.cont == 3:
                        # print('Book 2 Aqui')
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_bookq2 - start")
                        s = self.dialogs.otherBook1
                        self.animated.say(s)
                        time.sleep(1)
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_bookq2 - end")
                        self.otherTopics_book.remove('book')
                        self.cont = 0

                if (len(self.otherTopics_sports) > 0):

                    if self.cont == 2:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_sportq1 - start")

                        s = self.dialogs.otherSport
                        self.animated.say(s)
                        time.sleep(1)
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_sportq1 - end")

                    if self.cont == 3:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_sportq2 - start")
                        s = self.dialogs.otherSport1
                        self.animated.say(s)
                        time.sleep(1)
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_sportq2 - end")
                        self.otherTopics_book.remove('sports')
                        self.cont = 0

                elif (len(self.otherTopics_book) == len(self.otherTopics_sports) == 0):

                    if self.cont == 2:
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_topicfinal - start")
                        s = 'One last question. Can you talk about other things about this photo?'
                        print(s)
                        self.animated.say(s)
                        time.sleep(1)
                        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Other_topicfinal - end")

                    if self.cont == 3:
                        s = "Ahhh I see. That's fine !"
                        print(s)
                        self.animated.say(s)
                        time.sleep(1)
                        self.flag_topic = "End"
                        self.cont = 1

        if self.flag == 0 and active == False:

            self.cont1 = self.cont1 + 1

            if self.cont1 == 6:
                self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Not_User_Voice - start")
                self.animated.say("Sorry, I couldn't  hear that")
                self.cont1 = 0
                time.sleep(1.1)
                self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Not_User_Voice - end")
            # self.cont = 0

    def end_phrase(self):

        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Ending_Phrase - start")

        self.tts.say("Was nice to talk with you. Hope we can talk together soon")
        time.sleep(1)
        self.tts.say("Bye!")

        self.DB.General.SM.loadEvent(t="AvatarTalking", c="Dialog", v="Ending_Phrase - end")

    def set_topicStatus(self):

        self.flag_topic = "Who"

    def topic_Status(self):

        return (self.flag_topic)

    def waiting(self, m):

        pass


'''
	
	def test(self,m):

		new_value = m


		if new_value is not None and new_value is not self.last_value:

			if new_value:

				self.change = 1

				#print('False to True')
				self.voice_act = self.voice_act + 1
				#print('Voice active:', self.voice_act)

			else:

				self.change = 2
				#print('True to False')
				self.voice_deac = self.voice_deac + 1
				#print('Voice deactive:', self.voice_deac)

		else:

			self.change = 0


		self.last_value = new_value
		#print('change from testing', self.change)

		return [self.change, self.voice_act, self.voice_deac]

'''

'''

#Testing function
def main():

	robot = Robot()
	#robot.launch_robot()
	time.sleep(6)
	robot.face_tracking()
	robot.welcome_sentence()
	robot.image_validation(m=True)
	robot.commenting_photos()
	robot.set_personrecognized(num = 5)

A = main()

'''
