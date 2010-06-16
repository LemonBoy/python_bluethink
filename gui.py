#!/usr/bin/python
# -*- coding: utf-8 -*-

import bluetooth
import gtk
import sys
import gobject
import gconf
import os
import gtk.glade
import thread

apppath = sys.path[0]
liststore = gtk.ListStore(gobject.TYPE_STRING)

class MyGconf:

     def __init__(self, appname):
             self.basedir = "/apps/" + appname
             self.client = gconf.client_get_default()

     def add_section(self, name, keys):
             """
                Aggiunge una sottodirectory a self.basedir e la riempie
                con le chiavi specificate nel dizionario keys
                """
             dir = self.basedir + "/" + name + "/"
             for key, value in keys.iteritems():
                     path = dir + key
                     self.client.set_string(path, value)

     def clean_section(self, name):
             """
                cosa potrebbe mai fare questo metodo :)
                """
             dir = self.basedir + "/" + name
             self.client.recursive_unset(dir, 0)

     def get_sections(self):
             """
                Ritorna una tupla contenente l'elenco delle sezioni
                contenute in self.basedir
                """
             return self.client.all_dirs(self.basedir)

     def get_key(self, name):
             """
                Ritorna il valore di una specifica chiave.
                name deve essere un percorso relativo a self.basedir
                """
             path = self.basedir + "/" + name
             return self.client.get_string(path)

     def set_key(self, name, value):
             """
                Imposta il valore della chiave name a value
                """
             path = self.basedir + "/" + name
             self.client.set_string(path, value)

def scan(self):
	thread.start_new_thread(searchdev, ())


def searchdev():
	gtk.gdk.threads_enter()
	prefgui.get_widget('combobox1').get_model().clear()
	try:
		devices = bluetooth.discover_devices(duration=10)
		
		if len(devices) > 0:
			for addr in devices:
   	 			print addr
				prefgui.get_widget('combobox1').append_text(addr + ' ' + bluetooth.lookup_name(addr))
		else:
			prefgui.get_widget('combobox1').append_text("Nothing")
	
	except bluetooth.BluetoothError:
		prefgui.get_widget('combobox1').append_text("Nothing")
	gtk.threads_leave()

def save(self):
	
	if mg.get_key('device') == None:
		print "non trovato"
		params = {
			"device": "",
			"play_sound": "",
			}
		#mg.add_section("settings", params)
		if prefgui.get_widget('combobox1').get_active_text() == None:
			mg.set_key('device',"Nothing")
		else:
			mg.set_key('device',str(prefgui.get_widget('combobox1').get_active_text()))
		mg.set_key('tomboy_note',str(prefgui.get_widget('checkbutton2').get_active()))
		#mg.set_key('battery_low',str(prefgui.get_widget('checkbutton1').get_active()))
		#mg.set_key('play_sound',str(prefgui.get_widget('checkbutton3').get_active()))
	else:
		"Creazione..."
		if prefgui.get_widget('combobox1').get_active_text() == None:
			mg.set_key('device',"Nothing")
		else:
			mg.set_key('device',str(prefgui.get_widget('combobox1').get_active_text()))
		#mg.set_key('tomboy_note',str(prefgui.get_widget('checkbutton2').get_active()))
		#mg.set_key('battery_low',str(prefgui.get_widget('checkbutton1').get_active()))
		mg.set_key('play_sound',str(prefgui.get_widget('checkbutton3').get_active()))
        hide

def hide(self,a):
	prefgui.get_widget("pref_dialog").hide()
	return True
def show():
	prefgui.get_widget("pref_dialog").show()

mg = MyGconf('dalink')
prefgui = gtk.glade.XML(apppath + '/prop.glade')
window = prefgui.get_widget("pref_dialog") 
#window.hide()

#load stuff
device = str(mg.get_key('device'))
if device <> 'Nothing':
	prefgui.get_widget('combobox1').append_text(device)
	prefgui.get_widget('combobox1').set_active(0)
sound = str(mg.get_key('play_sound'))
if sound == 'True':
	prefgui.get_widget('checkbutton3').set_active(True)
else:
	prefgui.get_widget('checkbutton3').set_active(False)
#battery = str(mg.get_key('battery_low'))
#if battery == 'True':
#	prefgui.get_widget('checkbutton1').set_active(True)
#else:
#	prefgui.get_widget('checkbutton1').set_active(False)
#tomboyplugin = str(mg.get_key('tomboy_note'))
#if tomboyplugin == 'True':
#	prefgui.get_widget('checkbutton2').set_active(True)
#else:
#	prefgui.get_widget('checkbutton2').set_active(False)



dic = {"on_refresh_clicked": scan,
        "on_button3_clicked": save,
		"on_pref_dialog_delete_event": hide
	}

#window.connect('destroy', hide)

prefgui.signal_autoconnect (dic)
#tray
icon = gtk.StatusIcon()
disconnect = gtk.gdk.pixbuf_new_from_file(apppath + '/icon/' + 'disconnected' + '.png')
icon.set_from_pixbuf(disconnect)
#icon.connect("activate",wrapcall)



if __name__ == '__main__':

	gtk.main()
