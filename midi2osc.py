#!/usr/bin/env python
import gtk

class App(object):
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 7000

        self.gui = Gui(self)

    def run(self):
        self.gui.run()

    def quit(self, *arg):
        self.gui.quit()

class Gui:
    class Row(gtk.HBox):
        def __init__(self):
            gtk.HBox.__init__(self)

            self.button = gtk.Button("map")
            self.pack_start(self.button, False, False)

            self.entry = gtk.Entry()
            self.pack_start(self.entry, True, True)

            self.label = gtk.Label()
            self.pack_end(self.label, False, False, 2)

            self.show_all()

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

        reset = gtk.Button("set")

        hbox = gtk.HBox()
        hbox.pack_start(self.host, True, True)
        hbox.pack_start(gtk.Label(":"), False, False)
        hbox.pack_start(self.port, False, False)
        hbox.pack_start(reset, False, False)
        self.box.pack_start(hbox, False, False, 1)

        new = gtk.Button("new")
        self.box.pack_start(new, False, False)
        def pressed(*args): self.row()
        new.connect("button_press_event", pressed)

        self.win.show_all()

    def run(self):
        gtk.main()

    def quit(self):
        gtk.main_quit()

    def row(self):  # TODO change method name
        self.box.pack_start(Gui.Row(), False, False, 1)

if __name__=='__main__':
	App().run()
