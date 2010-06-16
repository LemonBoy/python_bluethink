#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	import bluetooth
	import gtk.glade
	import gtk
	import sys
	import pynotify
	import time
	import gobject
	import egg.trayicon
	import os
	import gui
	import thread
	import subprocess
except:
	print 'Error during the loading...'
	raise SystemExit

nokia_init1 = 'ATZ\r'
nokia_init2 = 'AT+CMGF=1\r'#iunit
#nokia_sms_monitor = 'AT+CNMI=2,1\r'#sms
nokia_cid = 'AT+CLIP=1\r'#Call id
nokia_state = 'AT+CPAS\r'#stato
nokia_battery = 'AT+CBC\r'

gtk.gdk.threads_init()

running = True

apppath = sys.path[0]
pynotify.init("bluethink")

#graphic
disconnect = gtk.gdk.pixbuf_new_from_file(apppath + '/icon/' + 'disconnected' + '.png')
connected = gtk.gdk.pixbuf_new_from_file(apppath + '/icon/' + 'connect' + '.png')
ABOUT_ICON = apppath + '/icon/' + 'bluethink' + '.png'

gui# load the gui & the settings
liststore = gtk.ListStore(gobject.TYPE_STRING)
device = gui.device

print device

if device == "Nothing" or None:
	device = 'null'
else:
	device = device.split(" ")
	device = device[0]
port = 1





def connect(self):

	thread.start_new_thread(link, (None,))


def show_error_dlg(error_string):
	notify(error_string, 'error')


def test(self):
	
	#th.setDaemon(True)
	thread.start_new_thread(link, ())

def notify(msg,icon = None):
	gtk.gdk.threads_enter()
	if icon <> None:
		#print apppath + '/icon/' + icon + '.png'
		img = gtk.gdk.pixbuf_new_from_file(apppath + '/icon/' + icon + '.png')
		n = pynotify.Notification("bluethink", msg)
		n.set_icon_from_pixbuf(img)
		n.attach_to_status_icon(gui.icon)
	else:
		n = pynotify.Notification("...", msg)
		n.attach_to_widget(gui.icon)
	n.show()
	gtk.threads_leave()

def popup_menu_cb(widget, button, time, data = None):
    if button == 3:
        if data:
            data.show_all()
            data.popup(None, None, None, 3, time)
    pass



def changestat(pixbuf):
	gtk.gdk.threads_enter()
	gui.icon.set_from_pixbuf(pixbuf)
	gtk.gdk.threads_leave()
	return


def link():
	print device
	if device == 'Nothing' :
		show_error_dlg("There isn't a selected device. Select one from the Settings panel")
		raise SystemExit
	socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	try:
		print "Connection to " + device + ":" + str(port) + "...",
		socket.connect((device, port))
		print "ok."
		devname = bluetooth.lookup_name(device)
		#changestat(connected)
		gui.icon.set_from_pixbuf(connected)
	except (bluetooth.BluetoothError), err:
			show_error_dlg('Error...' + str(err))
			return	

		
	
	notify('Connected to "<b>' + devname +'</b>"','connected')
	socket.send(nokia_init1)
	socket.send(nokia_init2)
	socket.send(nokia_cid)
	socket.send(nokia_battery)
	#socket.send(nokia_sms_monitor)
	socket.listen
	socket.accept
	data = ""
	i = 0
	
	while running	:
		i = int(i) + 1
		#print i 
		try:
			data = socket.recv(1024)
			#print len(data)
		except bluetooth.BluetoothError, b:
			show_error_dlg("Bluetooth Error: " + str(b))
			changestat (disconnect)
		
		#data = data.replace('/r','')
		data = data.replace('ATZ\r','')
		data = data.replace('AT+CMGF=1\r','')#iunit
		data = data.replace('AT+CNMI=2,1\r','')#sms
		data = data.replace('AT+CLIP=1\r','')#Call id
		data = data.replace('AT+CPAS\r','')#stato
		data = data.replace('AT+CBC\r','')
		data = data.replace('OK\r','')
		data = data.replace('ERROR\r','')
		
		print data
		if data.find('+CBC: ') <> -1:
			battery = data.replace('+CBC: ','')
			battery = data.split(',')
			state = battery[0]
			state = state[-1:]
			state = str(state).replace(' ','')
			charge = battery[1]
			charge = charge.replace('\r','')
			charge = charge.replace('\n','')
			if int(charge) < 25:
				selectedicon = 'gpm-phone-000'
			elif int(charge) < 50:
				selectedicon = 'gpm-phone-030'
			elif int(charge) < 75:
				selectedicon = 'gpm-phone-060'
			elif int(charge) < 100:
				selectedicon = 'gpm-phone-100'
#			print data
			if int(state) == 0:
				notify ('The battery is charge at ' + str(charge) + '%', str(selectedicon))
				#gui.prefgui.get_widget('progressbar1').set_fraction = float(charge)
				if int(charge) < 10	:
					notify ('The battery level is low', 'battery')
			else:
					notify ('Charging...', 'battery')
		
		if data.find('RING') <> -1:
			#print 'ciao'
			if data.find('+CLIP: ') <> -1:
				caller = data.split('"')
				if caller[1] <> '':		
					notify ('Incoming call from <b>' + caller[1] + '</b>','ring')
					#gui.icon.set_blinking(True)
					if gui.sound == 'True':
						os.popen(r"play " + apppath + '/online.wav')
			else:
				notify ('A call is coming','ring')
				if gui.sound == 'True':
					os.popen(r"play " + apppath + '/online.wav')
	


def hide(self):
	gui.window.hide_all()
def show(self):
	gui.window.show_all()




def about(win):
		img = gtk.Image()
		img.set_from_file(ABOUT_ICON)
		img.show()
		dlg = gtk.AboutDialog()
		dlg.set_version('0.1')
		dlg.set_name("Bluethink")
		dlg.set_copyright("Copyright (c) 2007 Ubutnubox")
		dlg.set_logo(img.get_pixbuf())
		def close(w, res):
			 if res == gtk.RESPONSE_CANCEL:
			 	w.hide()
		dlg.connect("response", close)
		dlg.set_license("Bluethink is free software relased under GPL license terms")

		dlg.set_website("http://bluethink.tuxfamily.org")
		dlg.set_authors(["Ubuntubox <segnalazionidalweb@gmail.com@gmail.com>"])
		dlg.run()


menu = gtk.Menu()
menuItem = gtk.ImageMenuItem(gtk.STOCK_CONNECT)
menuItem.connect('activate', test)
menu.append(menuItem)
menuItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
menuItem.connect('activate', show)
menu.append(menuItem)
menuItem = gtk.SeparatorMenuItem()
menu.append(menuItem)
menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
menuItem.connect('activate', about)
menu.append(menuItem)
menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
menuItem.connect('activate', gtk.main_quit)
menu.append(menuItem)
gui.icon.connect('popup-menu', popup_menu_cb, menu)


if __name__ == '__main__':

	#gui.icon.set_blinking(True)
	gtk.gdk.threads_enter()
	gtk.main()
	gtk.threads_leave()



	
