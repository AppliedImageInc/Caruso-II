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
import carusoII

print("after import")

##### global variables #####
version = "Caruso II Rev 3"
root = Tk()
try:
	root.iconbitmap('caruso.ico')
except:
	pass
root.title(version)

# UI 
def ui():

	##### UI functions #####

	# refresh the list of program files
	def refreshcsv():
		files = sorted(glob.glob(r'S:\Caruso II\parts\*.csv'))
		parts = []
		for file in files:
			split = file.split("\\")
			name = split[-1]
			print(name)
			if name != 'template':
			
				parts.append(name)

		partcombo['values'] = parts

	# move file down 1 spot in list
	def filedn(box): 
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

	# move file up 1 spot in list
	def fileup(box): 
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

	# delete selected file in list
	def delete(box): 
		idxs = box.curselection()
		if len(idxs)==1:
			pos = int(idxs[0])
			box.delete(pos)
			box.selection_set(pos)
		size = box.size()

	# save the measurement file
	def savefile(box):
		file = filedialog.asksaveasfile(mode='w',defaultextension=".csv")
		print(file)
		size = box.size()
		for i in range(size):
			line = box.get(i)
			file.write(line + '\n')

		file.close()

	# 
	# def update_dist_box():
		# distbox.insert(carusoII.dist_for_ui)

	# get the new distance measurement to add to the ui distbox
	def on_distance_change(*args):
		distance = carusoII.Dvar.get()
		print(f"distance changed to: {distance}")
		distbox.insert(END,distance)

	# get the new point to add to the ui pointbox
	def on_x_y_change(*args):
		x = carusoII.Xvar.get()
		y = carusoII.Yvar.get()
		print(f"x changed to: {x}")
		print(f"y changed to: {y}")
		pointbox.insert(END, x + ',' + y)

	# insert the updated part angle to the part angle box
	def set_angle():
		part_angle = carusoII.calculate_angle()
		gtaentry.delete(0,END)
		gtaentry.insert(0,str(part_angle))

	print("before tkinter")

	carusoII.ui_variable_inits()

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

	Xshow = ttk.Label(X1, textvariable = carusoII.Xvar, font ='Segoe 20')
	Xshow.grid(column = 0, row = 0, padx=40)

	Ylabel = ttk.Label(mainframe, text = 'Y-Axis', font = 'Segoe 12')
	Y1 = LabelFrame(mainframe, labelwidget = Ylabel, relief = 'ridge', borderwidth = 5)
	Y1.grid(column=2, row = 2, padx = 20)

	Yshow = ttk.Label(Y1, textvariable = carusoII.Yvar, font ='Segoe 20')
	Yshow.grid(column = 0, row = 0, padx=40)

	Dlabel = ttk.Label(mainframe, text = 'Distance', font = 'Segoe 12')
	D1 = LabelFrame(mainframe, labelwidget = Dlabel, relief = 'ridge', borderwidth = 5)
	D1.grid(column=1, row = 3, padx = 20, columnspan = 2, pady = 20)

	Dshow = ttk.Label(D1, textvariable = carusoII.Dvar, font ='Segoe 20')
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

	carusoII.Yvar.trace_add("write", on_x_y_change) # trace y bc it is changed second in carusoII.updatepos, so x will already be updated


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



	gotobutton = ttk.Button(gotoframe, text = 'Go To', command = lambda:[carusoII.gotopoint(gtaentry.get(), gtxentry.get(), gtyentry.get())])
	gotobutton.grid(column = 2, row = 0, padx = 10, pady = 10)

	gozerobutton = ttk.Button(gotoframe, text = 'Go Zero', command = lambda:[carusoII.gotopoint(None, gtxentry.get(), gtyentry.get())])
	gozerobutton.grid(column = 2, row = 1, padx = 10, pady = 10)

	goanglebutton = ttk.Button(gotoframe, text = 'Set Angle', command = set_angle)
	goanglebutton.grid(column = 2, row = 2, padx = 10, pady = 10)

	###### Take Corrected Point Widgets #######

	corrframe = ttk.Frame(mainframe, relief = 'ridge')
	corrframe.grid(column = 2, row = 15, padx=20, pady = 20, columnspan = 2, rowspan = 3)

	cvbutton = ttk.Button(corrframe, text = 'CV Meas', command = carusoII.mancpoint)
	cvbutton.grid(column = 0, row = 0, padx = 10, pady = 10)

	xradio = ttk.Radiobutton(corrframe, text='X', variable=carusoII.axis_state , value='x')
	xradio.grid(column = 1, row = 0, padx = 10, pady = 10)
	yradio = ttk.Radiobutton(corrframe, text='Y', variable=carusoII.axis_state , value='y')
	yradio.grid(column = 2, row = 0, padx = 10, pady = 10)

	oradio = ttk.Radiobutton(corrframe, text='Off', variable = carusoII.edge_detection_state, value=carusoII.off)
	oradio.grid(column = 0, row = 1, padx = 10, pady = 10)
	eradio = ttk.Radiobutton(corrframe, text='Edge', variable= carusoII.edge_detection_state, value=carusoII.edge)
	eradio.grid(column = 1, row = 1, padx = 10, pady = 10)
	lradio = ttk.Radiobutton(corrframe, text='Line', variable= carusoII.edge_detection_state, value=carusoII.line)
	lradio.grid(column = 2, row = 1, padx = 10, pady = 10)

	pradio = ttk.Radiobutton(corrframe, text='Point', variable = carusoII.pcdstate, value=0)
	pradio.grid(column = 0, row = 2, padx = 10, pady = 10)
	cradio = ttk.Radiobutton(corrframe, text='Center', variable = carusoII.pcdstate, value=1)
	cradio.grid(column = 1, row = 2, padx = 10, pady = 10)
	dradio = ttk.Radiobutton(corrframe, text='Distance', variable = carusoII.pcdstate, value=2)
	dradio.grid(column = 2, row = 2, padx = 10, pady = 10)

	###### Autofocus Button #######

	autofocus_frame = ttk.Frame(mainframe, relief = 'ridge')
	autofocus_frame.grid(column = 4, row = 15, padx=20, pady = 20, columnspan = 1, rowspan = 1)

	autofocus_button = ttk.Button(autofocus_frame, text = 'Autofocus Camera', command = carusoII.autofocus)
	autofocus_button.grid(column = 0, row = 0, padx = 10, pady = 10)

	score_button = ttk.Button(autofocus_frame, text = 'Get Autofocus Score', command = carusoII.cam2.calc_focus)
	score_button.grid(column = 0, row = 1, padx = 10, pady = 10)


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

	beginbutton = ttk.Button(autoframe, text = 'Begin', command = lambda: [carusoII.measurepart(partcombo.get(), snentry.get(), carusoII.unitstate.get(), autoframe, root)])
	beginbutton.grid(row = 2, column = 0, padx = 10, pady=10)


	liza_test_button = ttk.Button(autoframe, text = 'Ready?', command = carusoII.liza_test)
	liza_test_button.grid(row = 2, column = 1, padx = 10, pady=10)
	serial_label = ttk.Label(autoframe, text = 'Serial Command:', font = 'ariel 12')
	serial_label.grid(row = 2, column = 2, padx = 10, pady=10)
	serial_entry = ttk.Entry(autoframe, width = 10, font = 'ariel 12')
	serial_entry.grid(column = 3, row = 2, padx = 10, pady = 10)
	send_button = ttk.Button(autoframe, text = 'Send Command', command = lambda:[carusoII.send_serial_command(serial_entry.get())])
	send_button.grid(row = 2, column = 4, padx = 10, pady=10)

	distbox = Listbox(listframe, height=10, font='ariel 12')
	dscroll = ttk.Scrollbar(listframe, orient=VERTICAL, command=distbox.yview)
	dupbutton = ttk.Button(listframe, text="\u25b2", command=lambda: carusoII.fileup(distbox), default='active', width=5)
	ddnbutton = ttk.Button(listframe, text="\u25bc", command=lambda: carusoII.filedn(distbox), default='active', width=5)
	dsavebutton = ttk.Button(listframe, text="SAVE", command=lambda: carusoII.savefile(distbox), default='active', width=5)
	ddelbutton = ttk.Button(listframe, text="DEL", command=lambda: carusoII.delete(distbox), default='active', width=5)

	carusoII.Dvar.trace_add("write", on_distance_change)

	distbox.configure(yscrollcommand=dscroll.set)


	distbox.grid(column=3, row=10, rowspan=10)
	dscroll.grid(column=3, row=10, rowspan=14, sticky =(N,S,E))
	dupbutton.grid(column=2, row=10, sticky=(N,W),padx = 5)
	ddnbutton.grid(column=2, row=10, sticky=(S,W),pady=15,padx = 5)
	ddelbutton.grid(column=2, row=11, sticky=(N,W),pady=15,padx = 5)
	dsavebutton.grid(column=2, row=11, sticky=(S,W),padx = 5)

	buttonframe = ttk.Frame(mainframe, relief='ridge')
	buttonframe.grid(column = 4, row=10, padx = 20, pady=20, rowspan = 1, columnspan = 1)

	resetbutton = ttk.Button(buttonframe, text = 'RESET', command = carusoII.resetlaser)
	resetbutton.grid(column=1,row = 4, padx = 10, pady = 10)

	volbutton = ttk.Button(buttonframe, text = 'VOL', command = carusoII.vol)
	volbutton.grid(column=1,row = 5, padx = 10, pady = 10)

	thpbutton = ttk.Button(buttonframe, text = 'THP', command = lambda: [carusoII.thp, update_dist_box()])
	thpbutton.grid(column=1,row = 6, padx = 10, pady = 10)

	# linedbutton = ttk.Button(buttonframe, text = 'Edge Distance', command = edgedistance)
	# linedbutton.grid(column=1,row = 7, padx = 10, pady = 10)

	# linedbutton = ttk.Button(buttonframe, text = 'Line Center D', command = linedistance)
	# linedbutton.grid(column=1,row = 8, padx = 10, pady = 10)

	onbutton = ttk.Button(buttonframe, text = 'Motor On', command = carusoII.motoron)
	onbutton.grid(column=1,row = 9, padx = 10, pady = 10)

	offbutton = ttk.Button(buttonframe, text = 'Motor Off', command = carusoII.motoroff)
	offbutton.grid(column=1,row = 10, padx = 10, pady = 10)

	lowtohighradio = ttk.Radiobutton(mainframe, text='Low to High', variable=carusoII.camstate, value=1)
	hightolowradio = ttk.Radiobutton(mainframe, text='High to Low', variable=carusoII.camstate, value=-1)

	lowtohighradio.grid(column = 4, row = 2, sticky = N)
	hightolowradio.grid(column = 4, row = 2, sticky = S)

	metricradio = ttk.Radiobutton(mainframe, text='Metric', variable=carusoII.unitstate, value=1)
	englishradio = ttk.Radiobutton(mainframe, text='English', variable=carusoII.unitstate, value=-1)

	metricradio.grid(column = 4, row = 3, sticky = W)
	englishradio.grid(column = 4, row = 3, sticky = E)

	prevstr = ''
	currstr = ''

	carusoII.UI_controller_thread.start()
	carusoII.cam2.camera_thread.start()
	carusoII.autofocus_stage.main()


# things to do when the ui window is closed	
def on_exit():
	root.destroy() 
	
#main loop
def main():
	ui()
	# carusoII.init_serial_connections()
	# root.protocol("WM_DELETE_WINDOW", lambda: plot.save_pen_num(pen_num, root)) # when the window is closed, call the function to save the pen number
	root.protocol("WM_DELETE_WINDOW", on_exit)
	root.mainloop() # opens the loop that keep the gui running
	carusoII.UI_controller_thread.join()
	carusoII.cam2.camera_thread.start()
	
	
#run main
if __name__ == "__main__":
    main()

