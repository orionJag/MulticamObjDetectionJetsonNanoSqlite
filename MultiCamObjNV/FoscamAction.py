# Uses multiple FOSCAM FI9821P-v3 & pretrained model for object Detection
# This script provides PTZ action & takes picture & stores  



#Import statements 
import nanocamera as nano
from libpyfoscam import FoscamCamera
from time import sleep
from datetime import datetime, date


# function for snap a picture
def camTakePict(camNam, c_item, camObj, i_indx):
    if c_item == 'potted plant' or c_item == 'chair' or c_item == 'person' or  c_item == 'suitcase' :

        rc, imgCam = camObj.snap_picture_2()
        cFile = 'Images/' + camNam +'_' + 'AssetNm_' + c_item + str(i_indx)+ '_' + str(datetime.now()) + '.jpeg'

        if camObj is None and imgCam is None:
                print('Check Camera: ', camNam)

        else:          
                try:
                        fp = open(cFile, 'wb') 
                        fp.write(imgCam)
                        fp.close()
                except IOError:
                        print('Write failed')
        sleep(0.25)



# function for  Foscam movement (a set of left side, followed by right side to complete a cycle)
def moveFosCam(i, camObj):
    if i <=30:

        camObj.ptz_move_left()        
        sleep(0.25)
        camObj.ptz_stop_run()

    else: 

        camObj.ptz_move_right()
        sleep(0.25)
        camObj.ptz_stop_run()
