import os.path
from datetime import datetime, timedelta
import functools   # used to preserve metadata of function (i.e. function name, docstring)


def api_tracking():
    track_file = "api_tracker.txt"
    today = datetime.now().date()

    if os.path.exists(track_file):
        with open(track_file, 'r') as file:
            last_date, count = file.read().split(',')
            last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
            count = int(count)

        if today > last_date:
            count = 1
        else:
            count += 1
    else:
        count = 1

    with open(track_file, 'w') as file:
        file.write(f"{today}, {count}")

    return count


def api_limit_checker(func):
    @functools.wraps(func)   # used to preserve meta data of function, like name and docstring
    def wrapper(*args, **kwargs):
        call_count = api_tracking()
        if call_count > 25:   # checking if limit has been exceeded
            print("API limit of 25 calls per day exceeded")
            return None   # carried out instead of making an API call
        return func(*args, **kwargs)  # calls the original function being decorated
    return wrapper
