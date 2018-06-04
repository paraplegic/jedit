#!/usr/bin/env python

import curses
import json
import atexit
import time

## import sys
## import os

class Screen:

    window_list = []
    __stdscr = None

    def __init__( self ):
        self.window = None
        self._title = None
        self._status = None
        self._menu = None
        self._form = None

    def start( self ):
	atexit.register( self.terminate )
	self.window = curses.initscr()
        __stdscr = self.window
	curses.noecho()
	curses.cbreak()
	self.window.nodelay( False )
	self.window.clear()
	self.window.border( 0 )
	self.window.refresh()

    def terminate( self ):
	curses.nocbreak()
	curses.echo()
	curses.endwin()
        __stdscr = None

    def getchar( self ):
        return self.window.getch()

    def putstr( self, at, str, atts ):
        if atts:
            self.window.addstr( at[0], at[1], str, atts )
        else:
            self.window.addstr( at[0], at[1], str )

    def title( self, msg ):
        if msg:
            self._title = msg
        self.putstr( [0, 1], self._title, curses.A_BOLD )
    
    def status( self, msg ):
        if msg:
            self._status = msg
        y, x = self.window.getmaxyx()
        mx = x - len( msg ) - 1
        self.putstr( [y-1, mx], self._status[0:mx], curses.A_BOLD )

    def refresh( self ):
        for w in window_list:
            w.border( 0 )
        self._title( None )
        self.status( None )
        self.window.refresh()

def main():

    scr = Screen()
    print dir( scr )

    scr.start()
    scr.title( " Test Title " )
    scr.status( " Test status " )
    xx = scr.getchar()
    scr.terminate()
    print dir( scr )

if __name__ == "__main__":
    main()


