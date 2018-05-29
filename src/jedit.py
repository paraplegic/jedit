#!/usr/bin/env python

import curses
import json
import atexit
import time

## import sys
## import os

##
## initialize and clear the screen ... 
def scr_init():
	global window_list

	atexit.register( scr_end )
	scr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	scr.nodelay( False )
	scr.clear()
	scr.border( 0 )
	scr.refresh()
	window_list.append( scr )
	return scr

##
## restore the screen to line mode ...
def scr_end():
	curses.nocbreak()
	curses.echo()
	curses.endwin()
	print "\nscreen mode ended."

##
## create a new window with a box around it ...
def scr_window( at, sz ):
	rv = curses.newwin( sz[0], sz[1], at[0], at[1] )
	window_list.append( rv )
	rv.border( 0 )
	y, x = rv.getmaxyx()
	scr_refresh()
	return rv

##
## close the last window opened ...
def scr_endwin():
	x = window_list.pop()
	x = None
	scr_refresh()

## 
## refresh the windows(s) in correct order ...
def scr_refresh():
	for w in window_list:
		w.touchwin()
                w.border( 0 )
		w.refresh()

##
## clear a window line while respecting the bounding box ...
def scr_clearline( w, row ):
	y, x = w.getmaxyx()
	x -= 2
	spaces = " " * x
	w.addstr( row, 1, spaces )
        w.border( 0 ) 
	w.refresh()

##
## clear the contents of a window ...
def scr_clearwin( w ):
    y, x = w.getmaxyx()
    for ix in range( 1, y-1 ):
        scr_clearline( w, ix )

##
## display a status message in the lower right quadrant ...
def scr_status( w, msg ):
    y, x = w.getmaxyx()
    mx = x - len( msg ) - 1 
    w.addstr( y-1, mx, msg[0:mx] )
    w.refresh()

##
## touch the stdscr ...
def scr_touch():
	global stdscr
	stdscr.touchwin()

##
## hit return to continue ...
def scr_hitreturn():
	global stdscr
	scr_status( stdscr, "hit return" )
	return stdscr.getch()

##
## vertical menu for select list ... 
def scr_vmenu( w, lst ):
	
	ix = 0
	mx = len( lst ) - 1
	while True:
		if ix < 0:
			ix = 0
		if ix > mx:
			ix = mx
		w.addstr( ix+1, 1, lst[ix], curses.A_REVERSE | curses.A_BOLD )
		w.refresh()
		ch = w.getch()
		w.addstr( ix+1, 1, lst[ix], curses.A_NORMAL )
		w.refresh()
		if ch == curses.KEY_UP or ch == ord( 'k' ):
			ix -= 1 
		if ch == curses.KEY_DOWN or ch == ord( 'j' ):
			ix += 1 
		if ch == 10 or ch == 13:
			scr_endwin()
			return ix

##
## determine the bounding box for a list ...
def scr_listbb( lst ):
	wd = 0
	for t in lst:
            sz = len( t )
            if sz > wd:
		wd = sz

	wd += 2
	ht = len( lst ) + 2
        return (ht, wd)


##
## display a select list and return the selection ...
def scr_select( at, lst ):
    sz = scr_listbb( lst )
    w = scr_window( at, sz )
    ix = 1
    for t in lst:
        w.addstr( ix, 1, t )
        ix += 1

    return scr_vmenu( w, lst )

##
## horizontal menu for menu list ... 
def scr_hmenu( win, lst ):
    y,x = win.getmaxyx()
    n,w = scr_listbb( lst )

    spacing = x/n
    if w > spacing:
        spacing = w

    ix = 0
    mx = len( lst ) -1 
    while True:
        if ix < 0:
            ix = 0
        if ix > mx:
            ix = mx
        pos = ix * spacing
        win.addstr( 1, 1+pos, lst[ix], curses.A_REVERSE )
	win.refresh()
	ch = win.getch()
        win.addstr( 1, 1+pos, lst[ix], curses.A_NORMAL )

	if ch == curses.KEY_UP or ch == ord( 'k' ):
    	    ix -= 1 
	if ch == curses.KEY_DOWN or ch == ord( 'j' ):
		ix += 1 
	if ch == 10 or ch == 13:
		scr_endwin()
		return ix

##
## create a horizontal menu at top of a window ...
def scr_menu( win, lst ):
    y,x = win.getmaxyx()
    n,w = scr_listbb( lst )

    spacing = x/n
    if w > spacing:
        spacing = w

    for ix,t in enumerate( lst ):
        pos = ix * spacing
        win.addstr( 1, 1+pos, t )

    win.hline( 2, 1, curses.ACS_HLINE, x-2 )
    return scr_hmenu( win, lst )

##
## get a string from window at location ... 
def scr_getstring( w, at ):
	ht = at[0]
	wd = at[1]
	rv = ""
	ch = 0
	x = wd
	while ch != 10 and ch != 13:		## <cr>/<nl>
		ch = w.getch( ht,x )
		if ch > 31 and ch < 127:	## printable ascii char ...
			xx = chr( ch )
			w.addch( ht,x,xx )
			rv += xx
			x += 1

		if ch == 12:		        ## formfeed  ...
                    w.border( 0 )
                    w.refresh()

		if ch == 8 or ch == 127:	## backspace ...
			if len( rv ) >= 1:
				rv = rv[0:-1]
				scr_clearline( w, ht )
				w.addstr( ht,wd,rv )
				x -= 1
			else:
				curses.beep()

		w.move( ht,x )
                w.border( 0 )
		w.refresh()

	return rv

stdscr = None
window_list = []

def main():
	global stdscr

	stdscr = scr_init()
	stdscr.addstr( 0, 10, " Ceeqit Assurance Platform " )
	w = scr_window( [10,10], [30,30] )
	scr_hitreturn()

	n = scr_select( [10, 10], [ "One", "Two", "Three", "Four", "Five" ])
        n = scr_menu( stdscr,  [ "One", "Two", "Three", "Four", "Five" ])
	scr_status( stdscr, "happy as a pig" )

	while True:
		scr_clearline( w, 1 )
		s = scr_getstring( w, [1,1] )
		scr_clearline( w, 10 )
		w.addstr( 10, 10, s )
		scr_refresh()

	scr_end()
	time.sleep( 2 )
	print s

if __name__ == '__main__':
	main()




