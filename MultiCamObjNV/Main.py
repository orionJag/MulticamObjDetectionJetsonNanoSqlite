# Uses multiple FOSCAM FI9821P-v3 & pretrained model for object Detection 
# Certain objects when detected a picture is taken 
# All object that are detected are stored in SQLite Database 


# Database script 
# Database created using sqlitebrowser 
# CREATE TABLE OpnCVStats ( Msg_id VARCHAR(20), Pgm_Name VARCHAR(100), Camera_Name VARCHAR(50), Model_Name VARCHAR(100), Item_Id VARCHAR(20), Item_Desc VARCHAR(100), Item_Confidence VARCHAR(10), Item_LeftWdw VARCHAR(10), Item_TopWdw VARCHAR(10), Item_RightWdw VARCHAR(10), Item_BottmWdw VARCHAR(10), Item_WidthWdw VARCHAR(10), Item_HeightWdw VARCHAR(10), Item_AreaWdw VARCHAR(10), Item_Center VARCHAR(50), CrtTS DATETIME, rectime VARCHAR(10) , jclock VARCHAR(10) , jnvmodel VARCHAR(10) , jcpu1 VARCHAR(10) , jcpu2 VARCHAR(10) , jcpu3 VARCHAR(10) , jcpu4 VARCHAR(10) , jgpu VARCHAR(10) , jtempao VARCHAR(10) , jtempcpu VARCHAR(10) , jtempgpu VARCHAR(10) , jtemppll VARCHAR(10) , jtempiwlwifi VARCHAR(10) , jtempthermal VARCHAR(10) , jpowercur VARCHAR(10) )


#Import statements 
import cv2 
import jetson.inference
import jetson.utils 
import time
import numpy as np 
import nanocamera as nano
from libpyfoscam import FoscamCamera
from time import sleep
import sys 
from datetime import datetime, date
import sqlite3 as lite 
import FoscamAction as fcam
import JetsonStats as jStats
import PlotResults as fplt


# # Variables 
startTime = time.time()
fpsFiltered =0
msgId = 0 
runScptNm = sys.argv[0]
font = cv2.FONT_HERSHEY_SIMPLEX
i = 0 
j = 0
cycleNum = 1
lastCycleNum = 0


# # sqlite connection string 
conn = lite.connect('MultiCamDB.db')



# # pretrained models 
netMv1 = jetson.inference.detectNet('ssd-mobilenet-v1', threshold=.5) # w 50% confidence level  good 
#netMv2 = jetson.inference.detectNet('ssd-mobilenet-v2', threshold=.5) # w 50% confidence level  poor
#netI2 = jetson.inference.detectNet('ssd-inception-v2', threshold=.5) # w 50% confidence level  poor
#netCB = jetson.inference.detectNet('coco-bottle', threshold=.5) # w 50% confidence level 
#netCC = jetson.inference.detectNet('coco-chair', threshold=.5) # w 50% confidence level 
#netFA = jetson.inference.detectNet('facenet', threshold=.5) # w 50% confidence level 



# # insert into SQLite Database
def insrtSQLite(i_connSQL, i_msgId, i_pgmNam, i_camNam, i_mdlName, i_itemId, i_item, i_detectConfi, i_itemLeft, i_itemTop, i_itemRight, i_itemBottom, i_itemWidth, i_itemHeight, i_itemArea, i_itemCenter, i_transDate, i_statValue):
    sql = "INSERT INTO OpnCVStats VALUES( '" + str(i_msgId) +  "', '"  + (i_pgmNam) +  "', '"  + (i_camNam) +  "', '"  +  str(i_mdlName) +  "', '"  +  str(i_itemId)  +  "', '"  +  (i_item)  +  "',  '"  +  str(i_detectConfi)  +  "', '"  + str(i_itemLeft) +  "', '"  + str(i_itemTop) +  "', '"  + str(i_itemRight) +  "', '"  + str(i_itemBottom) +  "',  '" + str(i_itemWidth)  +  "',  '"  + str(i_itemHeight) +  "', '"  +  str(i_itemArea) +  "', '"  + str(i_itemCenter)  +  "',  '"  + str(i_transDate) + "',  '"  + i_statValue +  "')"

    with i_connSQL:
        curSQL = i_connSQL.cursor()
        curSQL.execute(sql)
        i_connSQL.commit()


# function to  retrieve detected object attributes 
def modelSet(connSQL, mId, cam, cImg, mdlName, cNet, cFrame, cWidth, cHeight, camObj, cIdx):
    detections = cNet.Detect(cFrame, cWidth, cHeight)
    jstatValue = jStats.startJsonStats() 
    

    # Loop thro for each item 
    for detectItems in detections:
        #print('Detected Items1 : ',detectItems)
        itemId      = detectItems.ClassID
        item        = cNet.GetClassDesc(itemId)
        itemTop     = int(detectItems.Top)
        itemLeft    = int(detectItems.Left)
        itemBottom  = int(detectItems.Bottom)
        itemRight   = int(detectItems.Right)
        itemWidth   = int(detectItems.Width)
        itemHeight  = int(detectItems.Height)
        itemArea    = int(detectItems.Area)
        itemCenter  = detectItems.Center
        detectConfi = round(detectItems.Confidence*100,2)
        transDate   =  datetime.now().strftime("%m/%d/%Y %H:%M:%S")

        # add inference info to the image 
        cv2.rectangle(cImg,(itemLeft, itemTop), (itemRight, itemBottom), (255,0,0),3)
        cv2.putText(cImg, (item +' conf ' + str(detectConfi)) +'%' + mdlName, (itemLeft, itemTop), font, .5, (0,0,255), 2)
        insrtSQLite(connSQL, mId, runScptNm, cam, mdlName, itemId, item, detectConfi, itemLeft, itemTop, itemRight, itemBottom, itemWidth, itemHeight,itemArea, itemCenter, transDate, jstatValue)
        fcam.camTakePict(cam, item, camObj, cIdx)


# For Foscam camera for OpenCV 
#camera_stream1 = "username1:password1@ipaddress1/videoMain"
#camera_stream2 = "username2:password2@ipaddress2/videoMain"

# Create the Camera instance
camera1 = nano.Camera(camera_type=2, source=camera_stream1, width=640, height=480, fps=30)
camera2 = nano.Camera(camera_type=2, source=camera_stream2, width=640, height=480, fps=30)


# For Foscam Camera for PTZ 
#mycam1 = FoscamCamera('ipaddress1', portnumber, 'username1', 'password1') 
#mycam2 = FoscamCamera('ipaddress2', portnumber, 'username2', 'password2') 


# Retrieve Camera name from dictonary 
camSysName = mycam1.get_dev_name()
devName = camSysName[1] 
camNam1 = devName['devName']

camSysName = mycam2.get_dev_name()
devName = camSysName[1] 
camNam2 = devName['devName']


#Set PTX speed: 0: Very slow 1: Slow 2: Normal speed 3: Fast 4: Very fast    
mycam1.set_ptz_speed(0)  
mycam2.set_ptz_speed(0)


# loop for 1 complete sequence 
while (camera1.isReady() and camera2.isReady()) and cycleNum <=1:
        try:    

                i = i+1
                j = j+1
                msgId = msgId + 1
                img1  = camera1.read()
                height1= img1.shape[0]
                width1 = img1.shape[1]

                img2  = camera2.read()
                height2= img2.shape[0]
                width2 = img2.shape[1]


                # convert image BGR2RGBA for Numpy   
                frame1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA).astype(np.float32)
                frame1 = jetson.utils.cudaFromNumpy(frame1)

                frame2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA).astype(np.float32)
                frame2 = jetson.utils.cudaFromNumpy(frame2)

                # execute for each pretrained model for camera-1 
                modelSet(conn, msgId, camNam1, img1, 'ssd-mobilenet-v1', netMv1, frame1, width1, height1, mycam1, i)
                #modelSet(conn, msgId, camNam1, img1, 'ssd-mobilenet-v2', netMv2, frame1, width1, height1, mycam1, i)
                #modelSet(conn, msgId, camNam1, img1, 'coco-chair', netCC, frame1, width1, height1, mycam1, i)
                #modelSet(conn, msgId, camNam1, img1, 'facenet',    netFA, frame1, width1, height1, mycam1, i)

                # Create window for camera-1
                cv2.putText(img1, str(round(fpsFiltered,1)) + ' fps', (0,30), font, 1, (0,0,255), 2)

                
               
                # execute for each pretrained model for camera-2
                modelSet(conn, msgId, camNam2, img2, 'ssd-mobilenet-v1', netMv1, frame2, width2, height2, mycam2, i)
                #modelSet(conn, msgId, camNam2, img2, 'ssd-mobilenet-v2', netMv2, frame2, width2, height2, mycam2, i)
                #modelSet(conn, msgId, camNam2, img2, 'coco-chair', netCC, frame2, width2, height2, mycam2, i)
                #modelSet(conn, msgId, camNam2, img2, 'facenet',    netFA, frame2, width2, height2, mycam2, i)

                # Create window for camera-2
                cv2.putText(img2, str(round(fpsFiltered,1)) + ' fps', (0,30), font, 1, (0,255,0), 2)

                # Show images                 
                cv2.imshow('FosCam1', img1)
                cv2.moveWindow('FosCam1', 0,0)
                cv2.imshow('FosCam2', img2)
                cv2.moveWindow('FosCam2', 0,550)
                lastCycleNum = cycleNum
                sleep(0.5)


                # compute FPS 
                dt = time.time() - startTime
                startTime = time.time()
                fps = 1/dt 
                fpsFiltered = 0.9*fpsFiltered + 0.1*fps # smoothing FPS

                # Move & Reset the camera view 
                if j ==10:
                        fcam.moveFosCam(i, mycam1)
                        fcam.moveFosCam(i, mycam2)
                        camera1.open()
                        camera2.open()
                        j=0

                # Starts the next cycle
                if i >=60: 
                        i=0        
                        cycleNum = cycleNum+1 
                        sleep(3)   

                # Break if the user issues keyboard interrupt 
                if cv2.waitKey(1) ==ord('q'):
                        break
        except KeyboardInterrupt:
                break        


# Release all resources 
print('# of Rounds: ', lastCycleNum)
camera1.release()
camera2.release()
cv2.destroyAllWindows()


# plot the graphs 
if cycleNum>=1:
        fplt.plot_ObjDetectCount()
        fplt.plot_ObjDetectCount_Time()


if conn:
    conn.close()
