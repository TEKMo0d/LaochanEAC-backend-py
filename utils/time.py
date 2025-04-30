from datetime import datetime

def dateTostring(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H-%M-%S")