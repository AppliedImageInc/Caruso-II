#===========================================================================#
#                                                                           #
#  Copyright (C) 2006 - 2018                                                #
#  IDS Imaging Development Systems GmbH                                     #
#  Dimbacher Str. 6-8                                                       #
#  D-74182 Obersulm, Germany                                                #
#                                                                           #
#  The information in this document is subject to change without notice     #
#  and should not be construed as a commitment by IDS Imaging Development   #
#  Systems GmbH. IDS Imaging Development Systems GmbH does not assume any   #
#  responsibility for any errors that may appear in this document.          #
#                                                                           #
#  This document, or source code, is provided solely as an example          #
#  of how to utilize IDS software libraries in a sample application.        #
#  IDS Imaging Development Systems GmbH does not assume any responsibility  #
#  for the use or reliability of any portion of this document or the        #
#  described software.                                                      #
#                                                                           #
#  General permission to copy or modify, but not for profit, is hereby      #
#  granted, provided that the above copyright notice is included and        #
#  reference made to the fact that reproduction privileges were granted     #
#  by IDS Imaging Development Systems GmbH.                                 #
#                                                                           #
#  IDS Imaging Development Systems GmbH cannot assume any responsibility    #
#  for the use or misuse of any portion of this software for other than     #
#  its intended diagnostic purpose in calibrating and testing IDS           #
#  manufactured cameras and software.                                       #
#                                                                           #
#===========================================================================#

# Developer Note: I tried to let it as simple as possible.
# Therefore there are no functions asking for the newest driver software or freeing memory beforehand, etc.
# The sole purpose of this program is to show one of the simplest ways to interact with an IDS camera via the uEye API.
# (XS cameras are not supported)
#---------------------------------------------------------------------------------------------------------------------------------------

#Libraries
from pyueye import ueye
import numpy as np
import cv2
import sys
from skimage import io, transform
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy # why import it twice???
import os
import time
import threading
#---------------------------------------------------------------------------------------------------------------------------------------

#Variables
hCam = ueye.HIDS(0)             #0: first available camera;  1-254: The camera with the specified camera ID
sInfo = ueye.SENSORINFO()
cInfo = ueye.CAMINFO()
pcImageMemory = ueye.c_mem_p()
MemID = ueye.int()
rectAOI = ueye.IS_RECT()

pitch = ueye.INT()
nBitsPerPixel = ueye.INT(8)    #24: bits per pixel for color mode; take 8 bits per pixel for monochrome
channels = 1                    #3: channels for color mode(RGB); take 1 channel for monochrome
m_nColorMode = ueye.INT()		# Y8/RGB16/RGB24/REG32
bytes_per_pixel = int(nBitsPerPixel / 8)

pxclkv = ueye.INT(50)
exp_time = ueye.DOUBLE(130)
gain_factor = ueye.INT(80)
# frame_rate = ueye.IS_SETFR

cal = 0
#---------------------------------------------------------------------------------------------------------------------------------------
# Graph Set-Up

figx = Figure(figsize=(12, 4), dpi=200)
canvasx = FigureCanvas(figx)

figy = Figure(figsize=(12, 4), dpi=200)
canvasy = FigureCanvas(figy)

#---------------------------------------------------------------------------------------------------------------------------------------


"""
class FreshCameraStream:
    def __init__(self):
        self.cap = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        
        # Start a background thread to read frames
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while not self.stopped:
            if not self.cap.isOpened():
                break
            # Continuously overwrite with the latest frame
            self.ret, self.frame = self.cap.read()
            
    def read(self):
        return self.ret, self.frame

    def release(self):
        self.stopped = True
        self.thread.join()
        self.cap.release()

cam = FreshCameraStream()
"""
print("START")
print()


# Starts the driver and establishes the connection to the camera
nRet = ueye.is_InitCamera(hCam, None)
if nRet != ueye.IS_SUCCESS:
    print("is_InitCamera ERROR")

# Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
nRet = ueye.is_GetCameraInfo(hCam, cInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetCameraInfo ERROR")

# You can query additional information about the sensor type used in the camera
nRet = ueye.is_GetSensorInfo(hCam, sInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetSensorInfo ERROR")

nRet = ueye.is_ResetToDefault( hCam)
if nRet != ueye.IS_SUCCESS:
    print("is_ResetToDefault ERROR")

# Set display mode to DIB
nRet = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)

# Set the right color mode
if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
    # setup the color depth to the current windows setting
    ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_BAYER: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
    # for color camera models use RGB32 mode
    m_nColorMode = ueye.IS_CM_BGRA8_PACKED
    nBitsPerPixel = ueye.INT(32)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_CBYCRY: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
    # for color camera models use RGB32 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_MONOCHROME: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

else:
    # for monochrome camera models use Y8 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("else")

# Can be used to set the size and position of an "area of interest"(AOI) within an image
nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
if nRet != ueye.IS_SUCCESS:
    print("is_AOI ERROR")

width = rectAOI.s32Width
height = rectAOI.s32Height

# Prints out some information about the camera and the sensor
print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
print("Maximum image width:\t", width)
print("Maximum image height:\t", height)
print()

#---------------------------------------------------------------------------------------------------------------------------------------

# Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
nRet = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, MemID)
if nRet != ueye.IS_SUCCESS:
    print("is_AllocImageMem ERROR")
else:
    # Makes the specified image memory the active memory
    nRet = ueye.is_SetImageMem(hCam, pcImageMemory, MemID)
    if nRet != ueye.IS_SUCCESS:
        print("is_SetImageMem ERROR")
    else:
        # Set the desired color mode
        nRet = ueye.is_SetColorMode(hCam, m_nColorMode)



# Activates the camera's live video mode (free run mode)

nRet = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
if nRet != ueye.IS_SUCCESS:
    print("is_CaptureVideo ERROR")

# Enables the queue mode for existing image memory sequences
nRet = ueye.is_InquireImageMem(hCam, pcImageMemory, MemID, width, height, nBitsPerPixel, pitch)
if nRet != ueye.IS_SUCCESS:
    print("is_InquireImageMem ERROR")
else:
    print("Press q to leave the programm")

#---------------------------------------------------------------------------------------------------------------------------------------

#nRet = ueye.is_SetExposureTime(hCam,)
cross = io.imread(r'bitmaps\biggercross.bmp')
cross = cross[:,:,0]
cross = np.where(cross==255,1,0)
icross = np.where(cross==0,1,0)
zeros = np.zeros_like(cross)
cross = cross.astype(np.uint8)
icross = icross.astype(np.uint8)
zeros = zeros.astype(np.uint8)


# nRet = ueye.is_PixelClock(hCam,ueye.IS_PIXELCLOCK_CMD_SET,pxclkv,ueye.sizeof(pxclkv))
if nRet != ueye.IS_SUCCESS:
    print("is_PixelClock ERROR")
else:
    print("Press q to leave the programm")
print(nRet)

nRet = ueye.is_Exposure(hCam,ueye.IS_EXPOSURE_CMD_SET_EXPOSURE,exp_time,ueye.sizeof(exp_time))
if nRet != ueye.IS_SUCCESS:
    print("is_Exposure ERROR")
else:
    print("Press q to leave the programm")
print(nRet)

nRet = ueye.is_SetHardwareGain(hCam ,gain_factor,ueye.IS_IGNORE_PARAMETER,ueye.IS_IGNORE_PARAMETER,ueye.IS_IGNORE_PARAMETER)
if nRet != ueye.IS_SUCCESS:
    print("is_SetHWGainFactor ERROR")
else:
    print("Press q to leave the programm")
print(nRet)

x = np.arange(222)
y = np.linspace(0,20,222)
axx = figx.gca()
axx.axis('off')
axisx, = axx.plot(x,y,'b')
axy = figy.gca()
axy.axis('off')
axisy, = axy.plot(x,y,'b')
yxn = np.zeros((222,5))
yyn = np.zeros((222,5))
#ax.ylim(0,300)
# Continuous image display


def calibrate():
    global cal
    print('Calibrate','Begin motion over light field press OK')
    input()
    array = np.array(ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False), dtype=np.float64)
    frame = np.reshape(array,(height.value, width.value, bytes_per_pixel))
    Larray = np.zeros_like(frame)
    Darray = np.zeros_like(frame)
    for i in range(20):
        array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)
        frame = np.reshape(array,(height.value, width.value, bytes_per_pixel))
        Larray += frame/20
    
    print('Calibrate','Begin motion over dark field press OK')
    input()
    for i in range(20):
        array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)
        frame = np.reshape(array,(height.value, width.value, bytes_per_pixel))
        Darray += frame/20

    #msgbox.showinfo('Calibrate','Calibration Finished!')

    Lmean = np.mean(Larray)
    Dmean = np.mean(Darray)

    cal = 1

    return Lmean, Dmean, Larray, Darray

def correct(R,l,d,L,D):
    C = (R-D)*((l-d)/(L-D)) + d
    C = C.astype(np.uint8)
    return C

nRet = ueye.is_Exposure(hCam,ueye.IS_EXPOSURE_CMD_SET_EXPOSURE,exp_time,ueye.sizeof(exp_time))
if nRet != ueye.IS_SUCCESS:
    print("is_Exposure ERROR")
else:
    print("Press q to leave the programm")
print(nRet)


while(nRet == ueye.IS_SUCCESS):

    # In order to display the image in an OpenCV window we need to...
    # ...extract the data of our image memory
    array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)

    # bytes_per_pixel = int(nBitsPerPixel / 8)

    # ...reshape it in an numpy array...
    frame = np.reshape(array,(height.value, width.value))
    #frame = transform.resize(frame,(1920,2560))
    #if cal == 1:
    #    frame = correct(frame, Lmean, Dmean, Larray, Darray)

    yxm = np.squeeze(np.mean(frame[int(height.value/2)-110:int(height.value/2)+112,int(width.value/2)-111:int(width.value/2)+111],axis = 0))
    yxp = np.squeeze(np.mean(frame[int(height.value/2)-110:int(height.value/2)+112,int(width.value/2)-109:int(width.value/2)+113],axis = 0))
    yxn[:,4] = yxn[:,3]
    yxn[:,3] = yxn[:,2]
    yxn[:,2] = yxn[:,1]
    yxn[:,1] = yxn[:,0]
    yxn[:,0] = np.absolute((yxp-yxm)/2)
    yx = np.squeeze(np.mean(yxn, axis = 1))

    
  
    
    yym = np.squeeze(np.mean(frame[int(height.value/2)-111:int(height.value/2)+111,int(width.value/2)-110:int(width.value/2)+112],axis = 1))
    yyp = np.squeeze(np.mean(frame[int(height.value/2)-109:int(height.value/2)+113,int(width.value/2)-110:int(width.value/2)+112],axis = 1))
    yyn[:,4] = yyn[:,3]
    yyn[:,3] = yyn[:,2]
    yyn[:,2] = yyn[:,1]
    yyn[:,1] = yyn[:,0]
    yyn[:,0] = np.absolute((yyp-yym)/2)
    yy = np.squeeze(np.mean(yyn, axis = 1))
    

    axisx.set_ydata(yx)
    canvasx.draw()
    rgba_buffer_x = canvasx.buffer_rgba()
    graphimgx = np.asarray(rgba_buffer_x) 
    graphimgx = graphimgx[..., :3]
    graphimgx = np.asarray(canvasx.buffer_rgba())[..., :3].copy().reshape(800, 2400, 3)
    # graphimgx = np.fromstring(canvasx.tostring_rgb(), dtype='uint8').reshape(800, 2400, 3)

    axisy.set_ydata(yy)
    canvasy.draw()
    rgba_buffer_y = canvasy.buffer_rgba()
    graphimgy = np.asarray(rgba_buffer_y) 
    graphimgy = np.rot90(graphimgy[..., :3])
    # graphimgy = np.rot90(np.fromstring(canvasy.tostring_rgb(), dtype='uint8').reshape(800, 2400, 3),k=3)
    
    # get which axis we are measuring 
    if os.path.isfile('xyrequest.npy'):
        # time.sleep(0.1)
        a = numpy.load('xyrequest.npy')
        print(a)
        os.remove('xyrequest.npy')
        # save the array to a .npy file so carusoII.py can read it
        if a == 1:
            numpy.save('xydata.npy', yx)
        if a == 0:
            numpy.save('xydata.npy', yy)


    # ...resize the image by a half
    
    fy, fx = frame.shape
    #print(frame)
    frame2 = np.dstack((frame,frame,frame))
    
    #redx = graphimgx[:,:,1] < 160
    #graphimgx = frame2[0:800,int(width.value/2)-1200:int(width.value/2)+1200]
    #graphimgx[redx] = [0,0,255]

    #redy = graphimgy[:,:,1] < 160
    #graphimgy =  frame2[int(height.value/2)-1200:int(height.value/2)+1200,-800:]
    #graphimgy[redy] = [0,0,255]
    
    frame2[0:800,int(width.value/2)-1200:int(width.value/2)+1200] = graphimgx
    frame2[int(height.value/2)-1200:int(height.value/2)+1200,-800:] = graphimgy
    frame2 = frame2*np.dstack((cross,cross,cross)) + np.dstack((zeros,icross*255,zeros))
    
    frame2 = cv2.resize(frame2,(0,0),fx=0.5, fy=0.5)
    
    #print(frame2)

    #frame2[int(fy/2)-1:int(fy/2),int(fx/2)-100:int(fx/2)+100,0:2] = (frame2[int(fy/2)-1:int(fy/2),int(fx/2)-100:int(fx/2)+100,0:2]/2).astype(np.uint8)
    #frame2[int(fy/2)-100:int(fy/2)+100,int(fx/2)-1:int(fx/2),0:2] = (frame2[int(fy/2)-100:int(fy/2)+100,int(fx/2)-1:int(fx/2),0:2]/2).astype(np.uint8)


    #frame2[int(fy/2)-1:int(fy/2),int(fx/2)-300:int(fx/2)+300,:] = [0,255,0]
    #frame2[int(fy/2)-300:int(fy/2)+300,int(fx/2)-1:int(fx/2),:] = [0,255,0]
    """
    ret, frame = cam.read() # Guaranteed fresh frame
    if not ret:
        break
    cv2.imshow("Fresh Frame", frame)
    """
#---------------------------------------------------------------------------------------------------------------------------------------
    #Include image data processing here

#---------------------------------------------------------------------------------------------------------------------------------------

    #...and finally display it
    cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame2)
    # cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame)

    # Press q if you want to end the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        Lmean, Dmean, Larray, Darray = calibrate()
#---------------------------------------------------------------------------------------------------------------------------------------

# Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
ueye.is_FreeImageMem(hCam, pcImageMemory, MemID)

# Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
ueye.is_ExitCamera(hCam)

# Destroys the OpenCv windows
cv2.destroyAllWindows()

print()
print("END")
