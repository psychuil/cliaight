import msvcrt
import random
from typing import NoReturn
import psutil
import os
import time
import colorful as cf
import arrow
import drives
import curses
from fuck_this_shit import print_str_at_loc

cf.use_style('solarized')


# TODO use this shit for graph history _-~`


def return_low_percent_with_color(percent) -> str:
    if float(percent) > 90:
        return f'{percent:>5}', curses.COLOR_RED
    elif float(percent) > 70:
        return f'{percent:>5}', curses.COLOR_YELLOW
    elif float(percent) > 40:
        return f'{percent:>5}', curses.COLOR_GREEN
    else:
        return f'{percent:>5}', curses.COLOR_CYAN

def return_high_percent_with_color(percent) -> str:
    if float(percent) > 90:
        return f'{percent:>5}', curses.COLOR_CYAN
    elif float(percent) > 70:
        return f'{percent:>5}', curses.COLOR_GREEN
    elif float(percent) > 40:
        return f'{percent:>5}', curses.COLOR_YELLOW
    else:
        return f'{percent:>5}', curses.COLOR_RED


def print_and_update_cpu_history() -> NoReturn:
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    print_str_at_loc(x=0, y=0, to_print='CPU Usage', fg_color=curses.COLOR_MAGENTA)
    for i in range(len(cpu_percent)):
        percent_str, cpu_color = return_low_percent_with_color(cpu_percent[i])
        print_str_at_loc(x=i * 7, y=1, to_print=f'{percent_str}%', fg_color=cpu_color)
        # cpu_output_str += f' [{return_percent_with_color(cpu_percent[i])}%] '


def get_memory_data():
    mem_data = psutil.virtual_memory()
    mem_percent_str, memory_color = return_low_percent_with_color(str(mem_data.percent))
    mem_str = f'{mem_percent_str}%  {mem_data.used / 1_000_000_000:.2f}GB'
    print_str_at_loc(x=0, y=4, to_print='Memory Usage', fg_color=curses.COLOR_MAGENTA)
    print_str_at_loc(x=1, y=5, to_print=mem_str, fg_color=memory_color)
    print_str_at_loc(x=1 + len(mem_str), y=5, to_print=f'/{mem_data.total / 1_000_000_000:.2f}GB',
                     fg_color=curses.COLOR_WHITE)
#
#
# def get_battery_data():
#     bat_data = psutil.sensors_battery()
#     bat_str = cf.underlined_cyan('\nBattery') + ':\n '
#     try:
#         if bat_data.power_plugged:
#             if bat_data.percent == 100:
#                 bat_str += cf.cyan('Plugged in, fully charged')
#             else:
#                 bat_str += cf.green(f'Charging: {return_percent_with_color(bat_data.percent)}%')
#         else:
#             bat_str += f'{return_percent_with_color(bat_data.percent)}%'
#     except AttributeError as e:
#         pass
#
#
def get_net_data():
    second_uptime = int((time.time() - psutil.boot_time()))
    net_stats = psutil.net_io_counters()
    mb_received = f'{net_stats.bytes_recv / 1_000_000:.2f}'
    mb_sent = f'{net_stats.bytes_sent / 1_000_000:.2f}'
    kbps_down = net_stats.bytes_recv / 1000 / second_uptime
    kbps_up = net_stats.bytes_sent / 1000 / second_uptime

    print_str_at_loc(x=0, y=9, to_print='Network Traffic Usage', fg_color=curses.COLOR_MAGENTA)
    print_str_at_loc(x=1, y=10, to_print=f' Down: {mb_received:>5} MB ({kbps_down:.1f}KBps avg)\tUp: {mb_sent:>5} MB ({kbps_up:.1f}KBps avg)', fg_color=curses.COLOR_BLUE)



def get_uptime():
    uptime_str = arrow.get(psutil.boot_time()).humanize(granularity=["hour", "minute", "second"])
    print_str_at_loc(x=0, y=0, to_print=f"{os.environ['COMPUTERNAME']}",orientation='rtl',
                     fg_color=curses.COLOR_YELLOW)
    print_str_at_loc(x=0, y=1, to_print=f"was booted", orientation='rtl',
                     fg_color=curses.COLOR_YELLOW)
    print_str_at_loc(x=0, y=2, to_print=f"{uptime_str}",orientation='rtl',
                     fg_color=curses.COLOR_YELLOW)



def print_exit_prompot():
    str = 'Ctrl-C to exit'
    color = curses.COLOR_RED
    print_str_at_loc(x=0, y=0, to_print=str, orientation='rtl', fg_color=color)


def print_all():
    print_and_update_cpu_history()
    get_memory_data()
    get_net_data()
    # print_exit_prompot()
    get_uptime()
    # time.sleep(1)


if __name__ == '__main__':
    while True:
        if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':
            break
        print_all()
