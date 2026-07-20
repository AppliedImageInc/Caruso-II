from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import serial
import time
import numpy
import scipy
import math
import pyautogui
import openpyxl

version = "Caruso II Rev 1.00.00"

#Densitometer Workstation rev 1.00.00 - Caruso II UI

root = Tk()
try:
	root.iconbitmap('caruso.ico')
except:
	pass
root.title(version)
# root.style = ttk.Style()
# root.style.theme_use("clam")


########### Define/Set Tkinter Variables #############

Xvar = StringVar()
Yvar = StringVar()
Dvar = StringVar()	#Density String to be displayed
# instvar = IntVar()		#Selects Instrument
# wl938 = IntVar()		#Selects Wavelength (Currently Only 660nm)
# filter518 = IntVar()	#Selects Color Filter / ND
# avgvar = IntVar()		#Slects number of measurements to average
# meas = IntVar()
# mleft = StringVar()
# advtype = StringVar()

Xvar.set('000.00000')
Yvar.set('000.00000')
Dvar.set('000.00000')

cX = 0
cY = 0
pX = 0
pY = 0

motres = .000096  #mm/step

camstate = 1
loopstate = 0

ser1 = serial.Serial()
ser2 = serial.Serial()
ser3 = serial.Serial()

xslope = 0

camoffset = [45.77,29.17] 		#From Aux to Main 

######### Program Functions #############

def serinitXY(): #Initialize serial connection
	try:
		ser1.port = 'COM4'
		ser1.baudrate = 9600
		ser1.bytesize = 7
		ser1.parity = serial.PARITY_SPACE
		ser1.stopbits = 1
		ser1.timeout = .1
		ser1.open()
	except:
		messagebox.showinfo('Failed to Connect to X-Axis')




def serinitMOT(): #Initialize serial connection
	try:
		ser2.port = 'COM5'
		ser2.baudrate = 9600
		ser2.parity = serial.PARITY_NONE
		ser2.stopbits = 1
		ser2.timeout = .1
		ser2.open()
	except:
		messagebox.showinfo('Failed to Connect to Motors')





def serinitCON(): #Initialize serial connection
	try:
		ser3.port = 'COM5'
		ser3.baudrate = 9600
		ser3.parity = serial.PARITY_NONE
		ser3.stopbits = 1
		ser3.timeout = .1
		ser3.open()
	except:
		messagebox.showinfo('Failed to Connect to Controller')

def motconfig():
	ser2.write(b'2H+\n')
	sleep(.01)
	ser2.write(b'2A4\n')
	sleep(.01)
	ser2.write(b'2AD10\n')
	sleep(.01)
	ser2.write(b'2V0\n')
	sleep(.01)
	ser2.write(b'2MPP\n')
	sleep(.01)
	ser2.write(b'2G\n')
	sleep(.01)
	ser2.write(b'1H+\n')
	sleep(.01)
	ser2.write(b'1A4\n')
	sleep(.01)
	ser2.write(b'1AD10\n')
	sleep(.01)
	ser2.write(b'1V0\n')
	sleep(.01)
	ser2.write(b'1MPP\n')
	sleep(.01)
	ser2.write(b'1G\n')
	sleep(.01)
	
def flush1():
	ser1.reset_input_buffer()
	ser1.flush()
	ser1.flushOutput()


def flush2():
	ser2.reset_input_buffer()
	ser2.flush()
	ser2.reset_output_buffer()


def flush3():
	ser3.reset_input_buffer()
	ser3.flush()
	ser3.reset_output_buffer()

def partaxis():
	global loopstate, xslope
	loopstate = 1
	if messagebox.askokcancel('Part Axis Config','All current points will be deleted!')
		pointbox.delete(0,END)
	else:
		return

	messagebox.showinfo('Part Axis Config','Select several positions along X-Axis of part')
	
	while loopstate = 1:
		
		curstr = getinputs()
		if currstr != prevstr:
			ctrlupdate(currstr)
		prevstr = currstr



		Tk.update_idletasks(root)
		Tk.update(root)
	size = pointbox.size()
	x = numpy.zeros(size)
	y = numpy.zeros(size)
	for i in range(size)
		point = pointbox.get(i)
		xstr, ystr = pointbox.split(',')
		x[i] = float(xstr)
		y[i] = float(ystr)

	xslope, xint, xr, xp, xstd = scipy.stats.linregress(x,y)




def updatepos():
	pX = cX
	pY = cY
	ser1.write(b'++addr5\n')
	sleep(.05)
	flush1()
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readlines()
		if a !=b'':
			a = a.decode('utf-8')
			a = float(a)/2
			w = 1
	
	ser1.write(b'++addr3\n')
	sleep(.05)
	flush1()
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		b = ser1.readlines()
		if b !=b'':
			b = float(b)/2
			w = 1

	Xvar.set(str(round(b,5)))
	Yvar.set(str(round(a,5)))

	pointbox.insert(str(round(b,5)) + ',' + str(round(a,5)))

	Cx = b
	Cy = a


	return (b,a)

def getpos():
	pX = cX
	pY = cY
	ser1.write(b'++addr5\n')
	sleep(.05)
	flush1()
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readlines()
		if a !=b'':
			a = a.decode('utf-8')
			a = float(a)/2
			w = 1
	
	ser1.write(b'++addr3\n')
	sleep(.05)
	flush1()
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		b = ser1.readlines()
		if b !=b'':
			b = float(b)/2
			w = 1

	Xvar.set(str(round(b,5)))
	Yvar.set(str(round(a,5)))

	Cx = b
	Cy = a


	return (b,a)

def getinputs():
	flush3()
	w = 0
	a = ''
	while w == 0:
		a = ser1.readlines()
		if a !=b'':
			a = a.decode('utf-8')
			w = 1
	return(a)

def ctrlupdate(a):
	global loopstate
	a = a.split(',')
	upSwitch = int(a[0])
	downSwitch = int(a[1])
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
	if V1 == 9:
		ser2.write(b'k\n')
	elif V1 == 8:
		V = bytes(str(5), 'utf-8')
	elif V1 == 7:
		V = bytes(str(2.5), 'utf-8')
	elif V1 == 6:
		V = bytes(str(0.5), 'utf-8')
	elif V1 == 5:
		V = bytes(str(0.05), 'utf-8')
	elif V1 == 4:
		V = bytes(str(0.003), 'utf-8')
	elif V1 == 3:
		V = bytes(str(0.0015), 'utf-8')
	elif V1 == 2:
		V = bytes(str(0.0005), 'utf-8')
	elif V1 == 1:
		V = bytes(str(0.0001), 'utf-8')
	else:
		sleep(.01)
	#V = bytes(str(V1), 'utf-8')
	if upSwitch == 0:
		ser2.write(b'2H+\n')
		sleep(.01)
		ser2.write(b'2V' + V + b'\n')
		sleep(.01)
		ser2.write(b'2G\n')
		sleep(.01)
	if downSwitch == 0:
		ser2.write(b'2H-\n')
		sleep(.01)
		ser2.write(b'2V' + V + b'\n')
		sleep(.01)
		ser2.write(b'2G\n')
		sleep(.01)
	if upSwitch == 1 and downSwitch == 1:
		ser2.write(b'2V0\n')
		sleep(.01)
	if leftSwitch == 0:
		ser2.write(b'1H+\n')
		sleep(.01)
		ser2.write(b'1V' + V + b'\n')
		sleep(.01)
		ser2.write(b'1G\n')
		sleep(.01)
	if rightSwitch == 0:
		ser2.write(b'1H-\n')
		sleep(.01)
		ser2.write(b'1V' + V + b'\n')
		sleep(.01)
		ser2.write(b'1G\n')
		sleep(.01)
	if leftSwitch == 1 and rightSwitch == 1:
		port.write(b'1V0\n')
		sleep(.01)
	if blue == 1:
		camswitch()
	if green == 1:
		updatepos()
	if red ==1:
		distdisp()
		loopstate = 0


def vol():
	ser1.write(b'++addr3\n')
	sleep(.1)
	ser1.write(b'VL\n')
	sleep(.1)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readline()

		if a !=b'':
			w = 1
			b = str(a.decode('UTF-8'))
			volcom = a[:-2] + b'VL\n'
			print(b)
	sleep(.1)
	print(volcom)
	ser1.write(b'++addr5\n')
	sleep(.1)
	ser1.write(volcom)
	sleep(.1)
	ser1.write(b'M1')






def distdisp():
	updatepos()
	a = cX-pX
	b = cY-pY
	c = (a**2 + b**2)**.5
	Dvar.set(str(round(c,5)))

	pointbox.insert(str(round(c,5)))


def godist(x,y):
	xcom = bytes('1D' + str(int(x/motres)) + '\n')
	ycom = bytes('2D' + str(int(y/motres)) + '\n')

	ser2.write(b'MPI\n')
	sleep(.01)
	ser2.write(b'A4\n')
	sleep(.01)
	ser2.write(b'AD4\n')
	sleep(.01)
	ser2.write(b'V2\n')
	sleep(.01)
	ser2.write(xcom)
	sleep(.01)
	ser2.write(ycom)
	sleep(.01)
	ser2.write(b'G\n')
	sleep(.01)

	motconfig()


def camswitch():
	x = camoffset[0]*camstate
	y = camoffset[1]*camstate

	godist(x,y)

	camstate = camstate*(-1)








####LISTBOX FUNCTIONS #############

def filedn(box): #Move file down 1 spot in list
	idxs = box.curselection()
	size = box.size()
	if len(idxs)==1:
		pos = int(idxs[0])
		if pos != (size-1):
			nam = box.get(pos)
			box.delete(pos)
			box.insert(pos+1, nam)
			box.selection_set(pos+1)
		else:
			box.selection_set(pos)


def fileup(box): #Move file up 1 spot in list
	idxs = box.curselection()
	size = box.size()
	if len(idxs)==1:
		pos = int(idxs[0])
		if pos != 0:
			nam = box.get(pos)
			box.delete(pos)
			box.insert(pos-1, nam)
			box.selection_set(pos-1)
		else:
			box.selection_set(pos)


def delete(box): #Delete selected file in list
	idxs = box.curselection()
	if len(idxs)==1:
		pos = int(idxs[0])
		box.delete(pos)
		box.selection_set(pos)
	size = box.size()


def savefile(box):
	
	file = filedialog.asksaveasfile(mode='w',defaultextension=".csv")
	print(file)
	size = box.size()
	for i in range(size):
		line = box.get(i)
		file.write(line + '/n')

	file.close()




	

########## Initialize Serial Connections ##########

serinitXY()
time.sleep(.5)
serinitMOT()
time.sleep(.5)
serinitCON()


########### Begin Tkinter Stuff ##############

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

######### Density Display ###########
carusolabel = ttk.Label(mainframe, text = 'Caruso II Measurement Machine ', font = 'Segoe 18')
carusolabel.grid(column=1, row = 0, columnspan=2, pady = 20)

Xlabel = ttk.Label(mainframe, text = 'X-Axis', font = 'Segoe 12')
X1 = LabelFrame(mainframe, labelwidget = Xlabel, relief = 'ridge', borderwidth = 5)
X1.grid(column=1, row = 2, padx = 20)

Xshow = ttk.Label(X1, textvariable = Xvar, font ='Segoe 20')
Xshow.grid(column = 0, row = 0, padx=40)

Ylabel = ttk.Label(mainframe, text = 'Y-Axis', font = 'Segoe 12')
Y1 = LabelFrame(mainframe, labelwidget = Ylabel, relief = 'ridge', borderwidth = 5)
Y1.grid(column=2, row = 2, padx = 20)

Yshow = ttk.Label(Y1, textvariable = Yvar, font ='Segoe 20')
Yshow.grid(column = 0, row = 0, padx=40)

Dlabel = ttk.Label(mainframe, text = 'Distance', font = 'Segoe 12')
D1 = LabelFrame(mainframe, labelwidget = Dlabel, relief = 'ridge', borderwidth = 5)
D1.grid(column=1, row = 3, padx = 20, columnspan = 2, pady = 20)

Dshow = ttk.Label(D1, textvariable = Dvar, font ='Segoe 20')
Dshow.grid(column = 0, row = 0, padx=40)


plabel = ttk.Label(mainframe, text = 'Points', font = 'Segoe 16')
dlabel = ttk.Label(mainframe, text = 'Distances', font = 'Segoe 16')
plabel.grid(column = 1, row = 9)
dlabel.grid(column = 2, row = 9)

pointbox = Listbox(mainframe, height=20, font='ariel 12')
pscroll = ttk.Scrollbar(mainframe, orient=VERTICAL, command=pointbox.yview)
pupbutton = ttk.Button(mainframe, text="\u25b2", command=lambda: fileup(pointbox), default='active', width=5)
pdnbutton = ttk.Button(mainframe, text="\u25bc", command=lambda: filedn(pointbox), default='active', width=5)
psavebutton = ttk.Button(mainframe, text="SAVE", command=lambda: savefile(pointbox), default='active', width=5)
pdelbutton = ttk.Button(mainframe, text="DEL", command=lambda: delete(pointbox), default='active', width=5)

pointbox.configure(yscrollcommand=pscroll.set)


pointbox.grid(column=1, row=10, rowspan=10)
pscroll.grid(column=1, row=10, rowspan=14, sticky =(N,S,E),padx=20)
pupbutton.grid(column=1, row=10, sticky=(N,W))
pdnbutton.grid(column=1, row=10, sticky=(S,W),pady=5)
pdelbutton.grid(column=1, row=11, sticky=(N,W),pady=5)
psavebutton.grid(column=1, row=11, sticky=(S,W))

distbox = Listbox(mainframe, height=20, font='ariel 12')
dscroll = ttk.Scrollbar(mainframe, orient=VERTICAL, command=distbox.yview)
dupbutton = ttk.Button(mainframe, text="\u25b2", command=lambda: fileup(distbox), default='active', width=5)
ddnbutton = ttk.Button(mainframe, text="\u25bc", command=lambda: filedn(distbox), default='active', width=5)
dsavebutton = ttk.Button(mainframe, text="SAVE", command=lambda: savefile(distbox), default='active', width=5)
ddelbutton = ttk.Button(mainframe, text="DEL", command=lambda: delete(distbox), default='active', width=5)

distbox.configure(yscrollcommand=dscroll.set)


distbox.grid(column=2, row=10, rowspan=10)
dscroll.grid(column=2, row=10, rowspan=14, sticky =(N,S,E),padx=20)
dupbutton.grid(column=2, row=10, sticky=(N,W))
ddnbutton.grid(column=2, row=10, sticky=(S,W),pady=5)
ddelbutton.grid(column=2, row=11, sticky=(N,W),pady=5)
dsavebutton.grid(column=2, row=11, sticky=(S,W))


prvstr = ''
curstr = ''

while True:
	
	curstr = getinputs()
	if currstr != prevstr:
		ctrlupdate(currstr)
	prevstr = currstr


	Tk.update_idletasks(root)
	Tk.update(root)








