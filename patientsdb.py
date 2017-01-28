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
    sql = '''INSERT INTO Patients (FirstName, LastName, MiddleName, \
          Address, Email, DOB, LastActive) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    params = (parameters["FirstName"], parameters["LastName"],
          parameters["MiddleName"], parameters["Address"],
          parameters["Email"], parameters["DOB"], parameters["LastActive"])
    cursor.execute(sql, params)
    cursor.connection.commit()

def delete_record_by_id(cursor, target_id):
    sql = """DELETE FROM Patients WHERE id = ?"""
    cursor.execute(sql, (target_id,))

def update_record_by_id(cursor, target_id, field, contents):
    sql = """UPDATE Patients SET ? = ? WHERE ID = ?"""
    cursor.execute(sql, field, contents, target_id)

def get_records_by_fields(cursor, params):
    """
    Gets records by searching for multiple matching fields. Fields
    should be designated as key value pair in the params dictionary
    """
    num_fields = len(params)
    base_query = ""
    for i in range(num_fields - 1):
        base_query += "{} = ? AND "
    base_query += "{} = ?"

    fields, values = utils.param_dict_to_tuple(params)
    base_query = base_query.format(*fields)
    sql = """SELECT * From Patients WHERE {}""".format(base_query)
    results = cursor.execute(sql, values)
    return results.fetchall()

def main():
    cursor = connect_database()
    #reinitialize_table(cursor, "Patients")
    p = {"LastName": "Mandujano", "FirstName": "TestUtilsParamToDict",
        "MiddleName":"Tulio", "Address":"Texas", "Email": "google",
        "DOB": "2017/01/26", "LastActive":"today"}
    #print (add_record(cursor, p))
    get_records_by_many_fields(cursor, {"FirstName":"Test", "Email":"google"})
    cursor.close()

if __name__ == '__main__':
    main()
