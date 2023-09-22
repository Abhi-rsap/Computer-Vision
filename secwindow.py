import sys

import cv2
import mediapipe as mp
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
        a= np.array(a)
        b=np.array(b)
        c=np.array(c)

        radians = np.arctan2(c[1] - b[1] , c[0] - b[0]) - np.arctan2(a[1] - b[1] , a[0] - b[0]) 
        deg = np.abs(radians * 180.0/ np.pi)

        if deg > 180.0:
            deg = 360 -deg
        
        return deg



class Ui_MainWindow(object):

    def openWindow(self):
        from search_win import Ui_Home3

        self.window2 = QtWidgets.QMainWindow()

        self.ui = Ui_Home3()

        self.ui.setupUi(self.window2)

        self.window2.show()



    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1189, 549)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(-1, -1, 1191, 551))
        self.widget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.widget.setObjectName("widget")
        self.openout_label = QtWidgets.QLabel(self.widget)
        self.openout_label.setGeometry(QtCore.QRect(40, 40, 640, 480))
        self.openout_label.setObjectName("openout_label")
        self.workout_correction_label = QtWidgets.QLabel(self.widget)
        self.workout_correction_label.setGeometry(QtCore.QRect(730, 330, 401, 71))
        self.workout_correction_label.setObjectName("workout_correction_label")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(840, 460, 171, 51))
        self.pushButton.setStyleSheet("font: 63 18pt \"Segoe UI Variable Text Semibold\";\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:0.818, x2:1, y2:1, stop:0 rgba(206, 24, 56, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openWindow)
        self.pushButton.clicked.connect(MainWindow.close)
        #self.pushButton.clicked.connect(self.stop)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(730, 0, 431, 141))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 0, 0);\n"
"font: 63 26pt \"Segoe UI Variable Text Semibold\";\n"
"")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(820, 100, 241, 81))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 0, 0);\n"
"font: 63 26pt \"Segoe UI Variable Text Semibold\";\n"
"")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.workout_name_label = QtWidgets.QLabel(self.widget)
        self.workout_name_label.setGeometry(QtCore.QRect(780, 210, 291, 51))
        self.workout_name_label.setObjectName("workout_name_label")
        self.workout_name_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 0, 0);\n"
"font: 63 26pt \"Segoe UI Variable Text Semibold\";\n"
"")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.Worker1 = Worker1()

        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)

    def ImageUpdateSlot(self, Image):
        self.openout_label.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openout_label.setText(_translate("MainWindow", "TextLabel"))
        self.workout_correction_label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton.setText(_translate("MainWindow", "back"))
        self.label_3.setText(_translate("MainWindow", "Home Workout "))
        self.label_4.setText(_translate("MainWindow", "Monitoring "))
        
    

class Worker1(QThread, Ui_MainWindow): 


    ImageUpdate = pyqtSignal(QImage)
    
    

    def run(self):
        self.ThreadActive = True
        file1 = open("url.txt","r+") 
        url = file1.read()
        file1.truncate()
        cap = cv2.VideoCapture(url)
        counter = 0 
        file2 = open("choice.txt","r+") 
        choice = file2.read()
        choice = int(choice)
        file2.truncate()
        stage = None
        while self.ThreadActive:
            
            
            with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence=0.5) as pose:

                while cap.isOpened():
                    ret,frame = cap.read()
                    if frame is not None:
                        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                        image.flags.writeable =False;

                        results = pose.process(image)
                        image.flags.writeable =True;
                    else:
                        break
                    
                    try:
                        landmarks = results.pose_landmarks.landmark

                    

                        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x , landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y ]

                        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x , landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y ]
                        
                        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x , landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y ]
                        
                        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x , landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y ]


                        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x , landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y ]

                        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x , landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y ]

                        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x , landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y ]

                        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x , landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y ]

                        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x , landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y ]

                        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x , landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y ]

                        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x , landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y ]
                        
                        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x , landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y ]

                        left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x , landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y ]

                        right_heel =[landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x , landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y ]

                        left_foot_index = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x , landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y ]

                        right_foot_index = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x , landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y ]

                    
                            

                        if(choice == 1): #Pushup
                            left_elbow_angle =  calculate_angle(left_shoulder, left_elbow, left_wrist)
                            right_elbow_angle =  calculate_angle(right_shoulder, right_elbow, right_wrist)
                            left_hip_angle =  calculate_angle(left_shoulder, left_hip, left_knee)
                            right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
                            left_knee_angle =  calculate_angle(left_hip, left_knee, left_ankle)
                            right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                    
                            
                            if((left_knee_angle > 150   and left_hip_angle > 150) or  (right_hip_angle > 150 and  right_knee_angle > 150)):
                                if(left_elbow_angle > 170 or right_elbow_angle > 170  ):
                                    stage = "up"

                                if((left_elbow_angle < 50  or  right_elbow_angle < 50)  and (stage == "up")):
                                    stage= "down"
                                    counter+=1
                                    
                            else:
                                if(left_knee_angle < 150 or right_knee_angle < 150):
                                    print("Don't bend your knees!!!")
                                   
                                
                                elif(right_hip_angle < 150 or left_hip_angle < 150):
                                    print("Keep your hip straight!!!")
                            cv2.rectangle(image, (0,0), (225,120), (245,117,16),-1)
                            cv2.putText(image, "COUNT", (35,42), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),2,cv2.LINE_AA)
                            cv2.putText(image, str(counter), (40,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3,cv2.LINE_AA)                                
                                
                            
                        if choice == 2: #SQUATS
                            
                            left_elbow_angle =  calculate_angle(left_shoulder, left_elbow, left_wrist)
                            right_elbow_angle =  calculate_angle(right_shoulder, right_elbow, right_wrist)
                            left_hip_angle =  calculate_angle(left_shoulder, left_hip, left_knee)
                            right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
                            left_knee_angle =  calculate_angle(left_hip, left_knee, left_ankle)
                            right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                            left_heel_angle = calculate_angle(left_knee, left_heel, left_foot_index)
                            right_heel_angle = calculate_angle(right_knee, right_heel, right_foot_index)
                            

                            if(left_hip_angle > 169 or right_hip_angle > 169):
                                stage = "stand"
                            
                            else:
              
                                if(right_knee_angle < 35 or left_knee_angle < 35 ):
                                    print("Bend your knees a little more!!!")
                            
                            if((right_heel_angle > 38  ) and (right_heel_angle < 53)):
                               
                        
                                if((right_knee_angle > 35 or left_knee_angle > 35) and (right_knee_angle < 55 or left_knee_angle < 55) and stage == "stand"):
                                    stage= "squat"
                                    counter+=1
                                    
                            cv2.rectangle(image, (0,0), (225,120), (245,117,16),-1)
                            cv2.putText(image, "COUNT", (35,42), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),2,cv2.LINE_AA)
                            cv2.putText(image, str(counter), (40,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3,cv2.LINE_AA)
                                    
                                
                            
                                    
                                
                        if choice == 3: # Dumble Curls
                            left_elbow_angle =  calculate_angle(left_shoulder, left_elbow, left_wrist)
                            right_elbow_angle =  calculate_angle(right_shoulder, right_elbow, right_wrist)
                            left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
                            right_shoulder_angle= calculate_angle(right_elbow, right_shoulder, right_hip)

                            a = np.array(right_shoulder)
                            b = np.array(right_elbow)
                            slope = (a[1] - b[1]) / (a[0] - b[0])

                            
                            
                            
                            if(left_shoulder_angle < 30  or right_shoulder_angle < 30):
                            
                                if((left_elbow_angle > 110 or right_elbow_angle > 110)):
                                    stage = "down"
                                if((left_elbow_angle < 60 or right_elbow_angle < 60) and stage == "down" and right_shoulder_angle < 20):
                                    
                                            stage= "up"
                                            counter+=1
                                        
                                    
                                elif (stage == "down" and (right_elbow_angle < 60  or left_elbow_angle < 60)):
                                    print("Don't move your shoulder!!!")

                            cv2.rectangle(image, (0,0), (225,120), (245,117,16),-1)
                            cv2.putText(image, "COUNT", (35,42), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),2,cv2.LINE_AA)
                            cv2.putText(image, str(counter), (40,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3,cv2.LINE_AA)

                        if choice == 4: #Lat-pulldowns
                            left_elbow_angle =  calculate_angle(left_shoulder, left_elbow, left_wrist)
                            right_elbow_angle =  calculate_angle(right_shoulder, right_elbow, right_wrist)
                            left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
                            right_shoulder_angle= calculate_angle(right_elbow, right_shoulder, right_hip)

                         
                            if right_elbow_angle > 130:
                                stage = "up"
                            if right_elbow_angle < 86 and stage == "up":
                                
                            
                                
                            
                                    stage = "down"
                                    counter+=1
                      
                            cv2.rectangle(image, (0,0), (225,120), (245,117,16),-1)
                            cv2.putText(image, "COUNT", (35,42), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),2,cv2.LINE_AA)
                            cv2.putText(image, str(counter), (40,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3,cv2.LINE_AA)
                                    
                        if choice == 5: # Seated Cable-rows
                            left_elbow_angle =  calculate_angle(left_shoulder, left_elbow, left_wrist)
                            right_elbow_angle =  calculate_angle(right_shoulder, right_elbow, right_wrist)
                            left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
                            right_shoulder_angle= calculate_angle(right_elbow, right_shoulder, right_hip)

                
                            if right_elbow_angle > 145:
                                stage = "start"
                        
                        
                        
                            if stage == "start" and right_elbow_angle < 75:
                                stage = "end"
                                counter+=1
                           
                            cv2.rectangle(image, (0,0), (225,120), (245,117,16),-1)
                            cv2.putText(image, "COUNT", (35,42), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),2,cv2.LINE_AA)
                            cv2.putText(image, str(counter), (40,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3,cv2.LINE_AA)            
                    
                    except:
                        pass
                    mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS)
                        
                    ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
