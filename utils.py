"""
Contains util functions for use across modules
"""

import re
import time

def correct_dob_form(dob):
    """Returns true if dob is in form YYYY/MM/DD"""
    # Note: More robust check would be against a calendar

    match = "[1-2][0-9][0-9][0-9]/[0-1][1-9]/[0-3][1-9]"
    pattern = re.compile(match)
    matched = pattern.match(dob)
    if matched == None:
        return False

    curr_yr = int(time.strftime("%Y"))
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
    print(correct_dob_form("2017/01/01"))

if __name__ == '__main__':
    main()
