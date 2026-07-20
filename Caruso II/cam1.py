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
from skimage import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import time

##### constants #####

CAM1_SN = "4102904421" # UI148xSE-M, can find these numbers in the camera manager in IDS Cockpit
CAM2_SN = "4103530378" # UI320xSE-M 
CAM1_ID = 11
CAM2_ID = 12

GRAPH_UPDATE_EVERY = 1 # how often we update the matplot graph
DISPLAY_SCALE = 0.25 # scale for the feed window size
# BUFFER_COUNT = 4
RETICLE_SIZE = 200 # 200 by 200 square (green), not including the cross hairs
FULL_WIDTH = 2560 # px, camera feed window dimensions
FULL_HEIGHT = 1920 # px
WINDOW_SCALE = 2400/2560 # we make the window smaller to decrease lag
GRAPH_WIDTH = 800 # dimensions of the graphs overlayed on the camera feed
GRAPH_HEIGHT = 400

##### uEye variables #####

hCam = ueye.HIDS(CAM1_ID) # camera handle
sInfo = ueye.SENSORINFO() # hardware info
cInfo = ueye.CAMINFO() # model info
rectAOI = ueye.IS_RECT() # rectangle initialization

pitch = ueye.INT() # # of bytes in a single row of pixels in memory
nBitsPerPixel = ueye.INT(8) 
m_nColorMode = ueye.INT(ueye.IS_CM_MONO8) # grey scale
bytes_per_pixel = 1

pxclkv = ueye.INT(16) # pixel clock
exp_time = ueye.DOUBLE(50) # exposure time
gain_factor = ueye.INT(10) # gain
desired_fps = ueye.DOUBLE(24) # user specified frame/sec
actual_fps = ueye.DOUBLE() # camera specified frame/sec

pcImageMemory = ueye.c_mem_p() # points to the address where the raw image data is stored
memID = ueye.int() # camera will populate this later

##### other variables #####

cal = 0 # for calibration? we don't do this

width = None # dimensions of the camera feed window
height = None
peak_x = 0 # variables for holding the maximums of the curve in the graphs 
peak_y = 0
centered_window = np.zeros((RETICLE_SIZE, RETICLE_SIZE))

# img_buffers = []

##### helper functions #####

# check for a uEye error
def check_ret(name, ret, fatal=False):
    if ret != ueye.IS_SUCCESS:
        print(f"{name} ERROR: {ret}")
        if fatal:
            raise RuntimeError(f"{name} failed with code {ret}")
    else:
        print(f"{name}: OK")
    return ret

# stop camera acquisition and release all uEye resources
def cleanup():
    try:
        ueye.is_StopLiveVideo(hCam, ueye.IS_FORCE_VIDEO_STOP)
    except Exception:
        pass
    # leftover from when i tried multiple buffers to speed up the feed
    """
    try:
        ueye.is_ExitImageQueue(hCam)
    except Exception:
        pass

    try:
        ueye.is_ClearSequence(hCam)
    except Exception:
        pass

    for pcMem, memID in img_buffers:
        try:
            ueye.is_FreeImageMem(hCam, pcMem, memID)
        except Exception:
            pass
    """
    # ueye.is_FreeImageMem(hCam, pcImageMemory, memID)
    try:
        ueye.is_ExitCamera(hCam)
    except Exception:
        pass

    cv2.destroyAllWindows()

# should ask james if he ever uses this (press c to calibrate)
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

# if we do the calibration this is for correcting the raw image based on that i think
# R = raw image, L = Larray, D = Darray, l = Lmean, d = Dmean
def correct(R,l,d,L,D):
    C = (R-D)*((l-d)/(L-D)) + d
    C = C.astype(np.uint8)
    return C

# populate the edge profile array for the specified axis
# ask GMT about implementing a better edge detection algorithm?
def set_edge_profiles(frame, axis):
    # NOTE: where edge stuff happens
    h_mid = height.value // 2 # floor division
    w_mid = width.value // 2

    # store the edge profiles of the last 5 frames
    edge_profiles = np.zeros((RETICLE_SIZE, 5)) 

    """
    # limits of the reticle window
    reticle_window_t = int(h_mid - RETICLE_SIZE/2)
    reticle_window_b = int(h_mid + RETICLE_SIZE/2)
    reticle_window_l = int(w_mid - RETICLE_SIZE/2)
    reticle_window_r = int(w_mid + RETICLE_SIZE/2)
    """

    guess_y = 20
    guess_x = 100
    reticle_window_t = int(h_mid - guess_y)
    reticle_window_b = int(h_mid + guess_y)
    reticle_window_l = int(w_mid - guess_x)
    reticle_window_r = int(w_mid + guess_x)

    # smoothing? 
    # also, in the bmp of the reticle, the square bulges out slightly, i think that is to compensate for the distortion of the camera lens? 
    # i think we average the centered window and the offcenter window to get a derivative so there are high values near the edge and low values elsewhere
    # im unclear on why the correction is needed here, my guess is that it was just tuning the bmp to a known target? 
    correction = 1
    delta = 2
    """
    if axis == 'x':
        centered_window   = np.squeeze(np.mean(frame[reticle_window_t + correction:reticle_window_b + correction, reticle_window_l:reticle_window_r], axis=0)) # squeeze eliminates empty dimensions, mean averages the array elements (along the 0th axis)
        off_center_window = np.squeeze(np.mean(frame[reticle_window_t + correction:reticle_window_b + correction, reticle_window_l + delta:reticle_window_r + delta], axis=0))
    if axis == 'y':
        centered_window   = np.squeeze(np.mean(frame[reticle_window_t:reticle_window_b, reticle_window_l + correction:reticle_window_r + correction], axis=1)) # squeeze eliminates empty dimensions, mean averages the array elements (along the 0th axis)
        off_center_window = np.squeeze(np.mean(frame[reticle_window_t + delta:reticle_window_b + delta, reticle_window_l + correction:reticle_window_r + correction], axis=1))
        """

    if axis == 'x':
        centered_window   = np.squeeze(np.mean(frame[reticle_window_t:reticle_window_b, reticle_window_l - correction:reticle_window_r - correction], axis=0)) # squeeze eliminates empty dimensions, mean averages the array elements (along the 0th axis)
        off_center_window = np.squeeze(np.mean(frame[reticle_window_t:reticle_window_b, reticle_window_l + correction:reticle_window_r + correction], axis=0))
    if axis == 'y':
        centered_window   = np.squeeze(np.mean(frame[int(h_mid - guess_x - correction):int(h_mid + guess_x - correction), int(w_mid - guess_y):int(w_mid + guess_y)], axis=1)) # squeeze eliminates empty dimensions, mean averages the array elements (along the 0th axis)
        off_center_window = np.squeeze(np.mean(frame[int(h_mid - guess_x + correction):int(h_mid + guess_x + correction), int(w_mid - guess_y):int(w_mid + guess_y)], axis=1))

    # populate the edge profiles
    edge_profiles[:, 4] = edge_profiles[:, 3]
    edge_profiles[:, 3] = edge_profiles[:, 2]
    edge_profiles[:, 2] = edge_profiles[:, 1]
    edge_profiles[:, 1] = edge_profiles[:, 0]
    edge_profiles[:, 0] = np.absolute((off_center_window - centered_window) / 2)
    averaged_edges = np.squeeze(np.mean(edge_profiles, axis=1)) # smooth the profiles?

    return averaged_edges

##### initialize camera #####
try:
    ret = ueye.is_InitCamera(hCam, None)
    check_ret("is_InitCamera", ret, fatal=True)

    ret = ueye.is_GetCameraInfo(hCam, cInfo)
    check_ret("is_GetCameraInfo", ret, fatal=True)

    ret = ueye.is_GetSensorInfo(hCam, sInfo)
    check_ret("is_GetSensorInfo", ret, fatal=True)

    ret = ueye.is_ResetToDefault( hCam)
    check_ret("is_ResetToDefault", ret, fatal=True)

    ret = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)
    check_ret("is_SetDisplayMode", ret, fatal=True)

    # set color mode
    ret = ueye.is_SetColorMode(hCam, m_nColorMode)
    check_ret("is_SetColorMode", ret, fatal=True)

    # pixel clock, idk what this isssss :'((((((((( smth to do with the frame rate i think
    ret = ueye.is_PixelClock(hCam, ueye.IS_PIXELCLOCK_CMD_SET, pxclkv, ueye.sizeof(pxclkv))
    check_ret("is_PixelClock SET", ret)

    # exposure, gain, fps
    ret = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, exp_time, ueye.sizeof(exp_time))
    check_ret("is_Exposure SET", ret)

    ret = ueye.is_SetHardwareGain(hCam, gain_factor, ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER)
    check_ret("is_SetHardwareGain", ret)

    ##### check that this isnt the problem #####
    ret = ueye.is_SetFrameRate(hCam, desired_fps, actual_fps)
    check_ret("is_SetFrameRate", ret)

    # Can be used to set the size and position of an "area of interest"(AOI) within an image
    ret = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
    if ret != ueye.IS_SUCCESS:
        print("is_AOI ERROR")

    width = rectAOI.s32Width
    height = rectAOI.s32Height

    full_w = rectAOI.s32Width.value # 2560 px
    full_h = rectAOI.s32Height.value # 1920 px

    # prints out some information about the camera and the sensor
    print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
    print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
    print("Maximum image width:\t", width)
    print("Maximum image height:\t", height)
    print()

    # allocate the memory and check that the allocation was successful
    ret = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, memID)
    check_ret("is_AllocImageMem", ret, fatal=True)

    ret = ueye.is_SetImageMem(hCam, pcImageMemory, memID)
    check_ret("is_SetImageMem", ret, fatal=True)

    ret = ueye.is_InquireImageMem(hCam, pcImageMemory, memID, width, height, nBitsPerPixel, pitch)
    check_ret("is_InquireImageMem", ret, fatal=True)

    # activate live video mode (free run mode)
    ret = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
    if ret != ueye.IS_SUCCESS:
        print("is_CaptureVideo ERROR")

    ##### graph setup #####

    figx = Figure(figsize=(12, 2), dpi=200, frameon=False) # matplot top level container for plot elements
    canvasx = FigureCanvas(figx) # matplot container for pixel drawing commands

    figy = Figure(figsize=(12, 2), dpi=200, frameon=False) # matplot top level container for plot elements
    canvasy = FigureCanvas(figy) # matplot container for pixel drawing commands

    # axes spacing
    x = np.arange(RETICLE_SIZE) 
    y = np.linspace(0, 5, RETICLE_SIZE)

    axx = figx.gca() # handle for the axes
    axx.axis('off') # hide the axes
    axx.margins(0)
    axisx, = axx.plot(x, y, 'b') # make the plotline (blue? do we switch it to red later?)

    axy = figy.gca() # handle for the axes
    axy.axis('off') # hide the axes
    axy.margins(0)
    axisy, = axy.plot(x, y, 'b') # make the plotline (blue? do we switch it to red later?)
    figx.patch.set_alpha(0)
    axy.patch.set_alpha(0)

    # initialize graph images so they exist before the first paste.
    canvasx.draw() # render the current fig into memory
    graphimgx = np.asarray(canvasx.buffer_rgba()).copy() # get the rendered pixels, return a 4-channel buffer, convert to numpy array
    canvasy.draw() # render the current fig into memory
    graphimgy = np.rot90(np.asarray(canvasy.buffer_rgba()).copy(), k=3) # get the rendered pixels, return a 4-channel buffer, convert to numpy array, k=3 rotates the array ccw 3 times
    # graphimgy = np.asarray(canvasy.buffer_rgba()[..., :3]).copy() # get the rendered pixels, return a 4-channel buffer, convert to numpy array
    # graphimgy = np.rot90(np.asarray(canvasy.buffer_rgba())[..., :3]).copy() # get the rendered pixels, return a 4-channel buffer, convert to numpy array

    ##### reticle setup #####
    # make a mask to overlay the camera feed
    BLACK = 255
    cross = io.imread(r'bitmaps\biggercross.bmp') # reticle bitmap
    
    cross = cross[:, :, 0] # convert the bmp to 2D
    # cross = np.where(cross == BLACK, 1, 0).astype(np.uint8) # convert the bmp to binary
    background = cross > 200
    cross = background.astype(np.uint8)
    icross = (~background).astype(np.uint8)
    # icross = np.where(cross == 0, 1, 0).astype(np.uint8) # invert the bmp
    zeros = np.zeros_like(cross, dtype=np.uint8) # all 0 array

    overlay_green = np.dstack((zeros, icross * BLACK, zeros)) # put the cross data in the green channel
    # overlay_mask = np.dstack((cross, cross, cross)) # make the mask 3-channel
    overlay_mask = np.dstack((background, background, background)).astype(np.uint8)
    frame_cross = cv2.resize(cross * 255, (0, 0), fx=DISPLAY_SCALE, fy=DISPLAY_SCALE)
    cv2.imshow("Reticle mask", frame_cross)
    cv2.waitKey(0)

    ##### main display loop #####
    # two graphs are displayed, one for the x axis, one for the y axis. they have peaks where there are edges (a pixel is darker/lighter than its neighbor)
    i = 0
    while True:
              # loop until we get the image data
        array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=True)
        if array is None or len(array) == 0:
            continue

        frame = np.reshape(array, (height.value, width.value))
        if cal == 1:
            frame = correct(frame, Lmean, Dmean, Larray, Darray)
        frame2 = np.dstack((frame, frame, frame)) # turns the grayscale image into a 3-channel image

        # only recompute/redraw graphs every N frames.
        if i % GRAPH_UPDATE_EVERY == 0:
            
            # get the edge data for both axes
            averaged_edges_x = set_edge_profiles(frame, 'x')
            averaged_edges_y = set_edge_profiles(frame, 'y')
            peak_x = np.max(averaged_edges_x)
            peak_y = np.max(averaged_edges_y)
            """
            print("curve_peak")
            print(peak_x)
            print(peak_y)
            """

            # populate the two graphs with the edge data
            axisx.set_ydata(averaged_edges_x)
            canvasx.draw() # render the figure into memory
            graphimgx = np.asarray(canvasx.buffer_rgba()).copy() # convert to 4 channel buffer, then to numpy array
            # get rid of the white background of the graphs
            # redx = graphimgx[:,:,1] < 160
            # graphimgx[redx] = [0,0,255]

            axisy.set_ydata(averaged_edges_y)
            canvasy.draw() # render the figure into memory
            # graphimgy = np.asarray(canvasy.buffer_rgba()[..., :3]).copy() # convert to 4 channel buffer, then to numpy array
            # graphimgy = np.rot90(np.asarray(canvasy.buffer_rgba())[..., :3]).copy() # convert to 4 channel buffer, then to numpy array
            graphimgy = np.rot90(np.asarray(canvasy.buffer_rgba()).copy(), k=3)  # k=3 rotates the array ccw 3 times 
            # get rid of the white background of the graphs
            # redy = graphimgy[:,:,1] < 160
            # graphimgy[redy] = [0,0,255]
    
            # if the measuring routine needs edge data there will be a xyrequest.npy file
            if os.path.isfile('xyrequest.npy'):
                time.sleep(0.1)
                a = np.load('xyrequest.npy')
                print(a)
                os.remove('xyrequest.npy')
                # save the data from the requested axis
                if a == 1:
                    np.save('xydata.npy', averaged_edges_x)
                elif a == 0:
                    np.save('xydata.npy', averaged_edges_y)

        # set the dimensions of the graphs
        x_graph_row0 = 0
        x_graph_row1 = min(GRAPH_HEIGHT, frame2.shape[0])
        x_graph_col0 = int(width.value / 2) - GRAPH_WIDTH
        x_graph_col1 = int(width.value / 2) + GRAPH_WIDTH

        y_graph_row0 = int(height.value / 2) - GRAPH_WIDTH
        y_graph_row1 = int(height.value / 2) + GRAPH_WIDTH
        y_graph_col0 = frame2.shape[1] - GRAPH_HEIGHT
        y_graph_col1 = frame2.shape[1]

        # dont let the graph dimensions exceed the camera window dimensions
        x_graph_col0 = max(0, x_graph_col0)
        x_graph_col1 = min(frame2.shape[1], x_graph_col1)

        y_graph_row0 = max(0, y_graph_row0)
        y_graph_row1 = min(frame2.shape[0], y_graph_row1)

        # calculate the heights and widths of the graphs
        x_slot_h = x_graph_row1 - x_graph_row0
        x_slot_w = x_graph_col1 - x_graph_col0
        y_slot_h = y_graph_row1 - y_graph_row0
        y_slot_w = y_graph_col1 - y_graph_col0

        # update frame2 with the graphs, remove the white background of the graphs
        if x_slot_h > 0 and x_slot_w > 0:
            graphx_fit = cv2.resize(graphimgx, (x_slot_w, x_slot_h)) # resize the graph
            # frame2[x_graph_row0:x_graph_row1, x_graph_col0:x_graph_col1, :] = graphx_fit
            graph_rgb = graphx_fit[:, :, :3] # exclude the alpha channel
            alpha = graphx_fit[:, :, 3] / float(BLACK) # normalize the alpha channel 0-255 -> 0-1 
            graph_bgr = cv2.cvtColor(graph_rgb, cv2.COLOR_RGB2BGR)
            roi = frame2[x_graph_row0:x_graph_row1, x_graph_col0:x_graph_col1, :] # add the graph to frame2
            alpha = alpha[:, :, None] # add a dimension so the alpha mask can be applied to all three BGR channels
            roi[:] = (graph_bgr * alpha + roi * (1.0 - alpha)).astype(np.uint8) # alpha blend

        if y_slot_h > 0 and y_slot_w > 0:
            graphy_fit = cv2.resize(graphimgy, (y_slot_w, y_slot_h)) # resize the graph
            # frame2[y_graph_row0:y_graph_row1, y_graph_col0:y_graph_col1, :] = graphy_fit
            graph_rgb = graphy_fit[:, :, :3] # exclude the alpha channel
            alpha = graphy_fit[:, :, 3] / float(BLACK) # normalize the alpha channel 0-255 -> 0-1 
            graph_bgr = cv2.cvtColor(graph_rgb, cv2.COLOR_RGB2BGR)
            roi = frame2[y_graph_row0:y_graph_row1, y_graph_col0:y_graph_col1, :] # add the graph to frame2
            alpha = alpha[:, :, None] # add a dimension so the alpha mask can be applied to all three BGR channels
            roi[:] = (graph_bgr * alpha + roi * (1.0 - alpha)).astype(np.uint8) # alpha blend

        """
        # apply reticle overlay
        if overlay_mask.shape == frame2.shape: # if the bmp and frame dimensions are the same
            frame2 = frame2 * overlay_mask + overlay_green
        else:
            # if the bmp and frame dimensions are not the same, resize the reticle
            mask_fit = cv2.resize(overlay_mask, (frame2.shape[1], frame2.shape[0]), interpolation=cv2.INTER_NEAREST)
            green_fit = cv2.resize(overlay_green, (frame2.shape[1], frame2.shape[0]), interpolation=cv2.INTER_NEAREST)
            frame2 = frame2 * mask_fit + green_fit
            """

        # apply reticle overlay
        frame_h, frame_w = frame2.shape[:2]
        reticle_h, reticle_w = icross.shape
        row0 = (reticle_h - frame_h) // 2
        col0 = (reticle_w - frame_w) // 2
        reticle_fit = icross[row0:row0 + frame_h, col0:col0 + frame_w].astype(bool)
        frame2[reticle_fit] = [0, 255, 0]

        # NOTE: Add compression of n_bits to see if that improves performance
        frame2 = cv2.resize(frame2, (0, 0), fx=DISPLAY_SCALE, fy=DISPLAY_SCALE) # decrease the window size to make it more usable

        # cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame2)
        cv2.imshow("Camera 1 (Low Magnification)", frame2)

        i += 1

        key = cv2.waitKey(1) & 0xFF # wait for a keyboard press 

        if key == ord('q'): # exit
            break
        elif key == ord('c'): # begin calibration
            result = calibrate()
            if result[0] is not None:
                Lmean, Dmean, Larray, Darray = result

finally:
    cleanup()
    print("\nEND")