import os.path
from datetime import datetime, timedelta
import functools   # used to preserve metadata of function (i.e. function name, docstring)


def api_tracking():
    track_file = "api_tracker.txt"   # defines file name
    today = datetime.now().date()

    if os.path.exists(track_file):
        with open(track_file, 'r') as file:
            last_date, count = file.read().split(',')
            last_date = datetime.strptime(last_date, '%Y-%m-%d').date()  # converts data string
            # into a date object, so it can be used for comparison
            count = int(count)

        if today > last_date:    # if today is not the last recorded date, then reset the counter
            count = 1
        else:    # incrementing the count if it's the same day
            count += 1
    else:
        count = 1    # if the file doesn't exist start the counter at 1

    with open(track_file, 'w') as file:    # writing the data and count into the tracking file
        file.write(f"{today}, {count}")

    return count    # to be used in the limit checker


def api_limit_checker(func):
    @functools.wraps(func)   # used to preserve meta data of function, like name and docstring
    def wrapper(*args, **kwargs):
        call_count = api_tracking()
        if call_count > 25:   # checking if limit has been exceeded
            print("API limit of 25 calls per day exceeded")
            return None   # carried out instead of making an API call
        return func(*args, **kwargs)  # calls the original function being decorated
    return wrapper
