from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import serial
import time
from time import sleep
import numpy
import scipy
import scipy.signal
import math
import os
import glob
import circle_fit

version = "Caruso II Rev 2.00.00"

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

cX = 0	#Current Measurement
cY = 0
pX = 0	#Previous Measurement
pY = 0
zX = 0	#Zero Point
zY = 0
pA = 0	#Part Angle

motres = .000096  #mm/step

camstate = IntVar()
camstate.set(1)

unitstate = IntVar()
unitstate.set(1)


xystate = IntVar()
xystate.set(1)

elstate = IntVar()
elstate.set(0)

pcdstate = IntVar()
pcdstate.set(0)

autostate = 0

loopstate = 0
lcent = 0
ccent = 0

xint = 0
xslope = 0

mmpp = .00008955   #millimeters per image pixel

xfact = 0.9999972
yfact = 0.9999888

ser1 = serial.Serial()
ser2 = serial.Serial()
ser3 = serial.Serial()


camoffset = [6.572,56.584] 		#From Aux to Main 

######### Program Functions #############

def serinitXY(): #Initialize serial connection
	try:
		ser1.port = '/dev/ttyUSB2'
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
		ser2.port = '/dev/ttyUSB1'
		ser2.baudrate = 9600
		ser2.parity = serial.PARITY_NONE
		ser2.stopbits = 1
		ser2.timeout = .1
		ser2.open()
	except:
		messagebox.showinfo('Failed to Connect to Motors')




def serinitCON(): #Initialize serial connection
	try:
		ser3.port = '/dev/ttyUSB0'
		ser3.baudrate = 9600
		ser3.parity = serial.PARITY_NONE
		ser3.stopbits = 1
		ser3.timeout = .1
		ser3.open()
	except:
		messagebox.showinfo('Failed to Connect to Controller')


	
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




def updatepos(r):
	global cX, cY, pX, pY, zX, zY, lcent
	pX = cX
	pY = cY
	ser1.write(b'++addr5\n')
	sleep(.05)
	flush1()
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readline()
		if a !=b'':
			try:
				a = a.decode('utf-8')
				a = -float(a)/2
			except:
				messagebox.showinfo('Error:', 'Please press the reset button and retry measurement')
				return
			w = 1
	
	ser1.write(b'++addr3\n')
	sleep(.05)
	flush1()
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		b = ser1.readline()
		if b !=b'':
			b = float(b)/2
			w = 1
	

	if lcent == 1:
		b = (cX+b)/2
		a = (cY+a)/2
		lcent = 0

	cX = b
	cY = a

	Xvar.set(str(round(b,5)))
	Yvar.set(str(round(a,5)))
	if r == 1:
		pointbox.insert(END,str(round(b,5)) + ',' + str(round(a,5)))
		zX = b
		zY = a

	#print('zX:', zX, 'zY:',zY,'cX:',cX,'cY:',cY,'pX:',pX,'pY:',pY)
	return (b,a)

def getinputs():
	flush3()
	w = 0
	a = ''
	while w == 0:
		a = ser3.readline()
		if a !=b'':
			a = a.decode('utf-8')
			w = 1
	return(a)



def ctrlupdate(a):
	global loopstate, autostate
	a = a.split(',')
	#print(a)
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
		sleep(.03)
	#V = bytes(str(V1), 'utf-8')
	if upSwitch == 0:
		ser2.write(b'2H+\n')
		sleep(.03)
		ser2.write(b'2V' + V + b'\n')
		sleep(.03)
		ser2.write(b'2A' + V + b'\n')
		sleep(.03)
		ser2.write(b'2AD' + V + b'\n')
		sleep(.03)
		ser2.write(b'2G\n')
		sleep(.03)
	if downSwitch == 0:
		ser2.write(b'2H-\n')
		sleep(.03)
		ser2.write(b'2V' + V + b'\n')
		sleep(.03)
		ser2.write(b'2A' + V + b'\n')
		sleep(.03)
		ser2.write(b'2AD' + V + b'\n')
		sleep(.03)
		ser2.write(b'2G\n')
		sleep(.03)
	if upSwitch == 1 and downSwitch == 1:
		ser2.write(b'2V0\n')
		sleep(.03)
		ser2.write(b'2G\n')
	if leftSwitch == 0:
		ser2.write(b'1H+\n')
		sleep(.03)
		ser2.write(b'1V' + V + b'\n')
		sleep(.03)
		ser2.write(b'1A' + V + b'\n')
		sleep(.03)
		ser2.write(b'1AD' + V + b'\n')
		sleep(.03)
		ser2.write(b'1G\n')
		sleep(.03)
	if rightSwitch == 0:
		ser2.write(b'1H-\n')
		sleep(.03)
		ser2.write(b'1V' + V + b'\n')
		sleep(.03)
		ser2.write(b'1A' + V + b'\n')
		sleep(.03)
		ser2.write(b'1AD' + V + b'\n')
		sleep(.03)
		ser2.write(b'1G\n')
		sleep(.03)
	if leftSwitch == 1 and rightSwitch == 1:
		ser2.write(b'1V0\n')
		sleep(.03)
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
		if elstate.get() ==2:
			centerpoint()
		else:
			pcdstate.set(1)
			mancpoint()
	if green == 1:
		print('elstate',elstate.get())
		if autostate == 1:
			autostate = 0
			return
		elif elstate.get() == 2:
			updatepos(1)
		else:
			pcdstate.set(0)
			mancpoint()
	if red ==1:
		if elstate.get() == 2:
			if loopstate == 1:
				loopstate = 0
			else:
				distdisp()
		else:
			pcdstate.set(2)
			mancpoint()



def vol():
	ser1.write(b'++addr3\n')
	sleep(.05)
	ser1.write(b'VL\n')
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readline()

		if a !=b'':
			w = 1
			b = str(a.decode('UTF-8'))
			volcom = a[:-2] + b'VL\n'
			#print(b)
	sleep(.05)
	#print(volcom)
	ser1.write(b'++addr5\n')
	sleep(.05)
	ser1.write(volcom)
	sleep(.05)
	ser1.write(b'M1')
	sleep(.05)
	ser1.write(b'++addr3\n')
	sleep(.05)
	ser1.write(b'M1')

def thp():
	ser1.write(b'++addr3\n')
	sleep(.1)
	ser1.write(b'AT\n')
	sleep(.1)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readline()

		if a !=b'':
			w = 1
			t = str(a.decode('UTF-8'))
			print('Temperature:', t)

		sleep(.1)
	ser1.write(b'AH\n')
	sleep(.1)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readline()

		if a !=b'':
			w = 1
			h = str(a.decode('UTF-8'))
			print('Humidity:', h)

	sleep(.1)
	ser1.write(b'AP\n')
	sleep(.1)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readline()

		if a !=b'':
			w = 1
			p = str(a.decode('UTF-8'))
			print('Pressure:', p)
	
	sleep(.1)
	ser1.write(b'T1\n')
	sleep(.1)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readline()

		if a !=b'':
			w = 1
			m = str(a.decode('UTF-8'))
			print('Material:', m)

	distbox.insert(0, t+ ',' + p + ',' + m)


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
		distbox.insert(END,str(round(e,5)))
	else:
		distbox.insert(END,str(round(e/25.4,6)))


def cupdate():
	ser1.write(b'++addr5\n')
	sleep(.05)
	flush1()
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		a = ser1.readline()
		if a !=b'':
			try:
				a = a.decode('utf-8')
				a = -float(a)/2
			except:
				messagebox.showinfo('Error:', 'Please press the reset button and retry measurement')
				return
			w = 1
	
	ser1.write(b'++addr3\n')
	sleep(.05)
	flush1()
	sleep(.05)
	ser1.write(b'RC\n')
	w = 0
	while w == 0:
		b = ser1.readline()
		if b !=b'':
			b = float(b)/2
			w = 1
	return(b, a)


def gaussfunc(x,a,b,c):
	return(a*numpy.exp(-((x-b)**2)/(2*c**2)))

def findedges(a):
	print(a)
	A = a.size
	ax = numpy.arange(A) - A/2 + 4
	max_ind = scipy.signal.argrelextrema(a, numpy.greater, order = 10)
	print(a.size,a)
	print(ax.size,ax)
	#Get values for every detected maximum
	max_ind = max_ind[0]
	maxes = []
	for i in range(len(max_ind)):
		maxes.append(a[max_ind[i]])
	mval = numpy.amax(maxes)
	print('mval:', mval)
	print('maxes:', maxes)
	print('max_ind', max_ind)


	#Filter maxes for edges over 1/2 the maximum edge value
	fmaxes = []
	for i in range(len(max_ind)):
		print('max', i, maxes[i])
		if maxes[i] > (mval/2):
			fmaxes.append(max_ind[i])

	
	locs = []
	print('fmaxes',fmaxes)

	for i in range(len(fmaxes)):
		j = 0
		while a[fmaxes[i]-j] > maxes[i]/2:
			j = j+1
			if (fmaxes[i] - j) == 0:
				break
		k = 0
		while a[fmaxes[i]+k] > maxes[i]/2:
			k = k+1
			if (fmaxes[i]+k) == len(a)-1:
				break

		xs = ax[fmaxes[i]-j:fmaxes[i]+k]
		ys = a[fmaxes[i]-j:fmaxes[i]+k]
		print(xs)
		print(ys)

		p0e = [mval,ax[fmaxes[i]],1]

		p0 = numpy.zeros(3)
		p1 = 0
		p0, p1 = scipy.optimize.curve_fit(gaussfunc, xs, ys,p0=p0e)

		print('p0',p0)
		print('p1',p1)



		locs.append(p0[1]*mmpp)

	return locs


def corredgefind(locs):
	
	cpos = locs[numpy.argmin(numpy.abs(locs))]
	print('cpos',cpos)

	

	return cpos


def linecenter(locs):

	print('locs', locs)

	c = locs[numpy.argmin(numpy.abs(locs))]
	locs[numpy.argmin(numpy.abs(locs))] = 1
	d = locs[numpy.argmin(numpy.abs(locs))]

	e = (c+d)/2

	print('c', c, 'd', d, 'e', e)


	return(e)

def getedges(xy):
	if xy == 1 or xy == 'x':
		a = [1]
	if xy == 0 or xy == 'y':
		a = [0]

	numpy.save('xyrequest.npy', a)
	w = 0
	while w == 0:
		if  os.path.isfile('xydata.npy'):
			time.sleep(1)
			xydata = numpy.load('xydata.npy')
			os.remove('xydata.npy')
			w = 1

	edges = findedges(xydata)

	return(edges)



def cpoint(xy,el):
	try:
		edges = getedges(xy)
	except:
		pass
		messagebox.showinfo(message = 'Check XY Edge Orientation')
		return

	print(edges, el)
	lx, ly = cupdate()
	if el == 'e' or el == 0:
		edge = corredgefind(edges)

	if el == 'l' or el == 1:
		edge = linecenter(edges)

	if el == 'o':
		edge = 0


	if xy == 'x' or xy == 1:
		cx = lx + edge
		cy = ly

	if xy == 'y' or xy ==0:
		cx = lx
		cy = ly - edge

	print(edge)




	return(cx, cy)



def mancpoint():
	global cX, cY, pX, pY, zX, zY, lcent, ccent
	try:
		xyn = xystate.get()
		eln = elstate.get()
		print('xyn', xyn, 'eln',eln)

		X, Y = cpoint(xyn, eln)

		pX = cX
		pY = cY

		pcd = pcdstate.get()
		print('pcd', pcd)

		if pcd == 0:
			pointbox.insert(END,str(round(X,5)) + ',' + str(round(Y,5)))
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
				distbox.insert(END,str(round(e,5)))
			else:
				distbox.insert(END,str(round(e/25.4,6)))

		cX = b
		cY = a
	except TypeError:
		pass 








def centerpoint():
	global lcent
	updatepos(0)
	lcent = 1

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

def gotopoint():
	global zX, zY, pA
	cgtX, cgtY = updatepos(0)
	pA = float(gtaentry.get())
	print('PA:', pA)

	gtX = float(gtxentry.get())
	gtY = float(gtyentry.get())
	xX = zX + gtX*numpy.cos(pA) + gtY*numpy.sin(pA)
	yY = zY + gtY*numpy.cos(pA) - gtX*numpy.sin(pA)
	fX = xX - cgtX
	fY = yY - cgtY
	godist(fX, fY)

def gotozero():
	global zX, zY
	cgtX, cgtY = updatepos(0)
	fX = zX - cgtX
	fY = zY - cgtY
	godist(fX, fY)

def gotoangle():
	global pA
	pA = -numpy.arctan((cY-pY)/(cX-pX))
	gtaentry.delete(0,END)
	gtaentry.insert(0,str(pA))

def gotoauto(gtX,gtY):
	global zX, zY, pA
	cgtX, cgtY = updatepos(0)
	pA = float(gtaentry.get())
	print('PA:', pA)

	xX = zX + gtX*numpy.cos(pA) + gtY*numpy.sin(pA)
	yY = zY + gtY*numpy.cos(pA) - gtX*numpy.sin(pA)
	fX = xX - cgtX
	fY = yY - cgtY
	godist(fX, fY)
	

def motconfig():

	ser2.write(b'2SCR1\n')
	sleep(.03)
	ser2.write(b'2MC\n')
	sleep(.03)
	ser2.write(b'2H+\n')
	sleep(.03)
	ser2.write(b'2A6\n')
	sleep(.03)
	ser2.write(b'2AD6\n')
	sleep(.03)
	ser2.write(b'2V0\n')
	sleep(.03)
	ser2.write(b'2MPP\n')
	sleep(.03)
	ser2.write(b'2G\n')
	sleep(.03)
	ser2.write(b'1SCR1\n')
	sleep(.03)
	ser2.write(b'1MC\n')
	sleep(.03)
	ser2.write(b'1H+\n')
	sleep(.03)
	ser2.write(b'1A6\n')
	sleep(.03)
	ser2.write(b'1AD6\n')
	sleep(.03)
	ser2.write(b'1V0\n')
	sleep(.03)
	ser2.write(b'1MPP\n')
	sleep(.03)
	ser2.write(b'1G\n')
	sleep(.03)



def godist(x,y):
	#print(x,y)
	ld = numpy.amax([abs(int(y/motres)),abs(int(x/motres))])/50000
	#print(ld)
	xcom = bytes('1D' + str(int(x/motres)) + '\n','utf-8')
	ycom = bytes('2D' + str(int(y/motres)) + '\n','utf-8')

	ser2.write(b'1MN\n')
	sleep(.03)
	ser2.write(b'1MPA\n')
	sleep(.03)
	ser2.write(b'1NG\n')
	sleep(.03)	
	ser2.write(b'1A0.05\n')
	sleep(.03)
	ser2.write(b'1PZ\n')
	sleep(.03)
	ser2.write(b'1AD0.05\n')
	sleep(.03)
	ser2.write(b'1V2\n')
	sleep(.03)
	ser2.write(xcom)
	sleep(.03)
	ser2.write(b'1G\n')
	time.sleep(.03)


	ser2.write(b'2MN\n')
	sleep(.03)
	ser2.write(b'2MPA\n')
	sleep(.03)
	ser2.write(b'2NG\n')
	sleep(.03)
	ser2.write(b'2A0.05\n')
	sleep(.03)
	ser2.write(b'2PZ\n')
	sleep(.03)
	ser2.write(b'2AD0.05\n')
	sleep(.03)
	ser2.write(b'2V2\n')
	sleep(.03)
	ser2.write(ycom)
	sleep(.03)
	ser2.write(b'2G\n')
	time.sleep(.03)


	ser2.reset_input_buffer()
	ser2.write(b'1"FIN1 \n')
	time.sleep(.05)
	ser2.write(b'2"FIN2 \n')
	time.sleep(.05)

	status1 = 0
	status2 = 0
	t1 = time.time()
	while status1 == 0 or status2 == 0:
		t2 = time.time()
		td = t2-t1
		lines = ser2.readlines()
		#print(lines, status1, status2)
		time.sleep(0.1)
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

	motconfig()

def motoron():
	ser2.write(b'1ON\n')
	ser2.write(b'2ON\n')

def motoroff():
	ser2.write(b'1OFF\n')
	ser2.write(b'2OFF\n')




def camswitch():
	cs = camstate.get()
	x = camoffset[0]*cs
	y = camoffset[1]*cs

	godist(x,y)

	camstate.set(camstate.get()*-1)



def resetlaser():
	ser1.write(b'++addr5\n')
	sleep(.1)
	ser1.write(b'RS\n')
	sleep(.1)
	ser1.write(b'5r1\n')
	sleep(.1)
	ser1.write(b'++addr3\n')
	sleep(.1)
	ser1.write(b'5r1\n')
	sleep(.1)
	ser1.write(b'RS\n')



#### Automeasure Functions

def parsepart(file):
	file = 'parts/' + file
	points = []
	centers = []
	meas = []
	diam = []
	with open(file,'rb') as lines:

		for line in lines:
			print(line)
			line = line.decode('utf-8-sig', 'ignore')
			a = line.split(',')

			if a[0][0] == 'P':
				points.append(a)

			if a[0][0] == 'C':
				centers.append(a)

			if a[0][0] == 'M':
				meas.append(a)

			if a[0][0] == 'D':
				diam.append(a)

	return(points, centers, meas, diam)


def autopoints(points):
	pmeas = {}
	for i in range(len(points)):
		X = mline[1]
		Y = mline[2]
		xy = mline[3]
		el = mline[4]
		godist(X,Y)


def measurepart():
	file = partcombo.get()
	sn = snentry.get()

	points, centers, meas, diam = parsepart(file)
	cpoints = {}

	print('points:',points)
	print('centers:',centers)
	print('meas:', meas)

	for i in range(len(points)):
		print(points[i])
		cx, cy = autocpoint(points[i])
		cpoints.update({points[i][0]:[cx, cy]})

	for i in range(len(centers)):
		x1 = cpoints[centers[i][1]][0]
		y1 = cpoints[centers[i][1]][1]
		x2 = cpoints[centers[i][2]][0]
		y2 = cpoints[centers[i][2]][1]

		x3 = (x1 + x2)/2
		y3 = (y1 + y2)/2

		cpoints.update({centers[i][0]:[x3,y3]})

	cmeas = []

	for i in range(len(meas)):
		x1 , y1 = cpoints[meas[i][1]]
		x2 , y2 = cpoints[meas[i][2]]

		D = (((x1-x2)*xfact)**2 + ((y1-y2)*yfact)**2)**0.5

		cmeas.append([meas[i][0], D])

	dmeas = []
	for i in range(len(diam)):

		points = diam[i][1:-1]
		print(points)
		print(cpoints)
		edgedata = numpy.zeros((len(points),2))
		for j in range(len(points)):
			edgedata[j,0], edgedata[j,1] = cpoints[points[j]]
		print(edgedata)
		xc, yc, r, sig = circle_fit.least_squares_circle(edgedata)

		D = r*2

		dmeas.append([diam[i][0], D])


	units = unitstate.get()

	file2 = 'completed/' + file[:-4] + '-' + sn + '.csv'

	if os.path.isfile(file2):
		with open(file2, 'a') as doc:
			temp = simpledialog.askstring(title = "Temperature", prompt="Enter Temperature in Degrees F" )
			humid = simpledialog.askstring(title = "Humidity", prompt="Enter Humidity in %RH")
			press = simpledialog.askstring(title = "Pressure", prompt="Enter Pressure in mbar")
			doc.write('Temperature,Humidity,Pressure,\n' + temp + ',' + humid + ',' + press + ',\n')
			doc.write('Measurement,Distance,\n')
			for i in range(len(cmeas)):
				if units == 1:
					doc.write(str(cmeas[i][0]) + ',' + str(round(cmeas[i][1],5)) + ',\n')
				else:
					doc.write(str(cmeas[i][0]) + ',' + str(round(cmeas[i][1]/25.4,6)) + ',\n')

	else:
		with open(file2, 'w') as doc:
			temp = simpledialog.askstring(title = "Temperature", prompt="Enter Temperature in Degrees F" )
			humid = simpledialog.askstring(title = "Humidity", prompt="Enter Humidity in %RH")
			press = simpledialog.askstring(title = "Pressure", prompt="Enter Pressure in mbar")
			doc.write('Temperature,Humidity,Pressure,\n' + temp + ',' + humid + ',' + press + ',\n')
			doc.write('Measurement,Distance,\n')
			for i in range(len(cmeas)):
				if units == 1:
					doc.write(str(cmeas[i][0]) + ',' + str(round(cmeas[i][1],5)) + ',\n')
				else:
					doc.write(str(cmeas[i][0]) + ',' + str(round(cmeas[i][1]/25.4,6)) + ',\n')

			for i in range(len(dmeas)):
				if units == 1:
					doc.write(str(dmeas[i][0]) + ',' + str(round(dmeas[i][1],5)) + ',\n')
				else:
					doc.write(str(dmeas[i][0]) + ',' + str(round(dmeas[i][1]/25.4,6)) + ',\n')

	time.sleep(1)
	os.system('libreoffice --calc /home/caruso/CUI2/' + file2)
	autoframe.configure(style = 'TFrame')





def refreshcsv():
	files = sorted(glob.glob('parts/*.csv'))
	parts = []
	for file in files:
		split = file.split('/')
		name = split[-1]
		print(name)
		if name != 'template':
			
			parts.append(name)

	partcombo['values'] = parts






				
def autocpoint(mline):
	global autostate, pY, pX, cY, cX
	X = float(mline[1])
	Y = float(mline[2])
	xy = mline[3]
	el = mline[4]
	autoframe.configure(style = 'red.TFrame')
	Tk.update_idletasks(root)
	Tk.update(root)
	
	for i in range(3):
		gotoauto(X,Y)
	if el == 'o':
		autoframe.configure(style = 'yellow.TFrame')
	else:
		autoframe.configure(style = 'green.TFrame')
	Tk.update_idletasks(root)
	Tk.update(root)
	autostate = 1
	while autostate == 1:
		a = getinputs()
		ctrlupdate(a)
	try:
		edges = getedges(xy)
	except:
		pass
		messagebox.showinfo(message = 'Check XY Edge Orientation')
		return


	lx, ly = cupdate()

	if el == 'e' or el == 0:
		edge = corredgefind(edges)

	if el == 'l' or el == 1:
		edge = linecenter(edges)

	if el == 'o' or el == 2:
		edge = 0


	if xy == 'x' or xy == 1:
		cx = lx + edge
		cy = ly

	if xy == 'y' or xy ==0:
		cx = lx
		cy = ly - edge

	print(edge)

	pX = cX
	pY = cY

	cX = cx
	cY = cy

	return(cx, cy)





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
		file.write(line + '\n')

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

rstyle = ttk.Style()
gstyle = ttk.Style()
ystyle = ttk.Style()

rstyle.configure('red.TFrame', background = 'red')
gstyle.configure('green.TFrame', background = 'green')
ystyle.configure('yellow.TFrame', background = 'yellow')
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


listframe = ttk.Frame(mainframe, relief='ridge')
listframe.grid(column = 1, row=10, padx = 20, pady=20, rowspan = 3, columnspan = 2)

plabel = ttk.Label(listframe, text = 'Points', font = 'Segoe 16')
dlabel = ttk.Label(listframe, text = 'Distances', font = 'Segoe 16')
plabel.grid(column = 1, row = 9,padx = 5,pady = 5)
dlabel.grid(column = 3, row = 9,padx = 5,pady = 5)

pointbox = Listbox(listframe, height=10, font='ariel 12')
pscroll = ttk.Scrollbar(listframe, orient=VERTICAL, command=pointbox.yview)
pupbutton = ttk.Button(listframe, text="\u25b2", command=lambda: fileup(pointbox), default='active', width=5)
pdnbutton = ttk.Button(listframe, text="\u25bc", command=lambda: filedn(pointbox), default='active', width=5)
psavebutton = ttk.Button(listframe, text="SAVE", command=lambda: savefile(pointbox), default='active', width=5)
pdelbutton = ttk.Button(listframe, text="DEL", command=lambda: delete(pointbox), default='active', width=5)

pointbox.configure(yscrollcommand=pscroll.set)


pointbox.grid(column=1, row=10, rowspan=10)
pscroll.grid(column=1, row=10, rowspan=14, sticky =(N,S,E))
pupbutton.grid(column=0, row=10, sticky=(N,W),padx = 5)
pdnbutton.grid(column=0, row=10, sticky=(S,W),pady=15,padx = 5)
pdelbutton.grid(column=0, row=11, sticky=(N,W),pady=15,padx = 5)
psavebutton.grid(column=0, row=11, sticky=(S,W),padx = 5)


###### GOTO Frame Widgets #######
gotoframe = ttk.Frame(mainframe, relief='ridge')
gotoframe.grid(column = 0, row=15, padx = 20, pady=20, rowspan = 2, columnspan = 2, sticky = 'W')


gtxlabel = ttk.Label(gotoframe, text = 'X', font = 'ariel 12')
gtxlabel.grid(column = 0, row = 0, padx = 10, pady = 10)

gtylabel = ttk.Label(gotoframe, text = 'Y', font = 'ariel 12')
gtylabel.grid(column = 1, row = 0, padx = 10, pady = 10)



gtxentry = ttk.Entry(gotoframe, width = 10, font = 'ariel 12')
gtxentry.grid(column = 0, row = 1, padx = 10, pady = 10)

gtyentry = ttk.Entry(gotoframe, width = 10, font = 'ariel 12')
gtyentry.grid(column = 1, row = 1, padx = 10, pady = 10)


gtalabel = ttk.Label(gotoframe, text = 'Part Angle', font = 'ariel 12')
gtalabel.grid(column = 0, row = 2, padx = 10, pady = 10)

gtaentry = ttk.Entry(gotoframe, width = 10, font = 'ariel 12')
gtaentry.grid(column = 1, row = 2, padx = 10, pady = 10)



gotobutton = ttk.Button(gotoframe, text = 'Go To', command = gotopoint)
gotobutton.grid(column = 2, row = 0, padx = 10, pady = 10)

gozerobutton = ttk.Button(gotoframe, text = 'Go Zero', command = gotozero)
gozerobutton.grid(column = 2, row = 1, padx = 10, pady = 10)

goanglebutton = ttk.Button(gotoframe, text = 'Set Angle', command = gotoangle)
goanglebutton.grid(column = 2, row = 2, padx = 10, pady = 10)

###### Take Corrected Point Widgets #######

corrframe = ttk.Frame(mainframe, relief = 'ridge')
corrframe.grid(column = 2, row = 15, padx=20, pady = 20, columnspan = 2, rowspan = 3)


cvbutton = ttk.Button(corrframe, text = 'CV Meas', command = mancpoint)
cvbutton.grid(column = 0, row = 0, padx = 10, pady = 10)


xradio = ttk.Radiobutton(corrframe, text='X', variable=xystate, value=1)
xradio.grid(column = 1, row = 0, padx = 10, pady = 10)
yradio = ttk.Radiobutton(corrframe, text='Y', variable=xystate, value=0)
yradio.grid(column = 2, row = 0, padx = 10, pady = 10)

oradio = ttk.Radiobutton(corrframe, text='Off', variable = elstate, value=2)
oradio.grid(column = 0, row = 1, padx = 10, pady = 10)
eradio = ttk.Radiobutton(corrframe, text='Edge', variable=elstate, value=0)
eradio.grid(column = 1, row = 1, padx = 10, pady = 10)
lradio = ttk.Radiobutton(corrframe, text='Line', variable=elstate, value=1)
lradio.grid(column = 2, row = 1, padx = 10, pady = 10)

pradio = ttk.Radiobutton(corrframe, text='Point', variable=pcdstate, value=0)
pradio.grid(column = 0, row = 2, padx = 10, pady = 10)
cradio = ttk.Radiobutton(corrframe, text='Center', variable=pcdstate, value=1)
cradio.grid(column = 1, row = 2, padx = 10, pady = 10)
dradio = ttk.Radiobutton(corrframe, text='Distance', variable=pcdstate, value=2)
dradio.grid(column = 2, row = 2, padx = 10, pady = 10)


##### Automated Part Measurement Widgets ######
autoframe = ttk.Frame(mainframe, relief = 'ridge')
autoframe.grid(row = 1, column = 1, columnspan = 3,  padx = 10, pady = 10)

partcombo = ttk.Combobox(autoframe, width = 20)
partcombo.grid(row = 1, column = 0, padx = 10, pady = 10)
refreshbutton = ttk.Button(autoframe, text = 'REFRESH', command = refreshcsv)
refreshbutton.grid(row = 1, column = 1, padx = 10, pady=10)

snlabel = ttk.Label(autoframe, text = 'SN:', font = 'ariel 12')
snlabel.grid(row = 1, column = 2, padx = 10, pady=10)
snentry = ttk.Entry(autoframe, width = 20, font = 'ariel 12')
snentry.grid(row = 1, column = 3, padx = 10, pady=10)

beginbutton = ttk.Button(autoframe, text = 'Begin', command = measurepart)
beginbutton.grid(row = 2, column = 0, padx = 10, pady=10)







distbox = Listbox(listframe, height=10, font='ariel 12')
dscroll = ttk.Scrollbar(listframe, orient=VERTICAL, command=distbox.yview)
dupbutton = ttk.Button(listframe, text="\u25b2", command=lambda: fileup(distbox), default='active', width=5)
ddnbutton = ttk.Button(listframe, text="\u25bc", command=lambda: filedn(distbox), default='active', width=5)
dsavebutton = ttk.Button(listframe, text="SAVE", command=lambda: savefile(distbox), default='active', width=5)
ddelbutton = ttk.Button(listframe, text="DEL", command=lambda: delete(distbox), default='active', width=5)

distbox.configure(yscrollcommand=dscroll.set)


distbox.grid(column=3, row=10, rowspan=10)
dscroll.grid(column=3, row=10, rowspan=14, sticky =(N,S,E))
dupbutton.grid(column=2, row=10, sticky=(N,W),padx = 5)
ddnbutton.grid(column=2, row=10, sticky=(S,W),pady=15,padx = 5)
ddelbutton.grid(column=2, row=11, sticky=(N,W),pady=15,padx = 5)
dsavebutton.grid(column=2, row=11, sticky=(S,W),padx = 5)

buttonframe = ttk.Frame(mainframe, relief='ridge')
buttonframe.grid(column = 4, row=10, padx = 20, pady=20, rowspan = 1, columnspan = 1)

resetbutton = ttk.Button(buttonframe, text = 'RESET', command = resetlaser)
resetbutton.grid(column=1,row = 4, padx = 10, pady = 10)

volbutton = ttk.Button(buttonframe, text = 'VOL', command = vol)
volbutton.grid(column=1,row = 5, padx = 10, pady = 10)

thpbutton = ttk.Button(buttonframe, text = 'THP', command = thp)
thpbutton.grid(column=1,row = 6, padx = 10, pady = 10)

# linedbutton = ttk.Button(buttonframe, text = 'Edge Distance', command = edgedistance)
# linedbutton.grid(column=1,row = 7, padx = 10, pady = 10)

# linedbutton = ttk.Button(buttonframe, text = 'Line Center D', command = linedistance)
# linedbutton.grid(column=1,row = 8, padx = 10, pady = 10)

onbutton = ttk.Button(buttonframe, text = 'Motor On', command = motoron)
onbutton.grid(column=1,row = 9, padx = 10, pady = 10)

offbutton = ttk.Button(buttonframe, text = 'Motor Off', command = motoroff)
offbutton.grid(column=1,row = 10, padx = 10, pady = 10)

lowtohighradio = ttk.Radiobutton(mainframe, text='Low to High', variable=camstate, value=1)
hightolowradio = ttk.Radiobutton(mainframe, text='High to Low', variable=camstate, value=-1)

lowtohighradio.grid(column = 4, row = 2, sticky = N)
hightolowradio.grid(column = 4, row = 2, sticky = S)

metricradio = ttk.Radiobutton(mainframe, text='Metric', variable=unitstate, value=1)
englishradio = ttk.Radiobutton(mainframe, text='English', variable=unitstate, value=-1)

metricradio.grid(column = 4, row = 3, sticky = W)
englishradio.grid(column = 4, row = 3, sticky = E)

prevstr = ''
currstr = ''

motconfig()
refreshcsv()

while True:
	
	currstr = getinputs()
	strlen = len(currstr)
	if strlen == 27:
		ctrlupdate(currstr)


	Tk.update_idletasks(root)
	Tk.update(root)








