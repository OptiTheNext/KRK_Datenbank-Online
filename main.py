import flask
import random
import mysql.connector
import datetime
import Columns

#Debugging
import traceback
import sys


querySAPID = "SELECT SAPID FROM KRK_Tabelle"
app = flask.Flask(__name__,
                  template_folder="templates",
                  static_folder="static")
app.secret_key = "VocUqjQUlO"

 

@app.route('/', methods=['POST', 'GET'])
def login():
    error = ''
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        pwd = flask.request.form['password']
        try:
          global mydb
          mydb = mysql.connector.connect(
          host="fogg.sglorch.de",
          user=username,
          password=pwd,
          database="hannes")
          flask.session["username"] = username
          return flask.redirect(flask.url_for('page_1'))
        except:
            error = 'Invalid Credentials. Please try again.'    
    return flask.render_template("login.html", error=error)


@app.route("/startseite")
def page_1():
    if("username" in flask.session):
      return flask.render_template('site_1.html',Topnav = True, startseite= True)
    else:
      return flask.redirect(flask.url_for('login'))

@app.route("/dateneingabe",methods=["POST","GET"])
def input():
  if("username" not in flask.session):
    return flask.redirect(flask.url_for('login'))

  if flask.request.method == 'POST': 
    #def reset(delete):
     # if(delete == True):
      #  if(Age != "" and SAPID != "" and sex != ""):
       #   return flask.render_template('site_1.html',Topnav = True, startseite= True)
        #  print("reset complete")
    #def NotAllowed(texts, overwrite, resetpls):
     # def ueberschreiben():
      #  dt_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
       # val = (int(SAPID),sex,Age,dt_string,int(SAPID))
        #mydb.cursor.execute(Columns.sql_update,val)
        #mydb.commit()
        #flask.render_template('site_2.html',Topnav = True, startseite= True)

      #if(overwrite == True):
       # reset(resetpls)
        #Wie leeren wir jetzt das Form? Maybe einfach über einen reset-Knopf. Dann nur anzeigen, dass erfolgreich eingetragen wurde. dann drückt man halt den Reset Knopf. Der Knopf ist auch schon da.
        # Wo ist der knopf? gerade kann ich die seite nicht anzeigen
      

  
    Age=flask.request.form['geburt']
    try:
      Age = datetime.datetime.strptime(Age,"%d.%m.%Y")
      if(Age > datetime.datetime.now()):
        return flask.render_template('site_2.html',Topnav = True, startseite= False, error ="Datum überprüfen")
    except:
      #NotAllowed("Datum überprüfen", False,False)
      return flask.render_template('site_2.html',Topnav = True, startseite= False, error="Datumsformat falsch")

    sex = flask.request.form['geschlecht']
    SAPID = SAPID = flask.request.form['sapid']
    
    if(SAPID.isnumeric()):
      numbers=[int(SAPID)]
    else:
      #NotAllowed("SAPID falsch",False,False)
      
      return flask.render_template('site_2.html',Topnav = True, startseite= False, error= "SAP ID ist keine Zahl")

    if(sex == "" or SAPID == "" or Age=="" ):
      #NotAllowed("Eingabe inkomplett",False,False)
      return flask.render_template('site_1.html',Topnav = True, startseite= False, error="Eingabe einkomplett")
      #Check if SAPID already in system
    cursor = mydb.cursor()
    cursor.execute(querySAPID)
    sid = cursor.fetchall()
    print(sid)
      
    for ids in sid:
      print(ids)
      if ids == (int(SAPID),):
        print("just updated")
        #NotAllowed("SAPID doppelt", True, False)
        return flask.render_template('site_1.html',Topnav = True, startseite= False, error= "SAP ID Doppelt")
    

    #Insert the new data into the SQL Database
    try:
      dt_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
      print(dt_string)
      val = (int(SAPID),sex,Age, dt_string)
      cursor = mydb.cursor()
      cursor.execute(Columns.sql, val)
      mydb.commit()

      
      return flask.render_template('site_2.html',Topnav = True, startseite= False,success = "Eingabe erfolgreich")
      
      
      
    except Exception as e:
      print(e)
      #NotAllowed("Fehler", False)
      return flask.render_template('site_2.html',Topnav = True, startseite= False, error ="Konnte nicht in Datenbank geschrieben werden")
    #Merging both dataframes
    
  return flask.render_template('site_2.html',Topnav = True, startseite= False)



@app.route("/datenausgabe", methods=['POST', 'GET'])
def page_3():
    if("username" in flask.session):
      return flask.render_template('site_3.html',Topnav = True, startseite= False)
    else:
      return flask.redirect(flask.url_for('login'))


@app.route("/datenanalyse", methods=['POST', 'GET'])
def page_4():
    if("username" in flask.session):
      return flask.render_template('site_4.html',Topnav = True, startseite= False)
    else:
      return flask.redirect(flask.url_for('login'))


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)