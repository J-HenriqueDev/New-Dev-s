import psutil
import os
import time
import platform

startTime = time.time()

def timetotal():
  total_seconds = float(time.time() - startTime)
  MINUTE = 60
  HOUR = MINUTE * 60
  DAY = HOUR * 24
  days = int( total_seconds / DAY )
  hours = int( ( total_seconds % DAY ) / HOUR )
  minutes = int( ( total_seconds % HOUR ) / MINUTE )
  seconds = int( total_seconds % MINUTE )
  string = ""
  if days > 0:
    string += str(days) + " " + (days == 1 and "{day}" or "{day}s" ) + ", "
  if len(string) > 0 or hours > 0:
    string += str(hours) + " " + (hours == 1 and "{hour}" or "{hour}s" ) + ", "
  if len(string) > 0 or minutes > 0:
    string += str(minutes) + " " + (minutes == 1 and "{minute}" or "{minute}s" ) + ", "
  string += str(seconds) + " " + (seconds == 1 and "{second}" or "{second}s" )
  return string;

def get_memory():
    memory = dict()
    mem = psutil.virtual_memory()
    process = psutil.Process(os.getpid())
    process = process.memory_info().rss
    memory['memory_used'] = f'{mem.used / 0x40_000_000:.2f}'
    memory['memory_available'] = f'{mem.available / 0x40_000_000:.2f}'
    memory['memory_total'] = f'{mem.total / 0x40_000_000:.2f}'
    memory['memory_free'] = f'{mem.free / 0x40_000_000:.2f}'
    memory['memory_percent'] = str(mem.percent) + '%'
    memory['process_python'] = f'{process / 1024 / 1024:.2f}'

    return memory

def cpu_usage():
  return psutil.cpu_percent(interval=1)

def host_name():
  return platform.processor()