#encoding: utf-8
import fm, channels
import thread, gobject, glib

while 1:
    mainclass = fm.FM()
    thread.start_new_thread(mainclass.play, ())
    gobject.threads_init()
    loop = glib.MainLoop()
    loop.run()
