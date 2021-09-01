import datetime
import pytz

def curr_time():
    # current time info
    tz_NY = pytz.timezone('America/New_York') 
    date = datetime.datetime.now(tz_NY).strftime("%m/%d/%y")
    day = datetime.datetime.now(tz_NY).strftime('%a')
    hour = datetime.datetime.now(tz_NY).strftime('%I')
    minute = datetime.datetime.now(tz_NY).strftime('%M')
    suffix = datetime.datetime.now(tz_NY).strftime('%p')

    curr_time = (f'{hour}:{minute} {suffix}')
    return day, curr_time, date

def convert_datetime_to_text(my_datetime_object):
    date = my_datetime_object.strftime("%m/%d/%y")
    day = my_datetime_object.strftime('%a')
    hour = my_datetime_object.strftime('%I')
    minute = my_datetime_object.strftime('%M')
    suffix = my_datetime_object.strftime('%p')

    curr_time = (f'{hour}:{minute} {suffix}')
    return day, curr_time, date