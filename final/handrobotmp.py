#!/usr/bin/python3
#基于mediapipe手势识别,静态手势识别，用于机器人控制
import sys
import cv2
import numpy as np
import time
import mediapipe as mp
import math
import serial
import threading
import tools
debug = True
#求二维向量角度
def vector_2d_angle(v1,v2):
    #求解二维向量的角度    
    v1_x=v1[0]
    v1_y=v1[1]
    v2_x=v2[0]
    v2_y=v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ =65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_
#获取手势向量
def hand_angle(hand_):
    #获取对应手相关向量的二维角度,根据角度确定手势    
    angle_list = []
    #---------------------------- thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    #---------------------------- index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    #---------------------------- middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    #---------------------------- ring 无名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    #---------------------------- pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list
#向量定义手势识别无法实现4 7 9
def h_gesture(angle_list):
    # 二维约束的方法定义手势
    # fist five gun love one six three thumbup yeah
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = None
    if 65535. not in angle_list:
        if (angle_list[0]>thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = 0#"fist"
        elif (angle_list[0]<thr_angle_s) and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle_s):
            gesture_str = 5#"five"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = 8#"gun"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
            gesture_str = 9#"love"
        elif (angle_list[0]>5)  and (angle_list[1]<thr_angle_s) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = 1#"one"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]<thr_angle_s):
            gesture_str = 6#"six"
        elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]>thr_angle):
            gesture_str = 3#"three"
        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = 1#"thumbUp"
        elif (angle_list[0]>thr_angle_thumb)  and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = 2#"two"
    return gesture_str
def handpos(hand_):
    #确定手中心坐标
    x=[]
    y=[]
    for h in hand_:
        x.append(h[0])
        y.append(h[1])
    hx=sum(x)/len(x)
    hy=sum(y)/len(y)
    return (hx,hy)

#/////////////////////////////////////////////////////////////
#获取摄像头，控制Robotarm移动
#摄像头默认分辨率640x480,处理图像时会相应的缩小图像进行处理，这样可以加快运行速度
#缩小时保持比例4：3,且缩小后的分辨率应该是整数
c = 80
width, height = c*4, c*3

orgFrame = None
ret = False

try:
    cap = cv2.VideoCapture(0)
except:
    print('Unable to detect camera! \n')
       
def getimage():
    global orgFrame
    global ret    
    global cap
    global width, height
    while True:        
        try:
            if cap.isOpened():
                ret, orgFrame = cap.read()                    
            else:
                time.sleep(0.01)
        except:               
            cap = cv2.VideoCapture(0)
            print('Restart Camera Successful!')        

th1 = threading.Thread(target = getimage)
th1.setDaemon(True)  #随着主线程退出而退出
th1.start()
#发送手势命令到下位机，执行动作组
#action1*2基座左右转动，action2*3点头，action3*3转动手腕，action4*2向前伸手抓取,action5把上述动作都做一遍
get_hand_num = False
action_finish = True
def runAction():
    global get_hand_num, action_finish
    global num_mean,pos_mean
    
    while True:
        if get_hand_num:
            get_hand_num = False
            action_finish = False #每个动作规定时间完成，期间为False
            print(pos_mean)
            if num_mean == 1:  #手指个数为1时执行1号动作action1()
                ser.write(b'1')
                print("1")                
                num_mean = 0
                time.sleep(2)           
            elif num_mean == 2:
                ser.write(b'2')
                print("2")
                num_mean = 0
                time.sleep(2)                          
            elif num_mean == 3:
                ser.write(b'3')
                print("3")
                num_mean = 0                
                time.sleep(2)                
            elif num_mean == 0:
                ser.write(b'4')
                print("4")
                num_mean = 0                
                time.sleep(2)                 
            elif num_mean == 5:
                ser.write(b'5')
                print("5")
                num_mean = 0
                time.sleep(3)               
            else:                
                time.sleep(0.5)
            
        else:
           time.sleep(0.1)
        action_finish = True   
#启动动作在运行线程
th2 = threading.Thread(target=runAction)
th2.setDaemon(True)
th2.start()

#主程序///////////////////////////////////////////////////////
try:
    ser = serial.Serial("COM4", 9600)
    print(ser)
    if ser.isOpen():
        print("COM open success")   
except:
    print("COM open failed")
num = []
pos=[]
num_mean = 0
pos_mean=(0,0)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75)

while True:               
    if orgFrame is not None and ret:        
        orgframe = cv2.resize(orgFrame, (width,height), interpolation = cv2.INTER_CUBIC)
        frame = orgframe[:,0:int(orgframe.shape[1]*3/5)]  # 剪切右侧矩形区域orgframe
        h, w, c = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame= cv2.flip(frame,1)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_local = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x*100
                    y = hand_landmarks.landmark[i].y*100
                    hand_local.append((x,y))
                if hand_local:
                    angle_list = hand_angle(hand_local)
                    gesture_str = h_gesture(angle_list)
                    hxy=handpos(hand_local)
                    #print(hxy)
                    cv2.putText(frame,str(gesture_str),(0,100),0,1.3,(0,0,255),3)
                cv2.imshow('MediaPipe Hands', frame)
                pos.append(hxy)
                num.append(gesture_str)
        
        #至少10次得到手指个数，取平均或最多数
        if len(num) >= 10:            
            #num_mean = int(round(np.mean(num)))
            num_mean= max(num,key=num.count)   #取数量最多的
            pos_mean=tuple(np.array(pos).mean(axis=0))
            num = []
            pos=[]
            #如果前一个动作还没有完成，本次手势无效
            if action_finish:
                get_hand_num = True            
                 
        key=cv2.waitKey(200)
        if(key==27):
            break
        else:
            time.sleep(0.01)
    else:      
        time.sleep(0.01)
     
cap.release()
cv2.destroyAllWindows()
