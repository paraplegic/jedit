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
		self.screen = None
		self._title = None
		self._status = None
		self._menu = None
		self._form = None

	def start( self ):
		atexit.register( self.terminate )
		self.screen = curses.initscr()
		__stdscr = self.screen
		curses.noecho()
		curses.cbreak()
		self.screen.nodelay( False )
		self.screen.clear()
		self.screen.border( 0 )
		self.screen.refresh()

	def terminate( self ):
		curses.nocbreak()
		curses.echo()
		curses.endwin()
		__stdscr = None

	def getchar( self ):
		return self.screen.getch()

	def putstr( self, at, str, atts ):
		if atts:
			self.screen.addstr( at[0], at[1], str, atts )
		else:
			self.screen.addstr( at[0], at[1], str )

	def title( self, msg ):
		if msg:
			self._title = msg
			self.putstr( [0, 1], self._title, curses.A_BOLD )
		
	def status( self, msg ):
		if msg:
			self._status = msg
			y, x = self.screen.getmaxyx()
			mx = x - len( msg ) - 1
			self.putstr( [y-1, mx], self._status[0:mx], curses.A_BOLD )

	def refresh( self ):
		for w in window_list:
			w.border( 0 )
			self._title( None )
			self.status( None )
			self.screen.refresh()

	class Window:

		def __init__( self, at, siz ):
			self.win = curses.newwin( at[0], at[1], siz[0], siz[1] )
			Screen.window_list.append( self.win )
			

def main():

	scr = Screen()
	scr.start()

	scr.title( " Test Title " )
	scr.status( " Test status " )
	ix = 0
	while True:
		xx = scr.getchar()
		scr.status( " Hit x to quit. " )
		if xx == 120:
			break
		scr.title( " title %s " % xx )
		w = scr.Window( [ 10, 10 ], [ 20, 20 ] )
		ix += 1

	scr.terminate()

if __name__ == "__main__":
		main()


