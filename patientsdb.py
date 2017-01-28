"""
Contains the public interface for interacting with
the patients database
python3.5

TODO
- add tests
"""
import sqlite3

import errors, utils

def connect_database(name="patientsdb.sqlite"):
    conn = sqlite3.connect(name)
    return conn.cursor()

def reinitialize_table(cursor, table):
    cursor.execute('''DROP TABLE IF EXISTS {}'''.format(table))
    create_patients_table(cursor, table)

def create_patients_table(cursor, table):
    cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                        FirstName   TEXT NOT NULL,
                        LastName    TEXT NOT NULL,
                        MiddleName  TEXT,
                        ID          INTEGER PRIMARY KEY AUTOINCREMENT,
                        Address     TEXT NOT NULL,
                        Email       TEXT,
                        DOB         DATE NOT NULL,
                        LastActive  DATE)'''.format(table))

def add_record(cursor, parameters):
    # Note: More robust address check if address provided is looked
    # up in a mapping service. Also, maybe should do this error checking
    # 1 layer up

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

    sql = '''INSERT INTO Patients (FirstName, LastName, MiddleName, \
          Address, Email, DOB, LastActive) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    params = (parameters["FirstName"], parameters["LastName"],
          parameters["MiddleName"], parameters["Address"],
          parameters["Email"], parameters["DOB"], parameters["LastActive"])
    cursor.execute(sql, params)
    cursor.connection.commit()
    return

def delete_record_by_id(cursor, target_id):
    sql = """DELETE FROM Patients WHERE id = ?"""
    cursor.execute(sql, (target_id,))

def update_record_by_id(cursor, target_id, field, contents):
    sql = """UPDATE Patients SET ? = ? WHERE ID = ?"""
    cursor.execute(sql, field, contents, target_id)

def get_records(cursor, field, target_value):
    sql = """SELECT * FROM Patients WHERE ? = ?"""
    cursor.execute(sql, field, target_value)

def test():
    cursor = connect_database()
    #reinitialize_table(cursor, "Patients")
    p = {"LastName": "Mandujano", "FirstName": "NewStyle",
        "MiddleName":"Tulio", "Address":"Texas", "Email": "google",
        "DOB": "2017/01/26", "LastActive":"today"}
    print (add_record(cursor, p))
    cursor.close()


test()
