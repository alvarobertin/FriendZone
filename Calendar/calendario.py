from flask import Flask, request, g, redirect, url_for, render_template, flash, session
import flask
import datetime
app = Flask(__name__)
calendario = []
dia = 0
mes = 0
anio= 0
actividades = [[11,"Crear un mmamamammafmemifiejfie"]]
diaElegido = 0
def construirCalendario(mes,diaDeLaSemana):
	calendario = [[0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0]]

	if(mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12):
		ultimoDia = 31
	elif (mes == 4 or mes == 6 or mes == 9 or mes == 11):
			ultimoDia = 30
	else:
		ultimoDia = 28

	dia = 1
	semana = 0
	while (dia <= ultimoDia):

		while (diaDeLaSemana < 7):
			calendario[semana][diaDeLaSemana] = dia
			diaDeLaSemana += 1
			dia += 1

			if(dia == ultimoDia + 1):
				break
		diaDeLaSemana = 0
		semana += 1 
	
	return calendario	




@app.route("/actividades/<dia>" , methods = ["GET","POST"])
def procesarActividades(dia):
	global calendario,mes,anio,activiad,diaElegido
	dia = datetime.date.today().day
	mes = datetime.date.today().month
	anio = datetime.date.today().year
	diaDeLaSemana = datetime.datetime(anio,mes,1).weekday()
	calendario = construirCalendario(mes, diaDeLaSemana)
	actividadesDelDia = []
	hayActividades = False
	if request.method == "POST":
		boton = request.form['boton']
		if boton == "Enviar":
			nuevaActividad = [int(dia), request.form['crearActividad']]
			actividades.append(nuevaActividad)
			diaElegido = int(dia)
		else:
			diaElegido = int(boton)
		if actividades != []:
			for actividad in actividades:
				if actividad[0] == diaElegido:
					actividadesDelDia.append(actividad[1])
					hayActividades = True
	return render_template("main.html",datos={"calendario":calendario,
											  "mes":mes,
											  "anio":anio,
											  "actividades":actividadesDelDia,
											  "hayActividades":hayActividades,
											  "diaElegido":diaElegido,
											  "presionoDia":True})

if(__name__ == "__main__"):
	app.run(debug=True)