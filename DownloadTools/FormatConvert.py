from datetime import datetime
import pytz


def local_to_utc(time_str, utc_format='%a %b %d %H:%M:%S %Y %z'):
    if int(time_str[-5:]) // 100 >= 0 :
        timezone = pytz.timezone('Etc/GMT' + str(-int(time_str[-5:]) // 100))
    else:
        timezone = pytz.timezone('Etc/GMT+' + str(-int(time_str[-5:]) // 100))
    local_format = "%Y-%m-%d %H:%M:%S"
    utc_dt = datetime.strptime(time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=timezone).astimezone(pytz.utc)
    return local_dt.strftime(local_format)