##cmd 관리자 모드 -> muti.py있는 곳으로 이동 아래 코멘트 복붙.
##python multi.py --shape-predictor shape_predictor_68_face_landmarks.dat

from threading import Thread
from time import sleep
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from pynput.mouse import Button, Controller
import pyautogui as m
import numpy as np
import argparse
import imutils
import time
import dlib
import os
import cv2
from tkinter import *
import tkinter

def threaded_function():
    global Keyboard_App
    Keyboard_App = tkinter.Tk()
    Keyboard_App.title("virtual Keyboard")
    Keyboard_App ['bg']='white'
    Keyboard_App.resizable(0,0)
    path = '@%s' % os.path.join(os.environ['WINDIR'], 'Cursors/arrow_r.cur').replace('\\', '/')
    Keyboard_App.config(cursor=path)
    Keyboard_App.geometry("600x650+1+1")

    def select(value):
        if value == "RESET":
            entry.delete(0,END)
        elif value == " Space ":
            entry.insert(END, ' ')
        elif value == "<-" :
            entry.delete(len(entry.get())-1,END)                    

        else:
            entry.insert(END, value)


    buttons = [
    'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', '?',' Space ', 'RESET',
    '<-']
    labell = Label (Keyboard_App, text="eye messenger", font =('arial', 30, 'bold'),
                    
                    bg ='white', fg="#000000").grid(row = 0, columnspan = 16)
    global entry
    entry = Entry(Keyboard_App, width=40,  font =('arial', 14, 'bold'))
    entry.grid(row = 1, columnspan = 40)

    varRow = 3
    varColumn = 0

    for button in buttons:
        command = lambda x=button: select(x)
        tkinter.Button(Keyboard_App, text = button, width =5, bg="pink", fg="#000000",
                    activebackground="#ffffff", activeforeground="#000990", relief = 'raised'
                       ,padx=20, pady=20, bd=5, font = ('arial', 12, 'bold'),
                       command = command).grid(row = varRow, column = varColumn)


        varColumn+=1
        if varColumn > 4 and varRow == 3:
            varColumn   = 0
            varRow+=1
        if varColumn   >4 and varRow ==4:
            varColumn   = 0
            varRow+=1
        if varColumn   >4 and varRow ==5:
            varColumn   = 0
            varRow+=1
        if varColumn   >4 and varRow ==6:
            varColumn   = 0
            varRow+=1
        if varColumn   >4 and varRow ==7:
            varColumn   = 0
            varRow+=1
    global mouse

    def event():
        mouse = Controller()
        time.sleep(3)

        mouse.position = (74, 100)
        Keyboard_App.update()
        time.sleep(2)
            

        mouse.position = (174, 100)
        Keyboard_App.update()
        time.sleep(2)
           
             
        mouse.position = (274, 100)
        Keyboard_App.update()
        time.sleep(2)
            
              
    Keyboard_App.mainloop()





def threaded_function2():
    m.FAILSAFE = False
    #taking size of screen
    (scrx,scry)=m.size()

    mLocOld = np.array([0,0])
    mouseLoc = np.array([0,0])
    DampingFactor = 15
    def calculateView(x,y):
        xvMax, yvMax = m.size()
        xvMin, yvMin = 0, 0
        xwMax, xwMin = 370, 270
        ywMax, ywMin = 290, 200
        sx = (xvMax - 0) // (xwMax - xwMin)
        sy = (yvMax - 0) // (ywMax - ywMin)
        xv = xvMin + (x - xwMin) * sx
        yv = yvMin + (y - ywMin) * sy
        return xv,yv
    def eye_aspect_ratio(eye):
       # compute the euclidean distances between the two sets of
       # vertical eye landmarks (x, y)-coordinates
       A = dist.euclidean(eye[1], eye[5])
       B = dist.euclidean(eye[2], eye[4])

       # compute the euclidean distance between the horizontal
       # eye landmark (x, y)-coordinates
       C = dist.euclidean(eye[0], eye[3])

       # compute the eye aspect ratio
       ear = (A + B) / (2.0 * C)

       # return the eye aspect ratio
       return ear
     
    # construct the argument parse and parse the arguments
    PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
    EYE_AR_THRESH = .15
    EYE_AR_CONSEC_FRAMES = 7
    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)


    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]

    # start the video stream thread
    print("[INFO] camera sensor warming up...")
    ##vs = FileVideoStream(args["video"]).start()
    fileStream = True
    ###여기 아랫줄 주석 제거함
    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    fileStream = False
    time.sleep(1.0)

    # loop over frames from the video stream
    while True:
       # if this is a file video stream, then we need to check if
       # there any more frames left in the buffer to process
       if fileStream and not vs.more():
          break

       # grab the frame from the threaded video file stream, resize
       # it, and convert it to grayscale
       # channels)
       frame = vs.read()
       frame = imutils.resize(frame, width=450)
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

       # detect faces in the grayscale frame
       rects = detector(gray, 0)

       # loop over the face detections
       for rect in rects:
          # determine the facial landmarks for the face region, then
          # convert the facial landmark (x, y)-coordinates to a NumPy
          # array
          shape = predictor(gray, rect)
          shape = face_utils.shape_to_np(shape)

          # extract the left and right eye coordinates, then use the
          # coordinates to compute the eye aspect ratio for both eyes
          global rightEAR
          leftEye = shape[lStart:lEnd]
          rightEye = shape[rStart:rEnd]
          nose = shape[nStart:nEnd]
          leftEAR = eye_aspect_ratio(leftEye)
          rightEAR = eye_aspect_ratio(rightEye)
          

          # average the eye aspect ratio together for both eyes
          ear = (leftEAR + rightEAR) / 2.0
          xv, yv = nose[0]
        
          xw = np.int(xv)
          yw = np.int(yv)
          print(type(xv))
          xv,yv = calculateView(xw,yw)
          # compute the convex hull for the left and right eye, then
          # visualize each of the eyes
          leftEyeHull = cv2.convexHull(leftEye)
          rightEyeHull = cv2.convexHull(rightEye)
          cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
          cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            #cv2.drawContours(frame, [noseHull], -1, (0, 255, 0), 1)
          if rightEAR < .15:
    ##          mouse.click(Button.left,1 )
             m.click(clicks = 1, button = 'left', pause = 1 )
                
    ##        if leftEAR < .15:
    ##            m.click(mouseLoc[0],mouseLoc[1],clicks = 1, button = 'right', pause = 0)
             mLocOld = mouseLoc

          # check to see if the eye aspect ratio is below the blink
          # threshold, and if so, increment the blink frame counter
          if ear < EYE_AR_THRESH:
             COUNTER += 1

          # otherwise, the eye aspect ratio is not below the blink
          # threshold
          else:
             # if the eyes were closed for a sufficient number of
             # then increment the total number of blinks
             if COUNTER >= EYE_AR_CONSEC_FRAMES:
                TOTAL += 1

             # reset the eye frame counter
             COUNTER = 0

          # draw the total number of blinks on the frame along with
          # the computed eye aspect ratio for the frame
          cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
          cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

       cv2.imshow("Frame", frame)
       key = cv2.waitKey(1) & 0xFF
     
        # if the `q` or 'esc' key was pressed, break from the loop
       if key == ord("q"):
           break
       elif key == 27:
           break
     
    cv2.destroyAllWindows()



if __name__ == "__main__":
    thread1 = Thread(target=threaded_function)
    thread2 = Thread(target=threaded_function2)

    thread1.start()
    thread2.start()
 
    thread1.join()
    thread2.join()
  
    print ("thread finishied .. exiting")



