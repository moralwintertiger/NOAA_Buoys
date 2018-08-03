import re

def dms_to_dd(entry):

    """
    Takes a DMS coordinate as a string input and produces a DD coordinate as output.
    Operates by HH + MM/60 + SS/3600
    """

    numeric_entry = re.sub("\D", "", entry)
    hh, mm, ss = float(numeric_entry[0:-4]), float(numeric_entry[-4:-2]), float(numeric_entry[-2:])
    if entry[0] == "-":
        return -(hh + mm/60 + ss/3600)
    else:
        return hh + mm/60 + ss/3600
