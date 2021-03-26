import os
import curses
import msvcrt as m
import time

# stdscr = curses.initscr()
# curses.noecho()
# curses.curs_set(0)
# curses.start_color()


def print_str_at_loc(x=0, y=0, to_print='=', orientation='ltr', fg_color=curses.COLOR_WHITE):
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    if orientation == 'rtl':
        x = os.get_terminal_size().columns - len(to_print)
    curses.init_pair(1, fg_color, 0)
    stdscr.addstr(y, x, to_print, curses.color_pair(1) + curses.A_ITALIC)
    stdscr.refresh()

