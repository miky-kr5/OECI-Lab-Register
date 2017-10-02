#! /usr/bin/env python
# _*_ coding: UTF-8 _*_

import web

SUBJECTS = [("6001", 3), ("6004", 2)]

SECCTION_IDS = {"C1": 1,
                "C2": 2,
                "C3": 3,
                "C4": 4}

QUERY = "SELECT students.id_card AS cedula, students.first_name AS nombre, students.last_name AS apellido, students.email AS email, sections.section AS seccion, schedules.description AS horario, rooms.name AS salon FROM students INNER JOIN schedules ON schedules.sched_id = students.schedule_id INNER JOIN rooms ON schedules.room_id = rooms.room_id INNER JOIN sections ON students.class_id = sections.section_id AND students.class_id = $sect AND students.subject_id = $subj;"

def main():
    db = web.database(dbn = 'mysql', user = 'root', pw = 'Familylost9989*', db = 'labs')

    for s in SUBJECTS:
        for c in SECCTION_IDS.keys():
            with open(s[0] + "_" + c + ".csv", "w") as f:
                values = {"sect": SECCTION_IDS[c],
                          "subj": s[1]}
                students = db.query(QUERY, values)

                f.write("Cedula, Nombres, Apellidos, E-mail, Seccion, Horario, Salon,\n")
                
                for student in students:
                    out_str = ""
                    out_str += unicode(student['cedula']) + ", "
                    out_str += unicode(student['nombre']) + ", "
                    out_str += unicode(student['apellido']) + ", "
                    out_str += unicode(student['email']) + ", "
                    out_str += unicode(student['seccion']) + ", "
                    out_str += unicode(student['horario']) + ", "
                    out_str += unicode(student['salon']) + ", "

                    f.write(out_str.encode('utf8') + "\n")

if __name__ == '__main__':
     main()
