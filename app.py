"""
Application for managing patient information and interfacing
with the database
"""

import patientsdb

def add_patient(cursor, params):
    # Note: More robust address check if address provided is looked
    # up in a mapping service.

    if "FirstName" not in parameters or parameters["FirstName"] == "":
        return errors.NameError("")
    if "LastName" not in parameters or parameters["LastName"] == "":
        return errors.NameError("")
    if "Address" not in parameters or parameters["Address"] == "":
        return errors.AddressError("")
    if "DOB" not in parameters or parameters["DOB"] == "" or \
        not utils.correct_dob_form(parameters["DOB"]):
        return errors.DOBError("") if "DOB" not in parameters \
            else errors.DOBError(parameters["DOB"])

    patientsdb.add_record(cursor, params)
    return

def update_patient():
    pass

def delete_patient():
    pass

def lookup_by_name(cursor, f_name, l_name):

    pass

def lookup_by_DOB():
    pass

def main():
    cursor = patientsdb.connect_database()

    add_patient(cursor)



if __name__ == '__main__':
    main()
