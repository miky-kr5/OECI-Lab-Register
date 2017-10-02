#! /usr/bin/env python
# _*_ coding: UTF-8 _*_

import pandas
import web

FILES = [("/home/miky/Documentos/listado_6001_C1.xls", 3),
         ("/home/miky/Documentos/listado_6001_C2.xls", 3),
         ("/home/miky/Documentos/listado_6001_C3.xls", 3),
         ("/home/miky/Documentos/listado_6001_C4.xls", 3),
         ("/home/miky/Documentos/listado_6004_C1.xls", 2),
         ("/home/miky/Documentos/listado_6004_C2.xls", 2)]

SHEET_NAME = "Sheet1"

SECCTION_IDS = {"C1": 1,
                "C2": 2,
                "C3": 3,
                "C4": 4}

QUERY = "INSERT INTO students(id_card, first_name, last_name, email, class_id, schedule_id, subject_id) VALUES($id, $fn, $ln, $ml, $cl, 1, $sj)"

def main():
    db = web.database(dbn = 'mysql', user = 'root', pw = 'Familylost9989*', db = 'labs')

    for f in FILES:
        xls = pandas.ExcelFile(f[0])
        df = xls.parse(SHEET_NAME)

        subject_id = f[1]
        section_id = SECCTION_IDS[df.iloc[7, 1]]

        row = 10
        while True:
            try:
                values = {"id": int(df.iloc[row, 2]),
                          "fn": unicode(df.iloc[row, 3]),
                          "ln": unicode(df.iloc[row, 4]),
                          "ml": unicode(df.iloc[row, 5]),
                          "cl": section_id,
                          "sj": subject_id}

                db.query(QUERY, vars = values)

                row += 1
            except IndexError:
                break

if __name__ == '__main__':
     main()
