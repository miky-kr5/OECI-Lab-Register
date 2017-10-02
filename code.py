#! /usr/bin/env python
# _*_ coding: UTF-8 _*_

import web

urls = (
	'/', 'Index',
        '/[0-9]+', 'Subject'
	)

render = web.template.render('templates/')

db = web.database(dbn = 'mysql', user = '', pw = '', db = '')

COOKIE_SUBJECT = "weblabs_cookie_subject"

def _get_schedule_list():
        cookie = web.cookies().get(COOKIE_SUBJECT)
                
        if cookie is None or int(cookie) <= 1:
                return []
        
        schedules = db.query("SELECT sched_id, description FROM schedules WHERE sched_id > 1 AND subject_id = " + str(cookie) + " " +
                             "ORDER BY sched_id ASC")

        lst = []
        for s in schedules:
                lst.append((s['sched_id'], s['description']))
		
        return lst

def _get_subject_list():
	subjects = db.query("SELECT subject_id, name FROM subjects WHERE subject_id > 1 ORDER BY subject_id ASC")

	lst = []
	for s in subjects:
		lst.append((s['subject_id'], s['name']))
		
	return lst

class Index:
        form = web.form.Form(
		web.form.Dropdown(
			'asignatura',
			_get_subject_list(),
			description = "Asignatura inscrita"
			),
		web.form.Button('Seleccionar')
		)
        
        def GET(self):
                return render.index(self.form())

        def POST(self):
                form = self.form()
                form.validates()
                subject_id = form.d.asignatura
                web.setcookie(COOKIE_SUBJECT, subject_id)
                raise web.seeother('/' + str(subject_id))

class Subject:

	form = web.form.Form(
		web.form.Textbox(
			'cedula',
			web.form.notnull,
			web.form.regexp('\d+', 'Debe ser un numero'),
			size = 30,
			description = "Cedula de identidad:"
			),
		web.form.Textbox(
			'email', 
			web.form.notnull,
			size = 30,
			description = "Correo electronico:"
			),
		web.form.Dropdown(
			'horario',
			[],
			description = "Horario a inscribir:"
			),
		web.form.Button('Registrar horario')
		)
        
	def GET(self):
                cookie = web.cookies().get(COOKIE_SUBJECT)

                def validate_cookie(cookie):
                        found = False

                        subjects = db.query("SELECT subject_id FROM subjects WHERE subject_id > 1 ORDER BY subject_id ASC")
                        for s in subjects:
                                if int(cookie) == int(s['subject_id']):
                                        found = True
                                        break

                        return found
                
                if cookie is None or not validate_cookie(cookie):
                        raise web.seeother('/')

                
                schedules = _get_schedule_list()
                form = self.form()
                form.horario.args = schedules
                
		schedules = db.query(
			"SELECT schedules.sched_id, schedules.description, schedules.capacity, rooms.name " +
			"FROM schedules " +
			"INNER JOIN rooms ON schedules.room_id = rooms.room_id " +
                        "AND schedules.subject_id = " + str(cookie) + " " +
                        "ORDER BY schedules.sched_id ASC "
			)

                subject_name = db.query("SELECT name FROM subjects WHERE subject_id = " + str(cookie))
                
		return render.subject(subject_name[0]['name'], schedules, form, None)

	def POST(self):
		schedules = db.query(
			"SELECT schedules.sched_id, schedules.description, schedules.capacity, rooms.name " +
			"FROM schedules " +
			"INNER JOIN rooms ON schedules.room_id = rooms.room_id " +
			"ORDER BY schedules.sched_id ASC"
			)

		form = self.form()

		if not form.validates():
			return render.index(
				schedules,
				self.form(),
				"No deje los campos vac&iacute;os.<br/>La c&eacute;dula debe ser un n&uacute;mero."
				)

		else:

			student = db.query(
				"SELECT schedule_id FROM students WHERE id_CARD = $id AND email = $email",
				vars = {
					'id':str(form.d.cedula),
					'email':form.d.email.upper()
					}
				)

			if len(student) == 0:
				return render.index(schedules, self.form, "Cedula o email no encontrados.")
			else:
				if student[0]["schedule_id"] != 8:
					return render.index(schedules, self.form, "Estudiante con horario ya registrado.")
				else:

					sched = db.query(
						"SELECT description, capacity FROM schedules WHERE sched_id = $id",
						vars = {'id':form.d.horario}
						)

					if len(sched) == 0:
						return render.index(schedules, self.form, "ERROR: Horario no encontrado.")
					else:
						x = 0
						for s in sched:
							if x > 0:
								raise Exception("POOTIS")
							desc = s['description']
							cap = int(s['capacity'])
							x += 1

						if cap <= 0:
							return render.index(schedules, self.form, "Horario agotado.")
						else:
							db.query(
								"UPDATE schedules SET capacity = $cap where sched_id = $id",
								vars = {
									'id':form.d.horario,
									'cap':str((cap - 1))
									}
								)

							db.query(
								"UPDATE students " +
								"SET schedule_id = $sched " +
								"WHERE id_CARD = $id AND email = $email",
								vars = {
									'id':str(form.d.cedula),
									'email':form.d.email.upper(),
									'sched':form.d.horario
									}
								)

							schedules = db.query(
								"SELECT schedules.sched_id, schedules.description, " +
								"schedules.capacity, rooms.name " +
								"FROM schedules " +
								"INNER JOIN rooms ON schedules.room_id = rooms.room_id " +
								"ORDER BY schedules.sched_id ASC"
								)

							web.sendmail(
								'',
								form.d.email.lower(),
								'OECI - Laboratorio Registrado',
								'Ha registrado exitosamente el horario de laboratorio: ' + desc
								)

							return render.index(schedules, self.form, "Horario registrado exitosamente.")

if __name__ == "__main__":
	web.config.smtp_server = ''
	web.config.smtp_port = -1
	web.config.smtp_username = ''
	web.config.smtp_password = ''
	web.config.smtp_starttls = True

	app = web.application(urls, globals())
	app.run()
