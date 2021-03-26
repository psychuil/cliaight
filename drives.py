import psutil
import colorful as cf

def get_bar_string(percent_for_bar):
    blocks = '-' * int(percent_for_bar / 5)
    return f'[{blocks:<20}]'


def print_drives():
    storage_str = ''
    storage_str += cf.underlined_bold_cyan(f"\nStorage") + ': \n'
    for drive in psutil.disk_partitions(all=True):
        units = 'GB'
        name = drive.device.split(':')[0]
        total = float(psutil.disk_usage(drive.mountpoint).total)
        used = float(psutil.disk_usage(drive.mountpoint).used)
        if total > 1_000_000_000_000:
            units = 'TB'
            used /= 1000
            total /= 1000
        used_str = f"{used / 1_000_000_000:.1f}"
        total_str = f"{total / 1_000_000_000:.1f}"
        percent = psutil.disk_usage(drive.mountpoint).percent

        storage_str += f" ({name})  {int(100 - percent):>4}%  {get_bar_string(percent)}  {used_str:>6}/{total_str:<6} {units}\n"
    print(storage_str)
