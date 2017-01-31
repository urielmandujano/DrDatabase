"""
Contains the test code for database manipulation functions
"""

import patientsdb

class DBTest(object):
    def __init__(self, testfile):
        self.cur = patientsdb.connect_database()
        self.testfile = testfile

    def run_all_tests(self):
        t1 = self.connect_database_test()
        t2 = self.reinitialize_table_test()
        t3 = self.create_table_test()
        t4 = self.add_record_test()
        t5 = self.delete_record_by_id_test()
        t6 = self.update_record_by_id_test()
        t7 = self.get_records_by_fields_test()
        t8 = self.get_records_by_date_test()
        results = [t1, t2, t3, t4, t5, t6, t7, t8]
        print("{} out of {} tests passed".format(sum(results), len(results)))

    def connect_database_test(self):
        """Tests if a valid cursor is created upon connection"""
        try:
            assert patientsdb.connect_database() != None
        except AssertionError:
            return False
        return True

    def reinitialize_table_test(self):
        """Tests if empty table with correct name exists after re-init"""
        patientsdb.reinitialize_table(self.cur, self.testfile)
        sql = """SELECT name FROM sqlite_master WHERE type='table'
                 AND name='{}'""".format(self.testfile)
        result1 = self.cur.execute(sql).fetchone()

        # Check if testtable exists and is empty
        sql = """SELECT * FROM {}""".format(self.testfile)
        result2 = self.cur.execute(sql).fetchall()
        if result1 and len(result2) == 0:
            return True
        else:
            return False

    def create_table_test(self):
        """Tests if new table is made with correct colmuns"""
        fields = ["FirstName", "LastName", "MiddleName", "ID", "Address", \
                  "Email", "DOB", "LastActive"]
        self.cur.execute("""DROP TABLE IF EXISTS {}""".format(self.testfile))
        patientsdb.create_patients_table(self.cur, self.testfile)

        sql = "PRAGMA table_info({})".format(self.testfile)
        results = self.cur.execute(sql).fetchall()
        for r in results:
            try:
                assert r[1] in fields
            except AssertionError:
                return False

        try:
            assert len(results) == len(fields)
        except AssertionError:
            return False

        return True

    def add_record_test(self):
        """Tests if an insertion is successful"""
        patientsdb.reinitialize_table(self.cur, self.testfile)

        p = {"LastName": "Generic", "FirstName": "Boring",
            "MiddleName":"Stale", "Address":"L.A.", "Email": "@google",
            "DOB": "2017-01-26", "LastActive":"2016-12-25"}
        patientsdb.add_record(self.cur, p, self.testfile)

        # Check DB increased by 1
        sql = """SELECT * FROM {}""".format(self.testfile)
        result = self.cur.execute(sql).fetchall()
        try:
            assert len(result) == 1
        except AssertionError:
            return False

        # Check new DB entry contains right information
        values = list(p.values()) + [1] # Add in ID field to params
        for r in result[0]:
            try:
                assert r in values
            except AssertionError:
                return False
        return True

    def delete_record_by_id_test(self):
        """Tests if deleting a single record by id works"""
        patientsdb.reinitialize_table(self.cur, self.testfile)
        p = {"LastName": "Generic", "FirstName": "Boring",
                "MiddleName":"Stale", "Address":"L.A.", "Email": "@google",
                "DOB": "2017-01-26", "LastActive":"2016-12-25"}
        num_records = 1
        patientsdb.add_record(self.cur, p, self.testfile)
        patientsdb.delete_record_by_id(self.cur, 1, self.testfile)

        # Check size of DB decreased by one
        sql = """SELECT * FROM {}""".format(self.testfile)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        try:
            assert len(result) == num_records - 1
        except AssertionError:
            return False

        # Check that deleted ID no longer in DB
        sql = """SELECT * FROM {} where ID == ?""".format(self.testfile)
        self.cur.execute(sql, (1,))
        result = self.cur.fetchall()
        try:
            assert len(result) == num_records - 1
        except AssertionError:
            return False

        return True

    def update_record_by_id_test(self):
        # Add new record
        patientsdb.reinitialize_table(self.cur, self.testfile)
        p = {"LastName": "Generic", "FirstName": "Boring",
            "MiddleName":"Stale", "Address":"L.A.", "Email": "@google",
            "DOB": "2017-01-26", "LastActive":"2015-11-14"}
        patientsdb.add_record(self.cur, p, self.testfile)

        # Create updated fields
        new_p = {"LastName": "NewGeneric", "FirstName": "NewBoring",
            "MiddleName":"NewStale", "Address":"NewL.A.",
            "Email": "New@google", "DOB": "2017-01-26", "LastActive":"2015-04-11"}

        # Update with new fields
        patientsdb.update_record_by_id(self.cur, 1, new_p, self.testfile)

        # Retrieve the added record by ID
        sql = """SELECT * FROM {} WHERE ID={}""".format(self.testfile, 1)
        result = self.cur.execute(sql).fetchall()

        # Check all retrieved fields match updated fields
        values = list(new_p.values()) + [1] # Add in ID field to params
        for r in result[0]:
            try:
                assert r in values
            except AssertionError:
                return False
        return True

    def get_records_by_fields_test(self):
        # Add multiple distinct records
        patientsdb.reinitialize_table(self.cur, self.testfile)
        pA = {"LastName": "A", "FirstName": "AA",
            "MiddleName":"AAA", "Address":"AAAA", "Email": "AAAAA",
            "DOB": "2017-01-26", "LastActive":""}
        pB = {"LastName": "B", "FirstName": "BB",
            "MiddleName":"BBB", "Address":"BBBB", "Email": "AAAAA",
            "DOB": "2017-01-26", "LastActive":""}
        pC = {"LastName": "C", "FirstName": "CC",
            "MiddleName":"CCC", "Address":"CCCC", "Email": "CCCCC",
            "DOB": "2017-01-26", "LastActive":""}
        patientsdb.add_record(self.cur, pA, self.testfile)
        patientsdb.add_record(self.cur, pB, self.testfile)
        patientsdb.add_record(self.cur, pC, self.testfile)

        # Get records by a field - Email
        results = patientsdb.get_records_by_fields(self.cur,
                                    {"Email":"AAAAA"},self.testfile)

        # Make sure each returned record matches (email) field query
        for r in results:
            try:
                assert r[5] == "AAAAA"
            except AssertionError:
                return False
        return True

    def get_records_by_date_test(self):
        # Insert 3 distinct date records
        patientsdb.reinitialize_table(self.cur, self.testfile)
        pA = {"LastName": "A", "FirstName": "AA",
            "MiddleName":"AAA", "Address":"AAAA", "Email": "AAAAA",
            "DOB": "2015-01-26", "LastActive":"2015-01-01"}
        pB = {"LastName": "B", "FirstName": "BB",
            "MiddleName":"BBB", "Address":"BBBB", "Email": "AAAAA",
            "DOB": "2017-01-26", "LastActive":"2016-01-01"}
        pC = {"LastName": "C", "FirstName": "CC",
            "MiddleName":"CCC", "Address":"CCCC", "Email": "CCCCC",
            "DOB": "2017-01-26", "LastActive":"2015-12-26"}
        patientsdb.add_record(self.cur, pA, self.testfile)
        patientsdb.add_record(self.cur, pB, self.testfile)
        patientsdb.add_record(self.cur, pC, self.testfile)

        # Query to receive only 2 of those date records back
        date = "2015-12-25"
        res = patientsdb.get_records_by_date(self.cur, date, self.testfile)

        # Make sure they are the correct number and correctly dated
        try:
            assert len(res) == 2
        except AssertionError:
            return False

        date = date.split('-')
        for r in res:
            r_date = r[7].split('-')
            for i in range(len(date)):
                if i == 0 and int(date[i]) < int(r_date[i]):
                    return True
                else:
                    try:
                        assert int(data[i]) <= int(r_date[i])
                    except AssertionError:
                        return False

def main():
    test = DBTest("TestTable")
    test.run_all_tests()

if __name__ == '__main__':
    main()
