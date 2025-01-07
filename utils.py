from datetime import datetime


def msg_time():
    return f'[{datetime.now().strftime("%y-%m-%d %H:%M")}]'
