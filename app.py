"""
Application for managing patient information and interfacing
with the database
"""
import pandas, math

import patientsdb, errors, utils

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
        not utils.correct_date_form(params["DOB"]):
        return errors.DateError("") if "DOB" not in params \
            else errors.DateError(params["DOB"])
    if "LastActive" not in params or params["LastActive"] == "" or \
        not utils.correct_date_form(params["LastActive"]):
        return errors.DateError("") if "LastActive" not in params \
            else errors.DateError(params["LastActive"])

    patientsdb.add_record(cursor, params)
    return

def update_patient(cursor, patient_id, update_params):
    patientsdb.update_record_by_id(cursor, patient_id, update_params)

def delete_patient(cursor, params):
    results = patientsdb.get_records_by_fields(cursor, params)
    if len(results) == 1:
        patient_id = str(results[0][3])
        patientsdb.delete_record_by_id(cursor, patient_id)
    return results

def lookup(cursor, params):
    return patientsdb.get_records_by_fields(cursor, params)

def read_patients_csv(cursor, filename):
    cols = ["FirstName", "LastName","MiddleName", "Address", \
            "Email", "DOB", "LastActive"]
    df = pandas.read_csv(filename)
    df = df.fillna("") # Fill NaN values

    try:
        assert list(df) == cols
    except AssertionError:
        form = ', '.join(cols)
        return "Invalid file header format. Must be:\n{}".format(form)

    successes, failures = 0, {}
    for row in df.iterrows():
        new_patient = {}
        for field, value in zip(cols, row[1]):
            new_patient[field] = value

        result = add_patient(cursor, new_patient)
        if result == None:
            successes += 1
        else:
            _track_add_errors(failures, result, new_patient)

    return _read_results(successes, failures)

def _track_add_errors(fails, outcome, patient):
    if isinstance(outcome, errors.Error):
        if outcome.name() in fails:
            fails[outcome.name()].append((outcome, patient))
        else:
            fails[outcome.name()] = [(outcome, patient)]

def _read_results(successes, fails):
    """
    Receives the number of successes and a dict of errors where
    keys are the error types and values are Error object with its
    corresponding patient data
    """
    res_str = "\nSuccessfully added {} patient records. \n".format(successes)

    for k in fails.keys():
        res_str += "Encountered {} {}:\n".format(len(fails[k]), k)
        for err, patient in fails[k]:
            cause = ','.join(list(patient.values()))
            res_str += " {}\n  Source: {}\n".format(err, cause)

    return res_str

def find_recently_active(cursor, threshold=1):
    pass

def main():
    p = {"LastName": "Lopez", "FirstName": "TestUtilsParamToDict",
        "MiddleName":"Tulio", "Address":"Texas", "Email": "google",
        "DOB": "2017/01/26", "LastActive":"today"}

    cursor = patientsdb.connect_database()

    #add_patient(cursor, p)
    #lookup(cursor, {"LastName":"Lopez"})
    #lookup(cursor, {"LastName":"Lopez", "FirstName":"TestUtilsParamToDict"})
    #delete_patient(cursor, {"ID":"255"})
    #update_patient(cursor, 21, {"LastName":"Maguire", "FirstName":"Gerardo", "Address":"Grayslake"})
    print(read_patients_csv(cursor, "small_patients.csv"))

if __name__ == '__main__':
    main()
