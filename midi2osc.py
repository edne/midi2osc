#!/usr/bin/env python
import sys, threading
import gtk
import pypm # python-pypm

class App(object):
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 7000

        self.midi = Midi(self)
        self.gui = Gui(self)

        self.events = list()

    def run(self):
        try:
            self.midi.start()
            self.gui.run()
    	except KeyboardInterrupt:
    		self.midi.quit()

    def quit(self, *arg):
        self.midi.quit()
        self.gui.quit()

    def reset(self, host, port):
        print "reset %s:%d" % (host,port)

    def map(self, path):
        self.gui.log(path, "--")

    def event(self, key, val):
        print key,val

class Event(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val

class Midi(threading.Thread):
    def __init__(self, app):
        self.app = app
        threading.Thread.__init__(self)

        self.midiIn = pypm.Input(self._getInputs())
        self._quit = False

    def run(self):
        while not self._quit:
            while not self.midiIn.Poll(): pass
            ev = self.midiIn.Read(1)[0][0]
            if ev[0]==0x90:  # note on
                self.app.event('n'+str(ev[1]), float(ev[2])/0xF)
            if ev[0]==0x80:  # note off
                self.app.event('n'+str(ev[1]), 0.0)
            if ev[0]==0xB0:  # control
                self.app.event('c'+str(ev[1]), float(ev[2])/0xF)

    def quit(self):
        self._quit = True

    def _getInputs(self):
        for i in xrange(pypm.CountDevices()):
            interf,name,inp,outp,opened = pypm.GetDeviceInfo(i)
            if inp == 1:
                print name
                return i


class Gui(object):
    class Row(gtk.HBox):
        def __init__(self, app, gui):
            self.app = app
            self.gui = gui
            gtk.HBox.__init__(self)

            button = gtk.Button("map")
            self.pack_start(button, False, False)
            def pressed(*args): self.map()
            button.connect("button_press_event", pressed)

            self.path = gtk.Entry()
            self.pack_start(self.path, True, True)

            self.label = gtk.Label()
            self.pack_end(self.label, False, False, 2)

            self.show_all()

            self.text = ""

        def map(self):
            if self.text:
                del self.gui.rows[self.text]

            self.text = self.path.get_text()
            if self.text:
                self.gui.rows[self.text] = self
                self.app.map(self.path.get_text())

        def log(self, msg):
            self.label.set_text(str(msg))

    def __init__(self, app):
        self.app = app

        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.set_title("midi2osc")
        self.win.connect("destroy", self.app.quit)

        self.box = gtk.VBox()
        self.win.add(self.box)

        self.host = gtk.Entry()
        self.host.set_text(app.host)

        self.port = gtk.Entry()
        self.port.set_width_chars(6)
        self.port.set_text(str(app.port))

        hbox = gtk.HBox()
        self.box.pack_start(hbox, False, False, 1)

        hbox.pack_start(self.host, True, True)
        hbox.pack_start(gtk.Label(":"), False, False)
        hbox.pack_start(self.port, False, False)

        reset = gtk.Button("set")
        hbox.pack_start(reset, False, False)
        def pressed(*args): self.reset()
        reset.connect("button_press_event", pressed)

        new = gtk.Button("new")
        self.box.pack_start(new, False, False)
        def pressed(*args): self.new()
        new.connect("button_press_event", pressed)

        self.win.show_all()

        self.rows = dict()

    def run(self):
        gtk.main()

    def quit(self):
        gtk.main_quit()

    def new(self):
        self.box.pack_start(Gui.Row(self.app, self), False, False, 1)

    def reset(self):
        self.app.reset(
            self.host.get_text(),
            int(self.port.get_text())
        )

    def log(self, rowkw, msg):
        if rowkw in self.rows.keys():
            self.rows[rowkw].log(msg)

if __name__=='__main__':
	App().run()
