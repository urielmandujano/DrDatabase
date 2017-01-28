"""
Application for managing patient information and interfacing
with the database
"""

import patientsdb, utils

def add_patient(cursor, params):
    # Note: More robust address check if address provided is looked
    # up in a mapping service.

    if "FirstName" not in params or params["FirstName"] == "":
        return errors.NameError("")
    if "LastName" not in params or params["LastName"] == "":
        return errors.NameError("")
    if "Address" not in params or params["Address"] == "":
        return errors.AddressError("")
    if "DOB" not in params or params["DOB"] == "" or \
        not utils.correct_dob_form(params["DOB"]):
        return errors.DOBError("") if "DOB" not in params \
            else errors.DOBError(params["DOB"])

    patientsdb.add_record(cursor, params)
    return

def update_patient():
    pass

def delete_patient():
    pass

def lookup(cursor, params):
    if len(params) == 1:
        results = patientsdb.get_record_by_field(cursor, params)
    else:
        results = patientsdb.get_records_by_many_fields(cursor, params)
    return results

def main():
    p = {"LastName": "Lopez", "FirstName": "TestUtilsParamToDict",
        "MiddleName":"Tulio", "Address":"Texas", "Email": "google",
        "DOB": "2017/01/26", "LastActive":"today"}

    cursor = patientsdb.connect_database()

    #add_patient(cursor, p)
    #lookup(cursor, {"LastName":"Lopez"})
    lookup(cursor, {"LastName":"Lopez", "FirstName":"TestUtilsParamToDict"})



if __name__ == '__main__':
    main()
