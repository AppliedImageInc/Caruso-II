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

##### camera properties #####
CAM_ID = 12  # 0: first available camera;  1-254: The camera with the specified camera ID
# BUFFER_COUNT = 4

pxclkv = ueye.INT(99) # pixel clock
exp_time = ueye.DOUBLE(100) # exposure time
gain_factor = ueye.INT(100) # gain
desired_fps = ueye.DOUBLE(24) # user specified frame/sec
actual_fps = ueye.DOUBLE() # camera specified frame/sec

GRAPH_UPDATE_EVERY = 1 # how often we update the matplot graph
DISPLAY_SCALE = 0.25 # scale for the feed window size

cal = 0 # for calibration? we don't do this


##### uEye variables #####

hCam = ueye.HIDS(CAM_ID) # camera handle
sInfo = ueye.SENSORINFO() # hardware info
cInfo = ueye.CAMINFO() # model info
rectAOI = ueye.IS_RECT() # rectangle initialization

pitch = ueye.INT() # # of bytes in a single row of pixels in memory
nBitsPerPixel = ueye.INT(8) 
m_nColorMode = ueye.INT(ueye.IS_CM_MONO8) # grey scale
bytes_per_pixel = 1

width = None
height = None

# img_buffers = []

##### other variables #####
cross_hair_size = 222 # 222 by 222 square (green)

# -------------------------------------------------------------------------
# Small helper for checking return codes
# -------------------------------------------------------------------------

def check_ret(name, ret, fatal=False):
    if ret != ueye.IS_SUCCESS:
        print(f"{name} ERROR: {ret}")
        if fatal:
            raise RuntimeError(f"{name} failed with code {ret}")
    else:
        print(f"{name}: OK")
    return ret


def wait_for_frame(timeout_ms=1000):
    """
    Wait for a fresh frame from the uEye image sequence.

    Returns
    -------
    frame : np.ndarray
        A copied mono8 image with shape (height.value, width.value), or None
        if no frame was available.
    """
    pcMem = ueye.c_mem_p()
    memID = ueye.int()

    ret = ueye.is_FreezeVideo(hCam, ueye.IS_WAIT)

    if ret != ueye.IS_SUCCESS:
        print("is_WaitForNextImage ERROR:", ret)
        return None

    try:
        array = ueye.get_data(
            pcMem,
            width,
            height,
            nBitsPerPixel,
            pitch,
            copy=True
        )

        expected_size = height.value * width.value * bytes_per_pixel

        if array is None or len(array) < expected_size:
            print("Empty/incomplete frame:", 0 if array is None else len(array))
            return None

        frame = np.reshape(array, (height.value, width.value)).copy()
        return frame

    finally:
        # Always unlock the sequence buffer after WaitForNextImage succeeds.
        ueye.is_UnlockSeqBuf(hCam, memID, pcMem)


def allocate_single_buffer():
    """
    Allocate one image buffer for FreezeVideo / get_data.
    """
    global pcImageMemory, MemID, pitch

    pcImageMemory = ueye.c_mem_p()
    MemID = ueye.int()

    ret = ueye.is_AllocImageMem(
        hCam,
        width,
        height,
        nBitsPerPixel,
        pcImageMemory,
        MemID
    )
    check_ret("is_AllocImageMem", ret, fatal=True)

    ret = ueye.is_SetImageMem(
        hCam,
        pcImageMemory,
        MemID
    )
    check_ret("is_SetImageMem", ret, fatal=True)

    ret = ueye.is_InquireImageMem(
        hCam,
        pcImageMemory,
        MemID,
        width,
        height,
        nBitsPerPixel,
        pitch
    )
    check_ret("is_InquireImageMem", ret, fatal=True)


def cleanup():
    """
    Stop camera acquisition and release all uEye resources.
    """
    try:
        ueye.is_StopLiveVideo(hCam, ueye.IS_FORCE_VIDEO_STOP)
    except Exception:
        pass
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
    # ueye.is_FreeImageMem(hCam, pcImageMemory, MemID)
    try:
        ueye.is_ExitCamera(hCam)
    except Exception:
        pass

    cv2.destroyAllWindows()


# -------------------------------------------------------------------------
# Initialize camera
# -------------------------------------------------------------------------

print("START\n")

try:
    ret = ueye.is_InitCamera(hCam, None)
    check_ret("is_InitCamera", ret, fatal=True)

    ret = ueye.is_GetCameraInfo(hCam, cInfo)
    check_ret("is_GetCameraInfo", ret, fatal=True)

    ret = ueye.is_GetSensorInfo(hCam, sInfo)
    check_ret("is_GetSensorInfo", ret, fatal=True)

    ret = ueye.is_ResetToDefault(hCam)
    check_ret("is_ResetToDefault", ret, fatal=True)

    ret = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)
    check_ret("is_SetDisplayMode", ret, fatal=True)

    # Choose color mode.
    if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
        ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        print("IS_COLORMODE_BAYER")
        print("\tm_nColorMode:", m_nColorMode)
        print("\tnBitsPerPixel:", nBitsPerPixel)
        print("\tbytes_per_pixel:", bytes_per_pixel)

    elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
        m_nColorMode = ueye.INT(ueye.IS_CM_BGRA8_PACKED)
        nBitsPerPixel = ueye.INT(32)
        bytes_per_pixel = 4
        print("IS_COLORMODE_CBYCRY")
        print("\tm_nColorMode:", m_nColorMode)
        print("\tnBitsPerPixel:", nBitsPerPixel)
        print("\tbytes_per_pixel:", bytes_per_pixel)

    elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
        m_nColorMode = ueye.INT(ueye.IS_CM_MONO8)
        nBitsPerPixel = ueye.INT(8)
        bytes_per_pixel = 1
        print("IS_COLORMODE_MONOCHROME")
        print("\tm_nColorMode:", m_nColorMode)
        print("\tnBitsPerPixel:", nBitsPerPixel)
        print("\tbytes_per_pixel:", bytes_per_pixel)

    else:
        m_nColorMode = ueye.INT(ueye.IS_CM_MONO8)
        nBitsPerPixel = ueye.INT(8)
        bytes_per_pixel = 1
        print("Unknown color mode, using MONO8")

    # Set color mode before allocating buffers.
    ret = ueye.is_SetColorMode(hCam, m_nColorMode)
    check_ret("is_SetColorMode", ret, fatal=True)

    # Optional pixel clock. Uncomment if desired.
    # ret = ueye.is_PixelClock(hCam, ueye.IS_PIXELCLOCK_CMD_SET, pxclkv, ueye.sizeof(pxclkv))
    # check_ret("is_PixelClock SET", ret)

    # Exposure/gain/FPS must be set after camera init.
    ret = ueye.is_Exposure(
        hCam,
        ueye.IS_EXPOSURE_CMD_SET_EXPOSURE,
        exp_time,
        ueye.sizeof(exp_time)
    )
    check_ret("is_Exposure SET", ret)

    ret = ueye.is_SetHardwareGain(
        hCam,
        gain_factor,
        ueye.IS_IGNORE_PARAMETER,
        ueye.IS_IGNORE_PARAMETER,
        ueye.IS_IGNORE_PARAMETER
    )
    check_ret("is_SetHardwareGain", ret)

    ret = ueye.is_SetFrameRate(hCam, desired_fps, actual_fps)
    check_ret("is_SetFrameRate", ret)
    print("Requested FPS:", desired_fps.value)
    print("Actual FPS:", actual_fps.value)

     # Get AOI after camera init/reset.
    rectAOI = ueye.IS_RECT()
    ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))

    full_w = rectAOI.s32Width.value
    full_h = rectAOI.s32Height.value

    # Desired smaller AOI
    aoi_w = 4000
    aoi_h = 3004

    # aoi_w = 1024
    # aoi_h = 1024

    rectAOI.s32X = ueye.INT((full_w - aoi_w) // 2)
    rectAOI.s32Y = ueye.INT((full_h - aoi_h) // 2)
    rectAOI.s32Width = ueye.INT(aoi_w)
    rectAOI.s32Height = ueye.INT(aoi_h)

    nRet = ueye.is_AOI(
        hCam,
        ueye.IS_AOI_IMAGE_SET_AOI,
        rectAOI,
        ueye.sizeof(rectAOI)
    )

    print("Set AOI:", nRet)


    width = rectAOI.s32Width
    height = rectAOI.s32Height

    print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
    print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
    print("Image width:\t\t", width.value)
    print("Image height:\t\t", height.value)
    print()

    # Allocate image sequence buffers after color mode/AOI/settings.
    allocate_single_buffer()

    # Start live capture after buffers are in the sequence.
    # ret = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
    # check_ret("is_CaptureVideo", ret, fatal=True)

    print("\nPress q to leave the program")
    print("Press c to calibrate\n")


    # ---------------------------------------------------------------------
    # Graph setup
    # ---------------------------------------------------------------------

    figx = Figure(figsize=(12, 4), dpi=200)
    canvasx = FigureCanvas(figx)

    figy = Figure(figsize=(12, 4), dpi=200)
    canvasy = FigureCanvas(figy)

    x = np.arange(cross_hair_size)
    y = np.linspace(0, 20, cross_hair_size)

    axx = figx.gca()
    axx.axis('off')
    axisx, = axx.plot(x, y, 'b')

    axy = figy.gca()
    axy.axis('off')
    axisy, = axy.plot(x, y, 'b')

    # store the edge profiles of the last 5 frames
    yxn = np.zeros((cross_hair_size, 5)) 
    yyn = np.zeros((cross_hair_size, 5))

    # Initialize graph images so they exist before the first paste.
    canvasx.draw()
    graphimgx = np.asarray(canvasx.buffer_rgba())[..., :3].copy()

    canvasy.draw()
    graphimgy = np.rot90(np.asarray(canvasy.buffer_rgba())[..., :3]).copy()


    # ---------------------------------------------------------------------
    # Overlay setup
    # ---------------------------------------------------------------------

    cross = io.imread(r'bitmaps\biggercross.bmp')
    cross = cross[:, :, 0]
    cross = np.where(cross == 255, 1, 0).astype(np.uint8)
    icross = np.where(cross == 0, 1, 0).astype(np.uint8)
    zeros = np.zeros_like(cross, dtype=np.uint8)

    overlay_green = np.dstack((zeros, icross * 255, zeros))
    overlay_mask = np.dstack((cross, cross, cross))


    def calibrate(num_frames=20):
        global cal

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

            Larray += frame_f / num_frames

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

            Darray += frame_f / num_frames

        if Larray is None or Darray is None:
            print("Calibration failed: no valid frames")
            return None, None, None, None

        Lmean = np.mean(Larray)
        Dmean = np.mean(Darray)

        cal = 1
        print("Calibration finished")

        return Lmean, Dmean, Larray, Darray


    def correct(R, l, d, L, D):
        C = (R - D) * ((l - d) / (L - D)) + d
        return C.astype(np.uint8)


    # ---------------------------------------------------------------------
    # Main display loop
    # ---------------------------------------------------------------------

    i = 0

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
        # raw = np.reshape(array, (height.value, pitch.value))
        # frame = raw[:, :width.value]

        # cv2.imshow("raw frame", frame)
        frame2 = np.dstack((frame, frame, frame)) # turns the grayscale image into a 3-channel image

        # only recompute/redraw graphs every N frames.
        if i % GRAPH_UPDATE_EVERY == 0:
            h_mid = height.value // 2 # floor division
            w_mid = width.value // 2

            # smoothing? 
            yxm = np.squeeze(np.mean(frame[h_mid - 110:h_mid + 112, w_mid - 111:w_mid + 111], axis=0)) # squeeze eliminates empty dimensions, mean averages the array elements (along the 0th axis)
            yxp = np.squeeze(np.mean(frame[h_mid - 110:h_mid + 112, w_mid - 109:w_mid + 113], axis=0))

            yxn[:, 4] = yxn[:, 3]
            yxn[:, 3] = yxn[:, 2]
            yxn[:, 2] = yxn[:, 1]
            yxn[:, 1] = yxn[:, 0]
            yxn[:, 0] = np.absolute((yxp - yxm) / 2)
            yx = np.squeeze(np.mean(yxn, axis=1))

            yym = np.squeeze(np.mean(
                frame[h_mid - 111:h_mid + 111, w_mid - 110:w_mid + 112],
                axis=1
            ))
            yyp = np.squeeze(np.mean(
                frame[h_mid - 109:h_mid + 113, w_mid - 110:w_mid + 112],
                axis=1
            ))

            yyn[:, 4] = yyn[:, 3]
            yyn[:, 3] = yyn[:, 2]
            yyn[:, 2] = yyn[:, 1]
            yyn[:, 1] = yyn[:, 0]
            yyn[:, 0] = np.absolute((yyp - yym) / 2)
            yy = np.squeeze(np.mean(yyn, axis=1))

            axisx.set_ydata(yx)
            canvasx.draw()
            graphimgx = np.asarray(canvasx.buffer_rgba())[..., :3].copy()

            axisy.set_ydata(yy)
            canvasy.draw()
            graphimgy = np.rot90(np.asarray(canvasy.buffer_rgba())[..., :3]).copy()

            if os.path.isfile('xyrequest.npy'):
                time.sleep(0.1)
                a = np.load('xyrequest.npy')
                print(a)
                os.remove('xyrequest.npy')

                if a == 1:
                    np.save('xydata.npy', yx)
                elif a == 0:
                    np.save('xydata.npy', yy)

        # Paste graph images. These coordinates match your original full-size layout.
        x_graph_row0 = 0
        x_graph_row1 = min(800, frame2.shape[0])
        x_graph_col0 = int(width.value / 2) - 1200
        x_graph_col1 = int(width.value / 2) + 1200

        y_graph_row0 = int(height.value / 2) - 1200
        y_graph_row1 = int(height.value / 2) + 1200
        y_graph_col0 = frame2.shape[1] - 800
        y_graph_col1 = frame2.shape[1]

        # Clamp coordinates to image bounds.
        x_graph_col0 = max(0, x_graph_col0)
        x_graph_col1 = min(frame2.shape[1], x_graph_col1)

        y_graph_row0 = max(0, y_graph_row0)
        y_graph_row1 = min(frame2.shape[0], y_graph_row1)

        # Resize graph images to exactly match their destination slots.
        x_slot_h = x_graph_row1 - x_graph_row0
        x_slot_w = x_graph_col1 - x_graph_col0
        y_slot_h = y_graph_row1 - y_graph_row0
        y_slot_w = y_graph_col1 - y_graph_col0

        if x_slot_h > 0 and x_slot_w > 0:
            graphx_fit = cv2.resize(graphimgx, (x_slot_w, x_slot_h))
            frame2[x_graph_row0:x_graph_row1, x_graph_col0:x_graph_col1, :] = graphx_fit

        if y_slot_h > 0 and y_slot_w > 0:
            graphy_fit = cv2.resize(graphimgy, (y_slot_w, y_slot_h))
            frame2[y_graph_row0:y_graph_row1, y_graph_col0:y_graph_col1, :] = graphy_fit

        # Apply cross overlay.
        if overlay_mask.shape == frame2.shape:
            frame2 = frame2 * overlay_mask + overlay_green
        else:
            # If bitmap size does not match camera frame size, resize the overlay.
            mask_fit = cv2.resize(overlay_mask, (frame2.shape[1], frame2.shape[0]), interpolation=cv2.INTER_NEAREST)
            green_fit = cv2.resize(overlay_green, (frame2.shape[1], frame2.shape[0]), interpolation=cv2.INTER_NEAREST)
            frame2 = frame2 * mask_fit + green_fit

        frame2 = cv2.resize(frame2, (0, 0), fx=DISPLAY_SCALE, fy=DISPLAY_SCALE)

        cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame2)

        i += 1

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('c'):
            result = calibrate()
            if result[0] is not None:
                Lmean, Dmean, Larray, Darray = result

finally:
    cleanup()
    print("\nEND")