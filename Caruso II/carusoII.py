from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import serial
import time
from time import sleep
import numpy
import numpy as np
import scipy
import math
import os
import glob
import circle_fit
import cam2
import autofocus_stage

from scipy.signal import find_peaks

# find function codes for the HP 5508 on page 86 here: file:///O:/Code%20Repository/Caruso%20II/manuals%20and%20spec%20sheets/05528-90023%20service%20manual.pdf"
# find compumotor commands here: file:///O:/Code%20Repository/Caruso%20II/manuals%20and%20spec%20sheets/sx_srg_e.pdf

##### global variables #####
cX = 0	# Current Measurement
cY = 0
pX = 0	# Previous Measurement
pY = 0
zX = 0	# Zero Point
zY = 0
pA = 0	# Part Angle

motres = .000096  # compumotor resolution mm/step

autostate = 0 # this is 1 during an "automated" measurement while we are waiting for operator input to the UI controller

loopstate = 0
lcent = 0
ccent = 0

xint = 0
xslope = 0

mmpp = .00008955   # millimeters per image pixel

xfact = 0.9999972
yfact = 0.9999888

# edge detection options 
edge = 'e' # looks for 1 edge between a dark and light field: light field | dark field
line = 'l' # looks for the midpoint between two edges; the middle of a thin line: light field | dark field | light field
off = 'o' # operator is manually finding the edges

# Edge detection parameters
RETICLE_CENTER_OFFSET = 4.0
PEAK_PROMINENCE_FRACTION = 0.30
MIN_PEAK_DISTANCE = 20
CENTROID_WINDOW_RADIUS = 3
RETICLE_SIZE = 222
LOCAL_PEAK_PROMINENCE = 0.30

ser_laser = serial.Serial() # serial port to lasers
ser_motor = serial.Serial() # serial port to compumotors
ser_control = serial.Serial() # serial port to UI controller
laser_port = "COM4" # physical PC port
motor_port = "COM5"
control_port = "COM6"
BAUDRATE = 9600 # units are bits/sec, # of signal changes/s


x_address = b"++addr3\n" # GPIB address, x laser 
y_address = b"++addr5\n" # GPIB address, y laser

camoffset = [6.572,56.584] # distance from cam1 to cam2

# initialize the tkinter variables, the first 5 are for the radio button in the UI, the last 3 are for the X-Axis, Y-Axis and Distance readouts in the center of the UI, and also for populating the X, Y, Points and Distances boxes
def ui_variable_inits():
	## right side of the UI ##
	global camstate # low to high or high to low, which camera to switch to
	camstate = IntVar() 
	camstate.set(1)

	global unitstate # metric or english
	unitstate = IntVar()
	unitstate.set(1)
	####

	## bottom right box of the UI ##
	global axis_state 
	axis_state = StringVar()
	axis_state.set('x')
	
	global edge_detection_state # off/edge/line type of measurement to be made, only used for manual
	edge_detection_state = StringVar()
	edge_detection_state.set(edge)

	global pcdstate # point/center/distance type of measurement to be made, only used for manual
	pcdstate = IntVar()
	pcdstate.set(0)
	####

	## center 3 boxes of the UI ##
	global Xvar
	Xvar = StringVar()
	Xvar.set('000.00000')

	global Yvar
	Yvar = StringVar()
	Yvar.set('000.00000')

	global Dvar
	Dvar = StringVar()	# String to be displayed 
	Dvar.set('000.00000')
	####

# UI controller arrow keys
prev_up = 1
prev_down = 1
prev_left = 1
prev_right = 1


##### Serial Functions #####

# initialize and open the serial ports
def serial_init(serial_object, serial_name):

	# the compumotors and the UI controller have these parameters, the laser port is slightly different
	serial_object.baudrate = int(BAUDRATE)
	serial_object.parity = serial.PARITY_NONE
	serial_object.stopbits = 1
	serial_object.timeout = .1

	print(serial_name)
	if serial_name == "laser": 
		serial_object.bytesize = 7
		serial_object.parity = serial.PARITY_SPACE
		serial_object.port = laser_port
	# all the compumotor drives share the same serial port (daisy chain)
	elif serial_name == "motor": 
		serial_object.port = motor_port	
	elif serial_name == "control":
		serial_object.port = control_port
	else: 
		print("Serial " + serial_name + " not recognized")

	# print(serial_name + " is " + str(serial_object.is_open))
	serial_object.open()
	# print(serial_name + " is " + str(serial_object.is_open))

# clear the input and output buffers of the specified serial port	
def flush(ser):
	ser.reset_input_buffer() # discards all recieved data waiting in the input buffer
	ser.flush() # force all the data waiting in the output buffer to transmit
	ser.flushOutput() # i think this is older and redundant

# check if the specified port is open
def check_serial_status(serial_object, serial_name):
	if serial_object.is_open == False:
		serial_init(serial_object, serial_name)
	if serial_object.is_open == True:
		return
	else:
		print("couldn't open the serial port")

# send a command to the laser, return what is recieved back
def send_serial_command_laser(address, command):
	# ser_laser.write(bytes(address, 'utf-8')) # set up the GPIB connection to x-axis ? 
	ser_laser.write(address)
	# sleep(.05)
	flush(ser_laser)
	# sleep(.05)
	if command != "none":
		ser_laser.write(bytes(command + '\n', 'utf-8'))
	ser_laser.write(bytes("RC" + '\n', 'utf-8')) # record (output to HP-IB)
	w = 0
	# does this rlly have to be a while loop?
	while w == 0:
		a = ser_laser.readline()
		if a !=b'':
			try:
				a = a.decode('utf-8')
			except:
				messagebox.showinfo('Error:', 'Please press the reset button and retry measurement')
				return
			w = 1
	print("a: " + a)
	return a

# read serial messages from the specified port (laser or compumotor)
def read_data(serial_object):
	data = serial_object.readlines()
	i=0
	data_decode = ""
	while i < len(data):
		data_decode = data[i].decode('utf-8')
		i += 1
	return data_decode

# read serial messages from the UI controller
def read_data_controller():
	flush(ser_control)
	got_serial_response = False
	response = ''
	while got_serial_response == False:
		response = ser_control.readline()
		print(response[0:1]) 
		if response !=b'':
			# print(response)
			try:
				response_decode = response.decode('utf-8')
			except:
				return
			got_serial_response = True
	return response_decode

# just for testing, send a command to the motors from the gui
def send_serial_command(command):
	check_serial_status(ser_motor, "motor") # make sure the serial port is open
	ser_motor.write(bytes(command + '\n', "utf-8"))
	read_data(ser_motor)

# just for testing
def liza_test():

	# xydata = numpy.load("O:\\Code Repository\\Caruso II\\Caruso II\\xydata.npy") # edge data from the camera
	# edges = findedges(xydata)
	# program_file = "XYTEST.csv"
	program_file = "Diameter_Test.csv"
	measurepart(program_file, "12345", unitstate.get())

	"""
	check_serial_status(ser_laser)
	check_serial_status(ser_motor)
	check_serial_status(ser3)
	ser_motor.write(b'2XE100\n2XD100\n2"SINEC-Y-MOTOR2\n2LF\n2CR\n2SSJ0\n2SSI1\n2SN50\n2A1\n2AD1\n2V.2\n2D20\n2MN\n2MPA\n2MR15\n2LD3\n2SCR4\n2VAR10=0\n2XT\n')
	ser_motor.write(b'2XR100\n')

	ser_laser.write(b'++addr3\n')
	flush(ser_laser)
	ser_laser.write(b'RC\n')
	w = 0
	while w == 0:
		b = ser_laser.readlines()
		for i in range(len(b)):
			print(b[i].decode('utf-8'))
		w = 1

	ser_laser.write(b'++addr5\n')
	flush(ser_laser)
	ser_laser.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser_laser.readline()
		if a !=b'':
			try:
				a = a.decode('utf-8')
				print("a: " + a)
				a = -float(a)/2
			except:
				messagebox.showinfo('Error:', 'Please press the reset button and retry measurement')
				return
			w = 1
	
	
	read_data()
	"""

# init all the serial connections and start the UI controller loop
def init_serial_connections():
	print("initializing the serial connections")
	serial_init(ser_laser, "laser")
	serial_init(ser_motor, "motor")
	serial_init(ser_control, "control")

##### Lasers #####

# get the x and y positions from the lasers
def updatepos(r):
	global cX, cY, pX, pY, zX, zY, lcent # current x,y; previos x,y; zero x,y; ??
	pX = cX
	pY = cY

	# some better names than a and b PLZ
	a = send_serial_command_laser(x_address, "RC") # turn off auto record?
	a = -float(a)/2 # im not sure why but the distance displayed on the 5508A is doubled and negative relative to the value we want
	b = send_serial_command_laser(y_address, "RC") # turn off auto record?
	
	# idk what lcent is 
	if lcent == 1:
		b = (cX+b)/2
		a = (cY+a)/2
		lcent = 0

	cX = b
	cY = a

	Xvar.set(str(round(b,5)))
	Yvar.set(str(round(a,5)))

	if r == 1:
		# pointbox.insert(END,str(round(b,5)) + ',' + str(round(a,5)))
		# pointbox.insert(END,Xvar + ',' + Yvar)
		# reset the zeros?
		zX = b
		zY = a

	#print('zX:', zX, 'zY:',zY,'cX:',cX,'cY:',cY,'pX:',pX,'pY:',pY)
	return (b,a)


# vol = Velocity of Light, get/set the vol for both lasers and put in measurement mode
def vol():
	vol_y = send_serial_command_laser(y_address, "VL") # get the velocity of light compensation number, maybe check if this is the same for both x and y?
	print("voly: " + vol_y)
	vol_x = send_serial_command_laser(x_address, "VL") # get the velocity of light compensation number, maybe check if this is the same for both x and y?
	print("volx: " + vol_x)
	send_serial_command_laser(x_address, vol[:-2] + "VL") # set the velocity of light compensation number to match the y axis
	m1_resx = send_serial_command_laser(x_address, "M1") # measurement mode, response is the current measurement
	m1_resy = send_serial_command_laser(y_address, "M1") # measurement mode, response is the current measurement


# request the temperature, humidity, pressure and material data from the laser
def thp():
	temperature = send_serial_command_laser(x_address, "AT")
	print('Temperature:', temperature)
	humidity = send_serial_command_laser(x_address, "AH")
	print('Humidity:', humidity)
	pressure = send_serial_command_laser(x_address, "AP")
	print('Pressure:', pressure)
	material = send_serial_command_laser(x_address, "T1") # material temperature sensor #1
	print('Material:', material)
	Dvar.set(temperature + ',' + pressure + ',' + material) # not sure why we dont include humidity in this?

# returns the x and y laser measurements
def cupdate():
	flush(ser_laser)
	y_measurement = float(send_serial_command_laser(y_address, "none"))/(-2) # not sure why we halve and negate the y measurements
	flush(ser_laser)
	x_measurement = float(send_serial_command_laser(y_address, "none"))/(2) # not sure why we halve the x measurements
	return(x_measurement, y_measurement)

# reset both lasers and sets the resolution
def resetlaser():
	reset_res = send_serial_command_laser(y_address, "RS") # resets the laser (measurement goes to zero)
	print("reset_res: " + reset_res)
	disp_res = send_serial_command_laser(y_address, "5R1") # sets the distance display resolution to 5 decimal points
	print("disp_res: " + disp_res)
	reset_res = send_serial_command_laser(x_address, "RS") # resets the laser (measurement goes to zero)
	print("reset_res: " + reset_res)
	disp_res = send_serial_command_laser(x_address, "5R1") # sets the distance display resolution to 5 decimal points
	print("disp_res: " + disp_res)

##### Motors ##### 

# put the motors in position profile mode (im not clear on why we need to do this, to recieve async input from the controller?)
def motconfig():
	ser_motor.write(b'2SCR1\n2MC\n2H+\n2A6\n2AD6\n2V0\n2MPP\n2G\n')
	ser_motor.write(b'1SCR1\n1MC\n1H+\n1A6\n1AD6\n1V0\n1MPP\n1G\n')

# turn the controllers on
def motoron():
	ser_motor.write(b'1ON\n')
	ser_motor.write(b'2ON\n')

# turn the controllers off
def motoroff():
	ser_motor.write(b'1OFF\n')
	ser_motor.write(b'2OFF\n')

# update the states, scale by the angle, move the motors
def gotopoint(part_angle, x, y):
	global zX, zY, pA # x,y zeros, part angle
	cgtX, cgtY = updatepos(0) # get the position from the laser
	pA = float(part_angle)
	print('PA:', pA)
	gtX = float(x)
	gtY = float(y)

	# project the desired distance onto the actual angled part
	if pA != None:
		fX = zX + gtX*numpy.cos(pA) + gtY*numpy.sin(pA) - cgtX
		fY = zY + gtY*numpy.cos(pA) - gtX*numpy.sin(pA) - cgtY
	else:
		fX = zX - cgtX
		fY = zY - cgtY
	godist(fX, fY) # move the motors

# put the motors in absolute position mode, move the compumotors
def godist(x,y):
	#print(x,y)
	ld = numpy.amax([abs(int(y/motres)),abs(int(x/motres))])/50000 # dont think we use this?
	#print(ld)

	# configure the x-axis
	ser_motor.write(b'1MN\n1MPA\n1NG\n1A0.05\n1PZ\n1AD0.05\n1V2\n')
	ser_motor.write(bytes('1D' + str(int(x/motres)) + '\n','utf-8'))
	ser_motor.write(b'1G\n')

	# configure the y-axis
	ser_motor.write(b'2MN\n2MPA\n2NG\n2A0.05\n2PZ\n2AD0.05\n2V2\n')
	ser_motor.write(bytes('1D' + str(int(x/motres)) + '\n','utf-8'))
	ser_motor.write(b'2G\n')

	# was working on a better way to wait for the move to finish on the sine bench, this works for now tho
	ser_motor.reset_input_buffer()
	ser_motor.write(b'1"FIN1 \n')
	ser_motor.write(b'2"FIN2 \n')

	status1 = 0
	status2 = 0
	t1 = time.time()

	while status1 == 0 or status2 == 0:
		t2 = time.time()
		td = t2-t1
		lines = ser_motor.readlines()
		#print(lines, status1, status2)
		# time.sleep(0.1)
		rxline = ''
		for line in lines:
			try:
				rxline = line.decode('utf-8')
				#print('rxline:',rxline)

				rlin = rxline.split(' ')
				#print('rlin:',rlin)
				for lin in rlin:
					if lin == 'FIN1':
						status1 = 1
					if lin == 'FIN2':
						status2 = 1
			except:
				pass
		if 	td > 60:
			status1 = 1
			status2 = 1

	motconfig() # switch the position mode back

# switch which camera is being used (high or low mag)
def camswitch():
	cs = camstate.get()
	x = camoffset[0]*cs
	y = camoffset[1]*cs

	godist(x,y)

	camstate.set(camstate.get()*-1)

##### UI Controller #####
"""
def ctrlupdate(a):
	global loopstate, autostate, prev_up, prev_down, prev_left, prev_right
	a = a.split(',')
	# print(a)
	try:
		downSwitch = int(a[0])
		upSwitch = int(a[1])
		leftSwitch = int(a[2])
		rightSwitch = int(a[3])
		V1 = int(a[4])
		upArrow = int(a[5])
		downArrow = int(a[6])
		leftArrow = int(a[7])
		rightArrow = int(a[8])
		blue = int(a[9])
		yellow = int(a[10])
		red = int(a[11])
		green = int(a[12])
	except:
		return
	D = 0
	V = bytes(str(0), 'utf-8')
	if V1 == 9:
		ser2.write(b'k\n')
		D = 0
	elif V1 == 8:
		V = bytes(str(5), 'utf-8')
		D = 10
	elif V1 == 7:
		V = bytes(str(1), 'utf-8')
		D = 5
	elif V1 == 6:
		V = bytes(str(0.1), 'utf-8')
		D = 1
	elif V1 == 5:
		V = bytes(str(0.01), 'utf-8')
		D = 0.5

	elif V1 == 4:
		V = bytes(str(0.003), 'utf-8')
		D = 0.05
	elif V1 == 3:
		V = bytes(str(0.0015), 'utf-8')
		D = 0.005
	elif V1 == 2:
		V = bytes(str(0.0005), 'utf-8')
		D = 0.0005
	elif V1 == 1:
		V = bytes(str(0.0001), 'utf-8')
		D = 0.0001
	else:
		pass
		# sleep(.03)
	#V = bytes(str(V1), 'utf-8')
	if upSwitch == 0:
		if (prev_up == 1):
			ser2.write(b'2S\n')
		ser2.write(b'2H+\n')
		# sleep(.03)
		ser2.write(b'2V' + V + b'\n')
		# sleep(.03)
		ser2.write(b'2A' + V + b'\n')
		# sleep(.03)
		ser2.write(b'2AD' + V + b'\n')
		# sleep(.03)
		ser2.write(b'2G\n')
		# sleep(.03)
	if downSwitch == 0:
		if (prev_down == 1):
			ser2.write(b'2S\n')
		ser2.write(b'2H-\n')
		# sleep(.03)
		ser2.write(b'2V' + V + b'\n')
		# sleep(.03)
		ser2.write(b'2A' + V + b'\n')
		# sleep(.03)
		ser2.write(b'2AD' + V + b'\n')
		# sleep(.03)
		ser2.write(b'2G\n')
		# sleep(.03)
	if upSwitch == 1 and downSwitch == 1:
		ser2.write(b'2V0\n')
		# sleep(.03)
		ser2.write(b'2G\n')
	if leftSwitch == 0:
		if (prev_left == 1):
			ser2.write(b'1S\n')
		ser2.write(b'1H+\n')
		# sleep(.03)
		ser2.write(b'1V' + V + b'\n')
		# sleep(.03)
		ser2.write(b'1A' + V + b'\n')
		# sleep(.03)
		ser2.write(b'1AD' + V + b'\n')
		# sleep(.03)
		ser2.write(b'1G\n')
		# sleep(.03)
	if rightSwitch == 0:
		if (prev_right == 1):
			ser2.write(b'1S\n')
		ser2.write(b'1H-\n')
		# sleep(.03)
		ser2.write(b'1V' + V + b'\n')
		# sleep(.03)
		ser2.write(b'1A' + V + b'\n')
		# sleep(.03)
		ser2.write(b'1AD' + V + b'\n')
		# sleep(.03)
		ser2.write(b'1G\n')
		# sleep(.03)
	if leftSwitch == 1 and rightSwitch == 1:
		ser2.write(b'1V0\n')
		# sleep(.03)
		ser2.write(b'1G\n')

	if upArrow == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		godist(0,D)
	if downArrow == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		godist(0,-D)
	if leftArrow == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		godist(-D,0)
	if rightArrow == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		godist(D,0)
		
	if blue == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		camswitch()
	if yellow == 1:
		if edge_detection_state.get() ==2:
			centerpoint()
		else:
			pcdstate.set(1)
			mancpoint()
	if green == 1:
		print('edge_detection_state',edge_detection_state.get())
		if autostate == 1:
			autostate = 0
			return
		elif edge_detection_state.get() == 2:
			updatepos(1)
		else:
			pcdstate.set(0)
			mancpoint()
	if red ==1:
		if edge_detection_state.get() == 2:
			if loopstate == 1:
				loopstate = 0
			else:
				distdisp()
		else:
			pcdstate.set(2)
			mancpoint()

	prev_up = upSwitch
	prev_down = downSwitch
	prev_left = leftSwitch
	prev_right = rightSwitch

"""
# move the motors according to the input from the UI controller
def ctrlupdate(a):
	global loopstate, autostate
	a = a.split(',')
	# print(a)
	try:
		downSwitch = int(a[0])
		upSwitch = int(a[1])
		leftSwitch = int(a[2])
		rightSwitch = int(a[3])
		V1 = int(a[4])
		upArrow = int(a[5])
		downArrow = int(a[6])
		leftArrow = int(a[7])
		rightArrow = int(a[8])
		blue = int(a[9])
		yellow = int(a[10])
		red = int(a[11])
		green = int(a[12])
	except:
		return
	D = 0
	V = bytes(str(0), 'utf-8')
	if V1 == 9:
		ser_motor.write(b'k\n')
		D = 0
	elif V1 == 8:
		V = bytes(str(5), 'utf-8')
		D = 10
	elif V1 == 7:
		V = bytes(str(1), 'utf-8')
		D = 5
	elif V1 == 6:
		V = bytes(str(0.1), 'utf-8')
		D = 1
	elif V1 == 5:
		V = bytes(str(0.01), 'utf-8')
		D = 0.5

	elif V1 == 4:
		V = bytes(str(0.003), 'utf-8')
		D = 0.05
	elif V1 == 3:
		V = bytes(str(0.0015), 'utf-8')
		D = 0.005
	elif V1 == 2:
		V = bytes(str(0.0005), 'utf-8')
		D = 0.0005
	elif V1 == 1:
		V = bytes(str(0.0001), 'utf-8')
		D = 0.0001
	else:
		sleep(.03)
	#V = bytes(str(V1), 'utf-8')
	if upSwitch == 0:
		ser_motor.write(b'2H+\n')
		sleep(.03)
		ser_motor.write(b'2V' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'2A' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'2AD' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'2G\n')
		sleep(.03)
	if downSwitch == 0:
		ser_motor.write(b'2H-\n')
		sleep(.03)
		ser_motor.write(b'2V' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'2A' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'2AD' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'2G\n')
		sleep(.03)
	if upSwitch == 1 and downSwitch == 1:
		ser_motor.write(b'2V0\n')
		sleep(.03)
		ser_motor.write(b'2G\n')
	if leftSwitch == 0:
		ser_motor.write(b'1H+\n')
		sleep(.03)
		ser_motor.write(b'1V' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'1A' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'1AD' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'1G\n')
		sleep(.03)
	if rightSwitch == 0:
		ser_motor.write(b'1H-\n')
		sleep(.03)
		ser_motor.write(b'1V' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'1A' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'1AD' + V + b'\n')
		sleep(.03)
		ser_motor.write(b'1G\n')
		sleep(.03)
	if leftSwitch == 1 and rightSwitch == 1:
		ser_motor.write(b'1V0\n')
		sleep(.03)
		ser_motor.write(b'1G\n')

	if upArrow == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		godist(0,D)
	if downArrow == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		godist(0,-D)
	if leftArrow == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		godist(-D,0)
	if rightArrow == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		godist(D,0)
		
	if blue == 1 and (leftSwitch + rightSwitch + downSwitch + upSwitch) == 4:
		camswitch()
	if yellow == 1:
		if edge_detection_state.get() == off:
			centerpoint()
		else:
			pcdstate.set(1)
			mancpoint()
	if green == 1:
		print('edge_detection_state',edge_detection_state.get())
		if autostate == 1:
			autostate = 0
			return
		elif edge_detection_state.get() == off:
			updatepos(1)
		else:
			pcdstate.set(0)
			mancpoint()
	if red ==1:
		if edge_detection_state.get() == off:
			if loopstate == 1:
				loopstate = 0
			else:
				distdisp()
		else:
			pcdstate.set(2)
			mancpoint()

##### Camera #####

# method for coordinating the kdc101 -> z925b -> xrn25x and the camera to focus the camera
def autofocus():
	print("not ready yet :(((((((")
	
	# decide which direction to move by moving a bit up then a bit down and checking which is better


# decide which direction to move the camera stage by moving a bit up then a bit down and checking which is better
def find_focus_dir():
	x_peak, y_peak = cam2.get_peak()
	one_turn = 0.05 # mm, one turn of the manual focus stage was 50um
	# the move method is relative, can be switched to absolute if that is prefered tho
	autofocus_stage.move(one_turn/4) # move the stage a bit down
	x_peak_down, y_peak_down = cam2.get_peak()
	autofocus_stage.move(-one_turn/2) # move the stage a bit up
	x_peak_up, y_peak_up = cam2.get_peak()
	



##### UI updates #####

# display the distance between the current and previous location in the GUI distance box
def distdisp():
	global cX, cY, pX, pY, zX, zY, lcent

	if lcent == 1:
		a = zX
		b = zY
		c ,d = updatepos(0)
		lcent = 0
		e = (((c-a)*xfact)**2 + ((d-b)*yfact)**2)**.5
		#print('zX:', zX, 'zY:',zY,'cX:',cX,'cY:',cY,'pX:',pX,'pY:',pY,'c',c,'d',d)
	else:
		updatepos(0)
		a = cX-zX
		b = cY-zY
		e = ((a*xfact)**2 + (b*yfact)**2)**.5
	units = unitstate.get()
	if units == 1:
		# distbox.insert(END,str(round(e,5)))
		Dvar.set(str(round(e,5)))
	else:
		# distbox.insert(END,str(round(e/25.4,6)))
		Dvar.set(str(round(e/25.4,6)))

# calculate the part angle
def calculate_angle():
	global pA
	pA = -numpy.arctan((cY-pY)/(cX-pX))
	return pA
	
##### Measurement Routine #####

# make the measurement file
def measurepart(program_file, serial_num, units):
	
	# sort the points in the program file
	points, midpoints, meas, diam, circle_centers = parsepart(program_file)
	edge_locs = {} # dictionary -> name : [edge_location_x, edge_location_y]
	dmeas = {}

	print('points:',points)
	print('midpoints:', midpoints)
	print('meas:', meas)
	print('circle_centers:', circle_centers)

	# for each of the circles to be measured, and the add the top, bottom, left and right to the list of points 
	for i in range(len(circle_centers)):
		circle_params = circle_centers[i][1:] # each circle point line of the file, but without the first column, ex. just (X-loc),(Y-loc),(Radius)
		print("circle_params")
		print(circle_params)
		name = circle_centers[i][0] # first column, ex. just X#
		x_c = float(circle_params[0]) # (X-loc)
		print("x_c: " + str(x_c))
		y_c = float(circle_params[1]) # (Y-loc)
		print("y_c: " + str(y_c))
		r = float(circle_params[2]) # (Radius)
		print("r: " + str(r))
		# if an edge detection method is specified, it will be in the 4th column of the program
		try:
			edge_detection_mode = circle_params[3]
		except: 
			edge_detection_mode = edge # default edge detection method

		# add the top, bottom, left and right of the circle to the list of points 
		# i think x1, x2, y1, y2 is just a way to identify the points by which axis is being used to measure
		points.append([name + 'x1', str(x_c - r), str(y_c),'x', edge_detection_mode])
		points.append([name + 'x2', str(x_c + r), str(y_c),'x', edge_detection_mode])
		points.append([name + 'y1', str(x_c), str(y_c - r),'y', edge_detection_mode])
		points.append([name + 'y2', str(x_c), str(y_c + r),'y', edge_detection_mode])

	# find an edge for every point
	for i in range(len(points)):
		print(points[i])
		edge_loc_x, edge_loc_y = autocpoint(points[i])
		print("edge_loc_x")
		print(edge_loc_x)
		print("edge_loc_y")
		print(edge_loc_y)
		edge_locs.update({points[i][0]:[edge_loc_x, edge_loc_y]})

	print("edge_locs: ")
	print(edge_locs)

	edge_values = list(edge_locs.values())
	

	# fit each set of four edges found at points around a circle to a circle function, rotate the circle by the part angle about the origin and update the circle array, diameter dictionary and point dictionary
	circle_meas = []
	for i in range(len(circle_centers)):

		edgedata = numpy.zeros((4,2))
		print("just values: ")
		print(edge_values[i:i+8])
		# i have no idea what this is for, what do the x1 x2 y1 y2 mean??
		edgedata[0,0] = edge_locs[circle_centers[i][0] + 'x1'][0]
		edgedata[0,1] = edge_locs[circle_centers[i][0] + 'x1'][1]
		edgedata[1,0] = edge_locs[circle_centers[i][0] + 'x2'][0]
		edgedata[1,1] = edge_locs[circle_centers[i][0] + 'x2'][1]
		edgedata[2,0] = edge_locs[circle_centers[i][0] + 'y1'][0]
		edgedata[2,1] = edge_locs[circle_centers[i][0] + 'y1'][1]
		edgedata[3,0] = edge_locs[circle_centers[i][0] + 'y2'][0]
		edgedata[3,1] = edge_locs[circle_centers[i][0] + 'y2'][1]
		
		# fit a circle to edgedata
		xc, yc, r, sigma = circle_fit.least_squares_circle(edgedata) # i think .least_squares_circle might be out of date, update to .standardLSQ()?
		D = r*2 

		# rotate the circle about the origin
		xtc = xc*numpy.cos(pA) - yc*numpy.sin(pA)
		ytc = yc*numpy.cos(pA) + xc*numpy.sin(pA)

		# populate the arrays and dictionaries
		circle_meas.append([circle_centers[i][0], xtc, ytc])
		dmeas.update({'D' + circle_centers[i][0]: D})
		edge_locs.update({'P' + circle_centers[i][0]:[xtc,ytc]})

	print('edgedata')
	print(edgedata)

	# 
	for i in range(len(midpoints)):
		x1 = edge_locs[midpoints[i][1]][0]
		y1 = edge_locs[midpoints[i][1]][1]
		x2 = edge_locs[midpoints[i][2]][0]
		y2 = edge_locs[midpoints[i][2]][1]

		x3 = (x1 + x2)/2
		y3 = (y1 + y2)/2

		edge_locs.update({midpoints[i][0]:[x3,y3]})

	print("midpoints: ")
	print(midpoints)

	cmeas = []
	for i in range(len(meas)):
		x1 , y1 = edge_locs[meas[i][1]]
		x2 , y2 = edge_locs[meas[i][2]]

		D = (((x1-x2)*xfact)**2 + ((y1-y2)*yfact)**2)**0.5

		cmeas.append([meas[i][0], D])

	print("cmeas: ")
	print(cmeas)

	units = unitstate.get()
	# file2 = 'completed/' + file[:-4] + '-' + sn + '.csv'
	measurement_file = "S:\\Caruso II\\"  + program_file[:-4] + '-' + serial_num + '.csv'

	if os.path.isfile(measurement_file):
		with open(measurement_file, 'a') as doc:
			# COMMENT THIS BACK IN for actual testing/production
			"""
			temp = simpledialog.askstring(title = "Temperature", prompt="Enter Temperature in Degrees F" )
			humid = simpledialog.askstring(title = "Humidity", prompt="Enter Humidity in %RH")
			press = simpledialog.askstring(title = "Pressure", prompt="Enter Pressure in mbar")
			doc.write('Temperature,Humidity,Pressure,\n' + temp + ',' + humid + ',' + press + ',\n')
			doc.write('Measurement,Distance,\n')
			"""
			for i in range(len(cmeas)):
				if units == 1:
					doc.write(str(cmeas[i][0]) + ',' + str(round(cmeas[i][1],5)) + ',\n')
				else:
					doc.write(str(cmeas[i][0]) + ',' + str(round(cmeas[i][1]/25.4,6)) + ',\n')

			for i in range(len(dmeas)):
				if units == 1:
					doc.write(str(diam[i]) + ',' + str(round(dmeas[diam[i]],5)) + ',\n')
				else:
					doc.write(str(diam[i]) + ',' + str(round(dmeas[diam[i]]/25.4,6)) + ',\n')

			doc.close()

	else:
		with open(measurement_file, 'w') as doc:
			# COMMENT THIS BACK IN for actual testing/production
			"""
			temp = simpledialog.askstring(title = "Temperature", prompt="Enter Temperature in Degrees F" )
			humid = simpledialog.askstring(title = "Humidity", prompt="Enter Humidity in %RH")
			press = simpledialog.askstring(title = "Pressure", prompt="Enter Pressure in mbar")
			doc.write('Temperature,Humidity,Pressure,\n' + temp + ',' + humid + ',' + press + ',\n')
			doc.write('Measurement,Distance,\n')
			"""
			for i in range(len(cmeas)):
				if units == 1:
					doc.write(str(cmeas[i][0]) + ',' + str(round(cmeas[i][1],5)) + ',\n')
				else:
					doc.write(str(cmeas[i][0]) + ',' + str(round(cmeas[i][1]/25.4,6)) + ',\n')

			for i in range(len(diam)):
				if units == 1:
					doc.write(str(diam[i]) + ',' + str(round(dmeas[diam[i]],5)) + ',\n')
				else:
					doc.write(str(diam[i]) + ',' + str(round(dmeas[diam[i]]/25.4,6)) + ',\n')

			for i in range(len(circle_meas)):
				if units == 1:
					doc.write(str(circle_meas[i][0]) + ',' + str(round(circle_meas[i][1],5)) + ',' + str(round(circle_meas[i][2],5)) + ',\n')
				else:
					doc.write(str(circle_meas[i][0]) + ',' + str(round(circle_meas[i][1]/25.4,6)) + ',' + str(round(circle_meas[i][2]/25.4,6)) +  ',\n')

			doc.close()
	time.sleep(1)
	# os.system(measurement_file)
	# autoframe.configure(style = 'TFrame')

# parse the program for a part into the different types of points
def parsepart(file):
	file = "S:\\Caruso II\\parts\\" + file # file with the points on the part to locate, + other info
	points = [] # written in the program as: P(#),(X-loc),(Y-loc),(measurement direction),(edge detection method), these points will be along the same line so no 2D measurement is needed
	midpoints = [] # written in the program as: C(#),P(#),P(#), midpoints between two points (P)
	meas = [] # written in the program as: M(#),P(#),P(#), distance between two points (P) or midpoints (C)
	diam = [] # written in the program as: D(X(#)), diameter of a circle measurements
	circle_centers = [] # written in the program as: X(#),(X-loc),(Y-loc),(Radius), center point of a circle

	# open the file, split it by the commas, sort the points, return the arrays
	with open(file,'rb') as lines:

		for line in lines:
			print("line: ")
			print(line)
			line = line.decode('utf-8-sig', 'ignore')
			a = line.split(',')

			if a[0][0] == 'P':
				points.append(a)

			if a[0][0] == 'C':
				midpoints.append(a)

			if a[0][0] == 'M':
				meas.append(a)

			if a[0][0] == 'D':
				diam.append(a[0])

			if a[0][0] == 'X':
				circle_centers.append(a)

	return(points, midpoints, meas, diam, circle_centers)

# pass in a whole line from the program, return the position of the edge				
def autocpoint(mline):
	global autostate, pY, pX, cY, cX
	print("mline: ")
	print(mline)
	X = float(mline[1])
	Y = float(mline[2])
	axis = mline[3] 
	edge_detection_mode = mline[4] # edge detection method
	# autoframe.configure(style = 'red.TFrame') # about to move the compumotors, turn the top of the UI red
	# Tk.update_idletasks(root)
	# Tk.update(root) # update the UI
	##### COMMENT THIS BACK IN for actual testing/production #####
	"""
	# VERY unclear to me why we do this three times??? is this why james has to press the green button three times?
	for i in range(3):
		gotopoint(pA, X, Y)
	# configure the frame
	if edge_detection_mode == off:
		autoframe.configure(style = 'yellow.TFrame') # the yellow frame tells the user that the operator needs to find the edge
	else:
		autoframe.configure(style = 'green.TFrame') # the green frame tells the user to press the green button
	Tk.update_idletasks(root)
	Tk.update(root) # update the UI
	autostate = 1 # think this keeps track of whether we need the operator to do smth with the UI controller
	# wait for the operator to do something with the UI controller
	while autostate == 1:
		a = read_data(ser_control)
		ctrlupdate(a)
	"""
	# load the camera data and find the edge location(s)
	try:
		edges = getedges(axis)
	except:
		pass
		messagebox.showinfo(message = 'Check XY Edge Orientation')
		return
	# get the current x,y measurement
	##### COMMENT THIS BACK IN #####
	lx, ly = cupdate() 
	# lx, ly =  0.00012, 0.00065

	# find the correct edge location based on the edge detection method
	edge_select = 0
	if edge_detection_mode == edge:  # or edge_detection_mode == 0:
		edge_select = corredgefind(edges)

	if edge_detection_mode == line: # or edge_detection_mode == 1:
		edge_select = linecenter(edges)

	if edge_detection_mode == off: # or edge_detection_mode == 2:
		edge_select = 0

	# dk if im misinterpreting this, but why are we updating the current x and y if we arent moving the motors?
	if axis == 'x':  # or axis == 1:
		cx = lx + edge_select
		cy = ly

	if axis == 'y': # or xy ==0:
		cx = lx
		cy = ly - edge_select

	print("edge select: ")
	print(edge_select)

	pX = cX
	pY = cY

	cX = cx
	cY = cy

	return(cx, cy)

# curve fit function, called when we are finding the edges
# a is the max of the data, b is the x position of the mean of the data, c is the std dev
def gaussfunc(x,a,b,c):
	return(a*numpy.exp(-((x-b)**2)/(2*c**2)))

def findedges(edge_data:np.ndarray) -> list[float]:
	"""
	Function which finds the strongest (global maxima) edges from 1D profile
	Edge locations are estimated with sub-pixel accuracy

	Args:
		edge_data (np.ndarray): Return value from `set_edge_profiles()`

	Returns:
		list[float]: Edge locations in [mm] relative to the reticle center.
	"""
	# Position of each sample relative to the reticle center.
	sample_positions = (
		np.arange(edge_data.size)
		- edge_data.size / 2
		+ RETICLE_CENTER_OFFSET  # Calibration offset.
	)

	# Detect prominent peaks while suppressing noise and duplicate detections.
	peak_indices, _ = find_peaks(
		edge_data,
		prominence=LOCAL_PEAK_PROMINENCE * edge_data.max(),
		distance=MIN_PEAK_DISTANCE ,
	)

	# Scan local peaks, filtering via absolute threshold criteria 
	edge_locations = []
	for peak_index in peak_indices:
     
		# Extract a small neighborhood left/right of peak
		# + profile boundary clipping
		window_start = max(0, peak_index - CENTROID_WINDOW_RADIUS)
		window_end = min(edge_data.size, peak_index + CENTROID_WINDOW_RADIUS + 1)

		window = sample_positions[window_start:window_end]
		window_averaging_weights = edge_data[window_start:window_end]

		# Intensity-weighted centroid for sub-pixel localization
		# 	i.e. consult the pixels in a small area around the peak, 
		# 	     with most of the focus around the center
		if window_averaging_weights.sum() > 0:
			edge_position = np.average(
				window,
				weights=window_averaging_weights,
			)
   
		# Just grab the peak, no avg
		else:
			edge_position = sample_positions[peak_index]

		# Convert edge position to [mm] using conversion constant
		edge_locations.append(edge_position * mmpp)

	return edge_locations

# called if edge_detection_mode option is edge
# if findedges returns the locations of edges, its unclear to me why if there were multiple that got through the filtering process, why we would choose the one with the smaller location? am i interpreting this wrong? GMT? 
def corredgefind(locs):
	cpos = locs[numpy.argmin(numpy.abs(locs))]
	print('cpos',cpos)
	return cpos

# called if edge_detection_mode option is line: light field | dark field | light field
# again, why are we choosing the smaller location? is the idea that there are many lines in a row, so we're detecting the left most one first bc the next measurement will be of the next one?
# also, the way we choose the two edges to find the center of seems crazy to me, why dont we just find the adjacent one in the array? GMT?
def linecenter(locs):
	c = locs[numpy.argmin(numpy.abs(locs))]
	locs[numpy.argmin(numpy.abs(locs))] = 1
	d = locs[numpy.argmin(numpy.abs(locs))]

	e = (c+d)/2 # average the edge locations to find the center of the line
	print('c', c, 'd', d, 'e', e)
	return(e)

# save the axis we want to measure, load the edge data from the camera, call findedges to find edge locations
def getedges(axis):
	# save which axis we are measuring so cam1.py or cam2.py can read it
	numpy.save('xyrequest.npy', numpy.array([axis])) 
	w = 0
	while w == 0:
		if  os.path.isfile('xydata.npy'):
			# time.sleep(1)
			xydata = numpy.load('xydata.npy') # edge data from the camera
			# os.remove('xydata.npy')
			w = 1
	# find the location of the edges
	edges = findedges(xydata)
	return(edges)


# dont rlly know the difference between this and mancpoint
def cpoint(xy,edge_detection_mode):
	try:
		edges = getedges(xy)
	except:
		pass
		messagebox.showinfo(message = 'Check XY Edge Orientation')
		return

	print(edges, edge_detection_mode)
	lx, ly = cupdate()
	if edge_detection_mode == edge: # or edge_detection_mode == 0:
		edge = corredgefind(edges)

	if edge_detection_mode == line: # or edge_detection_mode == 1:
		edge = linecenter(edges)

	if edge_detection_mode == off:
		edge = 0


	if xy == 'x' or xy == 1:
		cx = lx + edge
		cy = ly

	if xy == 'y' or xy ==0:
		cx = lx
		cy = ly - edge

	print(edge)
	return(cx, cy)


# dont rlly know the difference between this and cpoint
def mancpoint():
	global cX, cY, pX, pY, zX, zY, lcent, ccent
	try:
		xyn = xystate.get()
		edge_detection_mode = edge_detection_state.get()
		print('xyn', xyn, 'edge_detection_mode',edge_detection_mode)

		X, Y = cpoint(xyn, edge_detection_mode)

		pX = cX
		pY = cY

		pcd = pcdstate.get()
		print('pcd', pcd)

		if pcd == 0:
			Xvar = str(round(X,5))
			Yvar = str(round(Y,5))
			# pointbox.insert(END,str(round(X,5)) + ',' + str(round(Y,5)))
			zX = X
			zY = Y
			a = Y
			b = X

		elif pcd == 1:
			a = Y
			b = X
			ccent = 1


		elif pcd == 2:
			if ccent == 1:
				b = (cX+X)/2
				a = (cY+Y)/2
				lcent = 0
				e = (((zX-a)*xfact)**2 + ((zY-b)*yfact)**2)**.5
				#print('zX:', zX, 'zY:',zY,'cX:',cX,'cY:',cY,'pX:',pX,'pY:',pY,'c',c,'e',e)
			else:
				b = X-zX
				a = Y-zY
				e = ((a*xfact)**2 + (b*yfact)**2)**.5
			units = unitstate.get()
			if units == 1:
				# distbox.insert(END,str(round(e,5)))
				Dvar.set(str(round(e,5)))
			else:
				# distbox.insert(END,str(round(e/25.4,6)))
				Dvar.set(str(round(e/25.4,6)))

		cX = b
		cY = a
	except TypeError:
		pass 


def centerpoint():
	global lcent
	updatepos(0)
	lcent = 1










##### Miscellaneous #####

# dont think we ever call this ??
"""
def partaxis():
	global loopstate, xslope, xint
	loopstate = 1
	if messagebox.askokcancel('Part Axis Config','All current points will be deleted!'):
		pointbox.delete(0,END)
	else:
		return

	messagebox.showinfo('Part Axis Config','Select several positions along X-Axis of part')
	
	while loopstate == 1:
		
		curstr = getinputs()
		if currstr != prevstr:
			ctrlupdate(currstr)
		prevstr = currstr

		Tk.update_idletasks(root)
		Tk.update(root)
	size = pointbox.size()
	x = numpy.zeros(size)
	y = numpy.zeros(size)
	for i in range(size):
		point = pointbox.get(i)
		xstr, ystr = pointbox.split(',')
		x[i] = float(xstr)
		y[i] = float(ystr)

	xslope, xint, xr, xp, xstd = scipy.stats.linregress(x,y)
"""

# don't think this gets used
"""
def autopoints(points):
	pmeas = {}
	for i in range(len(points)):
		X = mline[1]
		Y = mline[2]
		xy = mline[3]
		el = mline[4]
		godist(X,Y)
"""

#Measure both sides of 2 lines to find the distance between their centers
# def linedistance():
# 	messagebox.showinfo('Line Center Distance Measurement','Measure both sides of 2 lines to find the distance between their centers')

# 	Da, ya, xa, a, b = edgedistance()

# 	Db, yb, xb, c, d = edgedistance()

# 	D = abs(c*xa-ya+d)/(c**2 + 1)**.5

# 	distbox.delete(END)
# 	distbox.delete(END)

# 	units = unitstate.get()
# 	if units == 1:
# 		distbox.insert(END,str(round(e,5)))
# 	else:
# 		distbox.insert(END,str(round(e/25.4,6)))


# #Measure Distance Between 2 edges
# def edgedistance():
# 	global loopstate
# 	loopstate = 1
# 	if messagebox.askokcancel('Edge Distance Measurement','Measure the distance between 2 edges.\nAll current points will be deleted!\n Press cancel and save current points if needed!'):
# 		pointbox.delete(0,END)
# 	else:
# 		return

# 	messagebox.showinfo('Edge Distance Measurement','Select several positions along 1st edge')
	
# 	#Enter special tkinter loop. Then accumulate points into point box. Then parse out the points into linear regression.
# 	while loopstate == 1:
		
# 		curstr = getinputs()
# 		if currstr != prevstr:
# 			ctrlupdate(currstr)
# 		prevstr = currstr

# 		Tk.update_idletasks(root)
# 		Tk.update(root)
# 	size = pointbox.size()
# 	x = numpy.zeros(size)
# 	y = numpy.zeros(size)
# 	for i in range(size):
# 		point = pointbox.get(i)
# 		xstr, ystr = pointbox.split(',')
# 		x[i] = float(xstr)
# 		y[i] = float(ystr)

# 	a, b, y1r, y1p, y1std = scipy.stats.linregress(x,y)

# 	#Find average X = xa then use line equation to find corresponding ya on the line. Use reciprical
# 	#calculation for vertical lines
# 	if abs(a)<=1:
# 		xa = numpy.average(x)
# 		ya = a*xa + b
# 	else:
# 		ya = numpy.average(y)
# 		xa = (ya - b)/a

# 	pointbox.delete(0,END)
# 	loopstate = 1
# 	messagebox.showinfo('Line Distance Measurement','Select several positions along 2nd edge')
# 	#Enter special tkinter loop. Then accumulate points into point box. Then parse out the points into linear regression.
# 	while loopstate == 1:
		
# 		curstr = getinputs()
# 		if currstr != prevstr:
# 			ctrlupdate(currstr)
# 		prevstr = currstr

# 		Tk.update_idletasks(root)
# 		Tk.update(root)
# 	size = pointbox.size()
# 	x = numpy.zeros(size)
# 	y = numpy.zeros(size)
# 	for i in range(size):
# 		point = pointbox.get(i)
# 		xstr, ystr = pointbox.split(',')
# 		x[i] = float(xstr)
# 		y[i] = float(ystr)

# 	c, d, y1r, y1p, y1std = scipy.stats.linregress(x,y)

# 	#Calculate distance using point from previous line and line equation of current line.
# 	D = abs(c*xa-ya+d)/(c**2 + 1)**.5

# 	pointbox.delete(0,END)

# 	#Check for parallelism > 0.5 degrees
# 	if (numpy.atan2(a) - numpy.atan2(c)) > (numpy.pi/360):
# 		if messagebox.askokcancel('Warning!','Lines are not parallel! Would you like to record measurement anyway?'):
# 			distbox.insert(END,str(round(D,5)))
# 	else:
# 		units = unitstate.get()
# 		if units == 1:
# 			distbox.insert(END,str(round(e,5)))
# 		else:
# 			distbox.insert(END,str(round(e/25.4,6)))

# 	xb = numpy.average(x)
# 	yb = numpy.average(y)

	
# 	#Calculate Average slope and intercept to obtain center line
# 	aslope = (a+c)/2
# 	aint = (c+d)/2



# 	if (a/abs(a)) != (c/abs(c)) and abs(a)>1:
# 		aslope = numpy.tan(numpy.average((numpy.atan2(a),numpy.atan2(c))))

# 	if aslope<=1:
# 		ax = (xa + xb)/2
# 		ay = aslope*ax + aint

# 	if aslope>1:
# 		ay = (ya + yb)/2
# 		ax = (ay + aint)/aslope

# 	return(D, ay, ax, aslope, aint)	

