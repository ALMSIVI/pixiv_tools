from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import date
import re

def parse_selection(value, correspondence):
  try:
    return correspondence[value]
  except: # no default value is needed
    return ''

def parse_number(value):
  try:
    return int(value)
  except:
    return ''

def parse_date(value, format):
  try:
    date = parse(value)
    return date.strftime(format)
  except ValueError:
    today = utils.today()
    value = value.lower()
    splitted = re.split('([dwmy])', value)
    
    days = 0
    months = 0
    years = 0

    for i in range(1, len(splitted), 2):
      if splitted[i] == 'd':
        days += int(splitted[i - 1])
      elif splitted[i] == 'w':
        days += int(splitted[i - 1]) * 7
      elif splitted[i] == 'm':
        months += int(splitted[i - 1])
      elif splitted[i] == 'y':
        years += int(splitted[i - 1])

    date = today - relativedelta(days = days, months = months, years = years)
    return date.strftime(format)
  except TypeError: # no default value is needed
    return ''