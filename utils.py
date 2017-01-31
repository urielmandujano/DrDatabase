"""
Contains util functions for use across modules
"""

import re
import datetime
from dateutil.relativedelta import relativedelta

def correct_date_form(dob):
    """Returns true if date is in form YYYY-MM-DD"""
    # Note: More robust check would be against a calendar

    match = "[1-2][0-9][0-9][0-9]-[0-1][1-9]-[0-3][1-9]"
    pattern = re.compile(match)
    matched = pattern.match(dob)
    if matched == None:
        return False

    curr_yr = int(datetime.date.today().year)
    given_yr = int(dob[:4])
    if curr_yr - 150 > given_yr or given_yr > curr_yr:
        return False

    given_mo = int(dob[5:7])
    if given_mo < 1 or given_mo > 12:
        return False

    given_day = int(dob[8:10])
    if given_day < 1 or given_day > 31:
        return False
    return True

def today():
    iso = datetime.date.today().isoformat()
    """
    today = ""
    for c in iso:
        if c == '-':
            c = '/'
        today += c
    return today
    """
    return iso

def date_threshold(fraction):
    back = int(365 * fraction)
    back_date = str(datetime.date.today() + relativedelta(days=-back))
    """
    thresh = ""
    for c in back_date:
        if c == '-':
            c = '/'
        thresh += c
    return thresh
    """
    return back_date

def param_dict_to_tuple(params):
    """Converts a dict of params into 2 ordered tuples for DB use"""
    fields = ['FirstName', 'LastName', 'MiddleName', 'ID', 'Address', 'Email',\
              'DOB', 'LastActive']
    ordered_fields, ordered_values = [], []
    for f in fields:
        if f in params:
            ordered_fields.append(f)
            ordered_values.append(params[f])
    return tuple(ordered_fields), tuple(ordered_values)

def main():
    print(correct_date_form("2017-01-01"))
    print(today())
    print(date_threshold(.3))

if __name__ == '__main__':
    main()
