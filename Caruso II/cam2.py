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
from pyueye import ueye
import numpy as np
import cv2
from skimage import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import time
from typing import Literal

##### constants #####

CAM1_SN = "4102904421" # UI148xSE-M, can find these numbers in the camera manager in IDS Cockpit
CAM2_SN = "4103530378" # UI320xSE-M 
CAM1_ID = 11
CAM2_ID = 12

GRAPH_UPDATE_EVERY = 1 # how often we update the matplot graph
DISPLAY_SCALE = 0.25 # scale for the feed window size
# BUFFER_COUNT = 4
RETICLE_SIZE = 222 # 222 by 222 square (green), not including the cross hairs
FULL_WIDTH = 4104 # px, camera feed window dimensions
FULL_HEIGHT = 3006 # px
WINDOW_SCALE = 2696/3006 # we make the window smaller to decrease lag
GRAPH_WIDTH = 1200 # dimensions of the graphs overlayed on the camera feed
GRAPH_HEIGHT = 400

EDGE_HISTORY_LENGTH = 5 # n_edges to average over, temporally

##### uEye variables #####

hCam = ueye.HIDS(CAM2_ID) # camera handle
sInfo = ueye.SENSORINFO() # hardware info
cInfo = ueye.CAMINFO() # model info
rectAOI = ueye.IS_RECT() # rectangle initialization

pitch = ueye.INT() # # of bytes in a single row of pixels in memory
nBitsPerPixel = ueye.INT(8) 
m_nColorMode = ueye.INT(ueye.IS_CM_MONO8) # grey scale
bytes_per_pixel = 1

# pxclkv = ueye.INT(99) # pixel clock
exp_time = ueye.DOUBLE(50) # exposure time
gain_factor = ueye.INT(100) # gain
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

# wait for a new image
def wait_for_frame(timeout_ms=1000):

    # check that we successfully got a frame, that it was the right size, 
    ret = ueye.is_FreezeVideo(hCam, ueye.IS_WAIT)
    if ret != ueye.IS_SUCCESS:
        print("is_WaitForNextImage ERROR:", ret)
        return None
    try:
        array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=True) # get the image data
        expected_size = height.value * width.value * bytes_per_pixel
        if array is None or len(array) < expected_size:
            print("empty/incomplete frame:", 0 if array is None else len(array))
            return None

        frame = np.reshape(array, (height.value, width.value)).copy() # reshape the frame into a numpy array
        return frame

    finally:
        # always unlock the sequence buffer after WaitForNextImage succeeds.
        ueye.is_UnlockSeqBuf(hCam, memID, pcImageMemory)

# allocate one image buffer for FreezeVideo / get_data
def allocate_single_buffer():
    global pcImageMemory, memID, pitch

    # allocate the memory and check that the allocation was successful
    ret = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, memID)
    check_ret("is_AllocImageMem", ret, fatal=True)

    ret = ueye.is_SetImageMem(hCam, pcImageMemory, memID)
    check_ret("is_SetImageMem", ret, fatal=True)

    ret = ueye.is_InquireImageMem(hCam, pcImageMemory, memID, width, height, nBitsPerPixel, pitch)
    check_ret("is_InquireImageMem", ret, fatal=True)

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

# get the peak of both graphs, for autofocus (maybe)
def get_peak(axis):
    return peak_x, peak_y

# calculate a focus score for the passed in frame using the variance of the Laplacian
def calc_focus():
   print("not ready yet :(")

# should ask james if he ever uses this (press c to calibrate)
def calibrate(num_frames=20):
    global cal

    # operator moves the camera over a light colored target?
    print("Calibrate: begin motion over light field, then press Enter")
    input()
    Larray = None

    for _ in range(num_frames):
        frame = wait_for_frame()
        if frame is None:
            continue
        frame_f = frame.astype(np.float64)
        if Larray is None:
            Larray = np.zeros_like(frame_f)
        Larray += frame_f / num_frames # add 1/20th of each frame's intesity here to get the average intensity?

    # operator moves the camera over a light colored target?
    print("Calibrate: begin motion over dark field, then press Enter")
    input()
    Darray = None

    for _ in range(num_frames):
        frame = wait_for_frame()
        if frame is None:
            continue
        frame_f = frame.astype(np.float64)
        if Darray is None:
            Darray = np.zeros_like(frame_f)
        Darray += frame_f / num_frames # add 1/20th of each frame's intesity here to get the average intensity?

    if Larray is None or Darray is None:
        print("Calibration failed: no valid frames")
        return None, None, None, None

    Lmean = np.mean(Larray) # one int representing the average intesity of the 20 light frames
    Dmean = np.mean(Darray) # one int representing the average intesity of the 20 dark frames

    cal = 1
    print("Calibration finished")
    return Lmean, Dmean, Larray, Darray

# if we do the calibration this is for correcting the raw image based on that i think
# R = raw image, L = Larray, D = Darray, l = Lmean, d = Dmean
def correct(R, l, d, L, D):
    C = (R - D) * ((l - d) / (L - D)) + d # flat field correction
    return C.astype(np.uint8)

def set_edge_profiles(
    frame:np.ndarray, 
    axis:Literal["x", "y"], 
    edge_history: np.ndarray,
) -> np.ndarray:
    """
    Populate the edge profile array for the specified axis

    ### Note:
        GMT's implementation of a "better" edge detection algorithm. 
        This message can be deleted.

    Args:
        frame (np.ndarray):
            2D image array from video frame
        axis (Literal["x", "y"]): 
            'x' or 'y' axis (direction of edge detection) 
        edge_history (np.ndarray):
            Rolling history of previous edge profiles.
            shape=(RETICLE_SIZE, 5)
        
    Returns:
        np.ndarray: 
            Smoothed edge profile.
            shape=(RETICLE_SIZE,), dtype=float.
    """
    # Spatial offset used for edge detection
    shift = 2
    correction = 1

    # Reticle crop region
    height, width = frame.shape[:2]

    half = RETICLE_SIZE // 2
    top = height // 2 - half
    bottom = top + RETICLE_SIZE
    left = width // 2 - half
    right = left + RETICLE_SIZE

    # Horizontal edge
    if axis == "x":
        centered = frame[
            top + correction : bottom + correction,
            left:right,
        ].mean(axis=0)

        shifted = frame[
            top + correction : bottom + correction,
            left + shift : right + shift,
        ].mean(axis=0)

    # Vertical edge
    elif axis == "y":
        centered = frame[
            top:bottom,
            left + correction : right + correction,
        ].mean(axis=1)

        shifted = frame[
            top + shift : bottom + shift,
            left + correction : right + correction,
        ].mean(axis=1)

    else:
        raise ValueError("axis must be 'x' or 'y'")

    # Current edge magnitude
    edges = np.abs(shifted - centered) / shift
    
    # Update rolling (overriding) edge history
    edge_history[:, 1:] = edge_history[:, :-1]
    edge_history[:, 0] = edges
    """
    Frame 1
    [current, 0, 0, 0, 0]

    Frame 2
    [current2, current1, 0, 0, 0]
    
    ...
    
    Frame 5
    [current5, current4, current3, current2, current1]

    Frame 6
    [current6, current5, current4, current3, current2]
    """

    # Average across the history window
    return edge_history.mean(axis=1)

##### initialize camera #####
try:
    ret = ueye.is_InitCamera(hCam, None)
    # ret = ueye.is_InitCamera(hCam.IS_USE_DEVICE_ID(), None)
    check_ret("is_InitCamera", ret, fatal=True)

    ret = ueye.is_GetCameraInfo(hCam, cInfo)
    check_ret("is_GetCameraInfo", ret, fatal=True)

    ret = ueye.is_GetSensorInfo(hCam, sInfo)
    check_ret("is_GetSensorInfo", ret, fatal=True)

    ret = ueye.is_ResetToDefault(hCam)
    check_ret("is_ResetToDefault", ret, fatal=True)

    ret = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)
    check_ret("is_SetDisplayMode", ret, fatal=True)

    # set color mode
    ret = ueye.is_SetColorMode(hCam, m_nColorMode)
    check_ret("is_SetColorMode", ret, fatal=True)

    # pixel clock, idk what this isssss :'((((((((( smth to do with the frame rate i think
    # ret = ueye.is_PixelClock(hCam, ueye.IS_PIXELCLOCK_CMD_SET, pxclkv, ueye.sizeof(pxclkv))
    # check_ret("is_PixelClock SET", ret)

    # exposure, gain, fps
    ret = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, exp_time, ueye.sizeof(exp_time))
    check_ret("is_Exposure SET", ret)

    ret = ueye.is_SetHardwareGain(hCam, gain_factor, ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER)
    check_ret("is_SetHardwareGain", ret)

    ret = ueye.is_SetFrameRate(hCam, desired_fps, actual_fps)
    check_ret("is_SetFrameRate", ret)

    # get AOI (area of interest)
    ret = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
    if ret != ueye.IS_SUCCESS:
        print("is_AOI ERROR")

    full_w = rectAOI.s32Width.value # 4104 px
    full_h = rectAOI.s32Height.value # 3006 px

    # making our requested AOI smaller def helps with decreasing the lag of the camera feed window, but making it too small makes it tough for the operator to use
    aoi_w = int(round(FULL_WIDTH * WINDOW_SCALE / 16) * 16) # 3680, has to be multiple of 16
    aoi_h = int(FULL_HEIGHT * WINDOW_SCALE) # 2696, has to be multiple of 4

    rectAOI.s32X = ueye.INT((full_w - aoi_w) // 2) # width margins
    rectAOI.s32Y = ueye.INT((full_h - aoi_h) // 2) # height margins
    rectAOI.s32Width = ueye.INT(aoi_w) # set the width
    rectAOI.s32Height = ueye.INT(aoi_h) # set the height

    ret = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_SET_AOI, rectAOI, ueye.sizeof(rectAOI))
    check_ret("is_AOI", ret)

    width = rectAOI.s32Width # actual width
    height = rectAOI.s32Height # actual height

    # allocate image sequence buffer
    allocate_single_buffer()

    # start live capture after buffers are in the sequence
    # ret = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
    # check_ret("is_CaptureVideo", ret, fatal=True)

    # prints out some information about the camera and the sensor
    print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
    print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
    print("Maximum image width:\t", width)
    print("Maximum image height:\t", height)
    print()

    print("\nPress q to leave the program")
    print("Press c to calibrate\n")


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
    cross = np.where(cross == BLACK, 1, 0).astype(np.uint8) # convert the bmp to binary
    icross = np.where(cross == 0, 1, 0).astype(np.uint8) # invert the bmp
    zeros = np.zeros_like(cross, dtype=np.uint8) # all 0 array

    overlay_green = np.dstack((zeros, icross * BLACK, zeros)) # put the cross data in the green channel
    overlay_mask = np.dstack((cross, cross, cross)) # make the mask 3-channel
    
    ##### main display loop #####
    # two graphs are displayed, one for the x axis, one for the y axis. they have peaks where there are edges (a pixel is darker/lighter than its neighbor)
    i = 0

    # Temporal smoothing
    # Averages last (EDGE_HISTORY) number of scans together 
    # Updates average every GRAPH_UPDATE_EVERY
    x_edge_history = np.zeros((RETICLE_SIZE, EDGE_HISTORY_LENGTH), dtype=np.float64)
    y_edge_history = np.zeros((RETICLE_SIZE, EDGE_HISTORY_LENGTH), dtype=np.float64)
    while True:
        # loop until we get a frame
        nRet = ueye.is_FreezeVideo(hCam, ueye.IS_WAIT)
        if nRet != ueye.IS_SUCCESS:
            print("FreezeVideo error:", nRet)
            continue

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
            averaged_edges_x = set_edge_profiles(frame, "x", x_edge_history)
            averaged_edges_y = set_edge_profiles(frame, "y", y_edge_history)
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

            axisy.set_ydata(averaged_edges_y)
            canvasy.draw() # render the figure into memory
            # graphimgy = np.asarray(canvasy.buffer_rgba()[..., :3]).copy() # convert to 4 channel buffer, then to numpy array
            # graphimgy = np.rot90(np.asarray(canvasy.buffer_rgba())[..., :3]).copy() # convert to 4 channel buffer, then to numpy array
            graphimgy = np.rot90(np.asarray(canvasy.buffer_rgba()).copy(), k=3)  # k=3 rotates the array ccw 3 times 
    
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

        # apply reticle overlay
        if overlay_mask.shape == frame2.shape: # if the bmp and frame dimensions are the same
            frame2 = frame2 * overlay_mask + overlay_green
        else:
            # if the bmp and frame dimensions are not the same, resize the reticle
            mask_fit = cv2.resize(overlay_mask, (frame2.shape[1], frame2.shape[0]), interpolation=cv2.INTER_NEAREST)
            green_fit = cv2.resize(overlay_green, (frame2.shape[1], frame2.shape[0]), interpolation=cv2.INTER_NEAREST)
            frame2 = frame2 * mask_fit + green_fit

        # NOTE: Add compression of n_bits to see if that improves performance
        frame2 = cv2.resize(frame2, (0, 0), fx=DISPLAY_SCALE, fy=DISPLAY_SCALE) # decrease the window size to make it more usable

        # cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame2)
        cv2.imshow("Camera 2 (High Magnification)", frame2)

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