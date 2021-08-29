from libs.custom_exceptions import WrongTimeFormatError

def parse(time: str):
    timeinseconds: int = 0
    if time.endswith("s"):
        timeinseconds = int(time.replace("s",""))
    elif time.endswith("m"):
        timeinseconds = int(time.replace("m","")) * 60
    elif time.endswith("h"):
        timeinseconds = int(time.replace("h","")) * 3600
    elif time.endswith("d"):
        timeinseconds = int(time.replace("d","")) * 86400
    elif time.endswith("w"):
        timeinseconds = int(time.replace("w","")) * 604800
    else:
        raise WrongTimeFormatError
    return timeinseconds