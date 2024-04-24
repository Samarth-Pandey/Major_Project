import cv2
import numpy as np
import time
import os 
import track_hands as TH

class virtualpaint():
    gc_mode=0
    brush_thickness = 15
    eraser_thickness = 100
    image_canvas =np.zeros((720,1280,3), np.uint8)

    currentT=0
    previousT =0

    header_img = "Images"
    header_img_list = os.listdir(header_img)
    overlay_image =[]


    for i in header_img_list:
        image = cv2.imread(f'{header_img}/{i}')
        overlay_image.append(image)

    cap = None
    default_overlay= overlay_image[0]
    draw_color = (255,200,100)

    detector= TH.handDetector(detectionCon=.85)

    xp =0
    yp=0

    def __init__(self):
        virtualpaint.cap = cv2.VideoCapture(0)
        virtualpaint.cap.set(3,1280)
        virtualpaint.cap.set(4,720)
        virtualpaint.cap.set(cv2.CAP_PROP_FPS, 60)
        virtualpaint.gc_mode=1

    def start(self):
        virtualpaint.gc_mode
        while(virtualpaint.gc_mode==1):
            ret, frame = virtualpaint.cap.read()
            frame = cv2.flip(frame,1)
            frame[0:125,0:1280] = virtualpaint.default_overlay

            frame = virtualpaint.detector.findHands(frame, draw=True)
            landmark_list = virtualpaint.detector.findPosition(frame, draw =False)

            if(len(landmark_list)!=0):
                x1, y1 =(landmark_list[8][1:]) #index
                x2, y2 = landmark_list[12][1:] #middle    
            
                my_fingers = virtualpaint.detector.fingerStatus()
                #print(my_fingers)
                if (my_fingers[1]and my_fingers[2]):
                    virtualpaint.xp, virtualpaint.yp = 0,0
                    if (y1<125):
                        if(200<x1<340):
                            virtualpaint.default_overlay = virtualpaint.overlay_image[0] 
                            virtualpaint.draw_color = (255,0,0)
                        elif (340<x1<500):
                            virtualpaint.default_overlay = virtualpaint.overlay_image[1]
                            virtualpaint.draw_color = (47,225,245)
                        elif (500<x1<640):
                            virtualpaint.default_overlay = virtualpaint.overlay_image[2]
                            virtualpaint.draw_color = (197,47,245)
                        elif (640<x1<780):
                            virtualpaint.default_overlay = virtualpaint.overlay_image[3]
                            virtualpaint.draw_color = (53,245,47)
                        elif (1100<x1<1280):
                            virtualpaint.default_overlay = virtualpaint.overlay_image[4]
                            virtualpaint.draw_color = (0,0,0)

                    cv2.putText(frame, 'Color Selector Mode', (900,680), fontFace=cv2.FONT_HERSHEY_COMPLEX, color= (0,255,255), thickness=2, fontScale=1)
                    cv2.line(frame, (x1,y1), (x2,y2), color=virtualpaint.draw_color, thickness=3)

                if (my_fingers[1] and not my_fingers[2]):
                            
                    cv2.putText(frame, "Writing Mode", (900,680), fontFace= cv2.FONT_HERSHEY_COMPLEX, color= (255,255,0), thickness=2, fontScale=1)
                    cv2.circle(frame, (x1,y1),15, virtualpaint.draw_color, thickness=-1)

                    if virtualpaint.xp ==0 and virtualpaint.yp ==0:
                        virtualpaint.xp =x1 
                        virtualpaint.yp =y1
                    
                    if virtualpaint.draw_color == (0,0,0):
                        cv2.line(frame, (virtualpaint.xp,virtualpaint.yp),(x1,y1),color= virtualpaint.draw_color, thickness=virtualpaint.eraser_thickness)
                        cv2.line(virtualpaint.image_canvas, (virtualpaint.xp,virtualpaint.yp),(x1,y1),color= virtualpaint.draw_color, thickness=virtualpaint.eraser_thickness)

                    else:
                        cv2.line(frame, (virtualpaint.xp,virtualpaint.yp),(x1,y1),color= virtualpaint.draw_color, thickness=virtualpaint.brush_thickness)
                        cv2.line(virtualpaint.image_canvas, (virtualpaint.xp,virtualpaint.yp),(x1,y1),color= virtualpaint.draw_color, thickness=virtualpaint.brush_thickness)
                    
                    virtualpaint.xp , virtualpaint.yp = x1, y1

            img_gray = cv2.cvtColor(virtualpaint.image_canvas, cv2.COLOR_BGR2GRAY)
            _, imginv= cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
            imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
            frame = cv2.bitwise_and(frame, imginv)
            frame =cv2.bitwise_or(frame, virtualpaint.image_canvas)
            virtualpaint.currentT = time.time()
            fps = 1/(virtualpaint.currentT- virtualpaint.previousT)
            virtualpaint.previousT = virtualpaint.currentT

            cv2.putText(frame, 'Client FPS:' + str(int(fps)), (10,670), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
            cv2.imshow('paint', frame)
            if cv2.waitKey(5) & 0xFF == 13:
                break
        virtualpaint.cap.release()
        cv2.destroyAllWindows()

        
