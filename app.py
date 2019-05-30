from flask import Flask, request, g, redirect, url_for, render_template, flash, session
import flask
import sys
from flask import json
from functools import wraps
import re # Para quitar los \n del final de las lineas
import json
import datetime
app = Flask(__name__)

###############################################################################################################
################################################FUNCTIONS AND PROCEDURES#######################################
###############################################################################################################
def procegroup():
#Devuelve los grupos en los que SI está el usuario.
    grupos = []
    archivo = open('grupos.txt','r+')
    for l in archivo: #recorre el archivo
        s = l.split() #Linea de archivo a Lista
        if session['username'] in s:
            grupos.append(s[0])
    archivo.close()
    return grupos

def lengroups():
#Devuelve la longitud de cada grupo en los que SI está el usuario.
    lengroups = []
    archivo = open('grupos.txt','r+')
    for l in archivo: #recorre el archivo
        s = l.split() #Linea de archivo a Lista
        if session['username'] in s:
            lengroups.append(len(s)-1)
    archivo.close()
    return lengroups

def procegroupN():
#Devuelve los grupos en los que NO está el usuario.
    grupos = []
    archivo = open('grupos.txt','r+')
    for l in archivo: #recorre el archivo
        s = l.split() #Linea de archivo a Lista
        if session['username'] not in s:
            grupos.append(s[0])
    archivo.close()
    return grupos

def lengroupsN():
#Devuelve la longitud de cada grupo en los que NO está el usuario.
    lengroups = []
    archivo = open('grupos.txt','r+')
    for l in archivo: #recorre el archivo
        s = l.split() #Linea de archivo a Lista
        if session['username'] not in s:
            lengroups.append(len(s)-1)
    archivo.close()
    return lengroups    

def checkExist(name):
#Recibe un nombre(grupo o usuario). Devuelve True si el nombre está en uso y False si no.    
    archivo = open('registro.txt','r+')
    
    reservednames = ["Meat","Vegetables","Fish","Pasta","Soccer","Golf",
                    "Tennis","Tejo","VideoGames","Shopping","Party",
                    "GetHigh","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    if name in reservednames:
        return True


    for l in archivo: #recorre el archivo
        s = l.split() #Linea de archivo a Lista
        if (name == s[0]): # if User exists
            archivo.close() 
            return True

    archivoG = open('grupos.txt','r+')
    for l in archivoG: #recorre el archivo
        s = l.split() #Linea de archivo a Lista
        if (name == s[0]): # if Name exists
            archivoG.close()
            return True  
            
    archivoG.close()
    archivo.close()
    return False

def checkPreferences(name):
#Recibe un nombre. Devuelve True si el ususario ya tiene las preferences configuaradas.

    archivo = open('preferencias.txt', 'r+')

    for l in archivo: #recorre el archivo
        s = l.split() #Linea de archivo a Lista
        if (name == s[0]): # if User exists
            archivo.close() 
            return True

    archivo.close()
    return False

def checkUserinGroup(name):
#Check si el user está en un grupo especifico
    archivo = open('grupos.txt','r+')
    for l in archivo: #recorre el archivo
        s = l.split() #Linea de archivo a Lista
        if s[0] == name:
            if session['username'] in s:
                return True
    archivo.close()
    return False

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
###############################################################################################################
###############################################################################################################
###############################################################################################################




        
@app.route("/", methods=['GET', 'POST'])
def login():
    if 'logged_in' in session: #Si está log in, entonces lo redirige a home.
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = request.form['Username'] 
        password = request.form['password'] 
        archivo = open('registro.txt','r+') 
        for l in archivo: 
            s = l.split() 
            if(user == s[0] and password == s[1]):
                print('lOG IN! CONGRAATS')
                session['logged_in'] = True
                session['username'] = user
                return redirect(url_for('preferences'))
                # https://youtu.be/QEMtSUxtUDY?t=1396
        archivo.close()
    return render_template('login.html')


# Revisa si está log in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/preferences", methods=['GET', 'POST'])
@is_logged_in
def preferences():
    msg = None

    days = ""
    #Comprobar que no se ha configurado las preferencias antes
    if checkPreferences(session['username']):
        return redirect(url_for('index'))

    if request.method == 'POST':
        food = request.form['food']
        hobby = request.form['hobby']
        sport = request.form['sport']
        Hfood = request.form['Hfood']
        Hhobby = request.form['Hhobby']
        Hsport = request.form['Hsport']

        #No pueden existir cosas que ame y odie a la misma vez
        if (Hfood == food or sport == Hsport or hobby == Hhobby):
            msg = "Same thing u hate and love? That's crazy bro... change it"
            return render_template('preferences.html',msg = msg)

        #Se usa un try porque cuando no se envian valores en algun dia, da error python
        for i in ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]:
            try:
                day1 = request.form[i]
            except:
                days += ""
            else:
                days += " " + i            

        archivo = open('preferencias.txt','a')        
        archivo.write(session['username'] + ' ') 
        archivo.write(food + ' ' + hobby + ' ' + sport + days + '\n')
        archivo.close()

        archivo = open('nopreferencias.txt','a')        
        archivo.write(session['username'] + ' ') 
        archivo.write(Hfood + ' ' + Hhobby + ' ' + Hsport + '\n')
        archivo.close()

        return redirect(url_for('index'))

        
    return render_template('preferences.html')



@app.route("/home", methods=['GET', 'POST'])
@is_logged_in
def index():


    msj = {'done': ''}
    if request.method == 'POST':
    #CODIGO PARA REMOVERSE DEL GRUPO
        njoin = request.form["njoin"]
        # with is like your try .. finally block in this case
        with open('grupos.txt', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
        
        archivo = open('grupos.txt','r+')
        for index, l in enumerate(archivo): #recorre el archivo
            s = l.split() #Linea de archivo a Lista
            if njoin in s and session['username'] in s:
                
                if (len(s) <= 2): #Si hay solo 2 datos(el nombre de grupo y el ultimo usuario) entonces lo borra.
                    linea = ''
                    data[index] = linea
                else:
                    linea = re.sub('[^A-Za-z0-9]+', ' ', data[index])
                    linea = linea.replace(session['username'],'') #Reemplaza el usuario por vacio.
                    data[index] = linea + "\n" # Es para quitar el caracter especial de \n  y poder hacerlo de manera correcta 
                
                
                archivo.close()
                
                # and write everything back
                with open('grupos.txt', 'w') as file:
                    file.writelines( data )
                done = True
                msj = {'done': done}
                return render_template('group.html', len = len(procegroup()), grupos = procegroup(), lengroups = lengroups(), msj=msj)   
    
    return render_template('group.html', len = len(procegroup()), grupos = procegroup(), lengroups = lengroups()) 
















#############CALENDARIO #########################
actividades = [[0,"Welcomeeeee!!!!"]]
diaElegido = 0

@app.route("/see/<name>/<diaa>", methods = ["GET","POST"])
@is_logged_in
def see(name,diaa):
    if checkUserinGroup(name):
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
                nuevaActividad = [int(diaa), request.form['crearActividad']]
                actividades.append(nuevaActividad)

                diaElegido = int(diaa)
                if int(diaElegido) < 10:
                    diaWrite = "0" + str(diaElegido)
                else:
                    diaWrite = diaElegido
                        
                if int(mes) < 10:
                    mes = "0" + str(mes)

                archivo = open('groups/'+name+ '.txt','a+')        
                archivo.write(str(diaWrite) +"/" +str(mes)+"/"+str(anio)+" "+request.form['crearActividad']+"\n") 
                archivo.close()                
  
#COMO HACEEER VOTACIONES??????????????????????

            else:
                diaElegido = int(boton)
            if actividades != []:
                
                try:    
                    archivo2 = open('groups/'+ name + '.txt','r+')

                except:
                    archivo2 = open('groups/'+ name + '.txt','w+')

                for l in archivo2: 
                    s = l.split() 
                    dia = str(s[0][0]) + str(s[0][1])
                    
                    if dia[0] == "0":
                        dia = dia[1]

                    if(int(dia) == diaElegido):
                        actividadesDelDia.append(l)
                        hayActividades = True                       

                archivo2.close()

        return render_template("see.html",datos={"calendario":calendario,
                                                  "mes":mes,
                                                  "anio":anio,
                                                  "actividades":actividadesDelDia,
                                                  "hayActividades":hayActividades,
                                                  "diaElegido":diaElegido,
                                                  "presionoDia":True,
                                                  "name":name})


 
    else:
        print("No está")
        return redirect(url_for('index'))

    

#############CALENDARIO #########################




@app.route("/JGroup", methods=['GET', 'POST'])
@is_logged_in
def JGroup():
    msj = {'done': ''}
    if request.method == 'POST':
        njoin = request.form["njoin"]

        # with is like your try .. finally block in this case
        with open('grupos.txt', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
        
        archivo = open('grupos.txt','r+')
        for index, l in enumerate(archivo): #recorre el archivo
            s = l.split() #Linea de archivo a Lista
            if njoin in s:
                data[index] = re.sub('[^A-Za-z0-9]+', ' ', data[index]) + session['username'] + "\n" # Es para quitar el caracter especial de \n  y poder hacerlo de manera correcta 
                archivo.close()
                # and write everything back
                with open('grupos.txt', 'w') as file:
                    file.writelines( data )
                done = True
                msj = {'done': done}
                return render_template('JGroup.html', len = len(procegroupN()), grupos = procegroupN(), lengroups = lengroupsN(), msj=msj)       
              
    return render_template('JGroup.html', len = len(procegroupN()), grupos = procegroupN(), lengroups = lengroupsN(), msj=msj)




@app.route("/NewGroup", methods=['GET', 'POST'])
@is_logged_in
def NewGroup():
    msj = {'exists': ""}
    if request.method == 'POST':
        groupname = request.form['groupname']

        archivo = open('grupos.txt','a')
                 
        if checkExist(groupname):
            exists = True
            msj = {'exists': exists} #Name exists
            archivo.close()
            return render_template('NewGroup.html', msj=msj)            

        archivo.write(groupname + ' ') 
        archivo.write(session['username'] + "\n")
        done = True
        msj = {'done': done}
        archivo.close()
        return redirect(url_for('index'))

    return render_template('NewGroup.html', msj=msj)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'logged_in' in session: #Si está log in, entonces lo redirige a home.
        return redirect(url_for('index'))    
    msj = {'exists': ""}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        archivo = open('registro.txt','a')

        if checkExist(username):
            exists = True
            msj = {'exists': exists} #User exists
            archivo.close()
            return render_template('register.html', msj=msj) 
        
        archivo.write(username + ' ') 
        archivo.write(password + "\n")
        done = True
        msj = {'done': done}
        archivo.close()
        return redirect(url_for('login'))
    return render_template('register.html', msj=msj)


if __name__ == '__main__':
    app.secret_key='ajbertin'
    app.run(debug=True)

