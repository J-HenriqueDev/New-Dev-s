import json
from pymongo import MongoClient
import pymongo
import time
import psutil
import config.database
import config.db
import config.time


def uptime():
 
  try:
    f = open("/proc/uptime")
    contents = f.read().split()
    f.close()
  except:
    return "Cannot open uptime file"

  total_seconds = float(contents[0])
 
  ## Helper vars:
  MINUTE = 60
  HOUR = MINUTE * 60
  DAY = HOUR * 24
 
  ## Get the days, hours, etc:
  days = int( total_seconds / DAY )
  hours = int( ( total_seconds % DAY ) / HOUR )
  minutes = int( ( total_seconds % HOUR ) / MINUTE )
  seconds = int( total_seconds % MINUTE )#eval timetotal()
 
  ## Build up the pretty string (like this: "N days. N hours, N minutes, N seconds")
  string = ""
  if days > 0:
    string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
  if len(string) > 0 or hours > 0:
    string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
  if len(string) > 0 or minutes > 0:
    string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
  string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
  return string;

def tempoen(texto):
  total_seconds = float(texto)
 
  ## Helper vars:
  MINUTE = 60
  HOUR = MINUTE * 60
  DAY = HOUR * 24
 
  ## Get the days, hours, etc:
  days = int( total_seconds / DAY )
  hours = int( ( total_seconds % DAY ) / HOUR )
  minutes = int( ( total_seconds % HOUR ) / MINUTE )
  seconds = int( total_seconds % MINUTE )#eval timetotal()
 
  ## Build up the pretty string (like this: "N days. N hours, N minutes, N seconds")
  string = ""
  if days > 0:
    string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
  if len(string) > 0 or hours > 0:
    string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
  if len(string) > 0 or minutes > 0:
    string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
  string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
  return string;

def tempopt(texto):
  total_seconds = float(texto)
 
  ## Helper vars:
  MINUTE = 60
  HOUR = MINUTE * 60
  DAY = HOUR * 24
 
  ## Get the days, hours, etc:
  days = int( total_seconds / DAY )
  hours = int( ( total_seconds % DAY ) / HOUR )
  minutes = int( ( total_seconds % HOUR ) / MINUTE )
  seconds = int( total_seconds % MINUTE )#eval timetotal()
 
  ## Build up the pretty string (like this: "N days. N hours, N minutes, N seconds")
  string = ""
  if days > 0:
    string += str(days) + " " + (days == 1 and "dia" or "dias" ) + ", "
  if len(string) > 0 or hours > 0:
    string += str(hours) + " " + (hours == 1 and "hora" or "horas" ) + ", "
  if len(string) > 0 or minutes > 0:
    string += str(minutes) + " " + (minutes == 1 and "minuto" or "minutos" ) + ", "
  string += str(seconds) + " " + (seconds == 1 and "segundo" or "segundos" )
 
  return string;