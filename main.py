import flask
import random
import mysql.connector
import datetime
import Columns
import os
import pandas
import numpy
import matplotlib
import requests


#Debugging
import traceback
import sys

global sexbefore
sexbefore = False

querySAPID = "SELECT SAPID FROM KRK_Tabelle"
app = flask.Flask(__name__,
                  template_folder="templates",
                  static_folder="static")
app.secret_key = "x5xSsB$JDwGe%iEMLp6R4p9D&zv2$Xi2m7tCvNgn3PUmaqPH&EqbZvrx#v8YEH69wXxbmYoEQ68nE!7qs*aUqgd6Qsr6BRfSPJ45fztH4K*dHVhBR9UgFJniygvQS6hq"


#Workaround für ältere Browser
@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico',
                                     mimetype='image/vnd.microsoft.icon')


@app.route('/android-chrome-192x192.png')
def favicon_chrome_192():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'android-chrome-192x192.png')


@app.route('/android-chrome-256x256.png')
def favicon_chrome_256():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'android-chrome-256x256.png')


@app.route('/browserconfig.xml')
def favicon_browserconfig():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'browserconfig.xml')


@app.route('/apple-touch-icon.png')
def favicon_apple_touch():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'apple-touch-icon.png')


@app.route('/mstile-150x150.png')
def favicon_mstile():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'mstile-150x150.png')


@app.route('/safari-pinned-tab.svg')
def favicon_safari_pinned():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'safari-pinned-tab.svg')


@app.route('/site.webmanifest')
def favicon_webmanifest():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'site.webmanifest')


@app.route('/', methods=['POST', 'GET'])
def login():
    error = ''
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        pwd = flask.request.form['password']
        try:
            global mydb
            mydb = mysql.connector.connect(host="fogg.sglorch.de",
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
    if ("username" in flask.session):
        return flask.render_template('site_1.html',
                                     Topnav=True,
                                     startseite=True)
    else:
        return flask.redirect(flask.url_for('login'))


@app.route("/dateneingabe", methods=["POST", "GET"])
def dateneingabe():
    if not "username" in flask.session:
        return flask.redirect(flask.url_for('login'))

    #Import von Daten
    if "Import" in flask.request.form:
        print("In Import")
        IDToFind = flask.request.form["sapidimport"]
        if IDToFind.isnumeric():
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM KRK_Tabelle WHERE SAPID = %(sapid)s",
                           {'sapid': IDToFind})
            myresult = cursor.fetchone()
            if myresult is None:
                # Wenn SAP ID nicht in Datenbnak
                return flask.render_template('site_2.html',
                                             Topnav=True,
                                             startseite=False,
                                             error="SAP ID nicht gefunden")

            print(myresult)
            import_var = {
                'sapid': myresult[0],
                'geschlecht': myresult[1],
                'geburt': datetime.datetime.strftime(myresult[2], "%d.%m.%Y")
            }
            print(import_var)
            return flask.render_template('site_2.html',
                                         Topnav=True,
                                         startseite=False,
                                         import_var=import_var)

    #Schreiben von daten
    if "Schreiben" in flask.request.form:
        print("In Input")
        if ("username" not in flask.session):
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

            Age = flask.request.form['geburt']
            try:
                Age = datetime.datetime.strptime(Age, "%d.%m.%Y")
                if (Age > datetime.datetime.now()):
                    return flask.render_template('site_2.html',
                                                 Topnav=True,
                                                 startseite=False,
                                                 error="Datum überprüfen")
            except:
                #NotAllowed("Datum überprüfen", False,False)
                return flask.render_template('site_2.html',
                                             Topnav=True,
                                             startseite=False,
                                             error="Datumsformat falsch")

            sex = flask.request.form['geschlecht']
            SAPID = SAPID = flask.request.form['sapid']

            if (SAPID.isnumeric()):
                numbers = [int(SAPID)]
            else:
                #NotAllowed("SAPID falsch",False,False)

                return flask.render_template('site_2.html',
                                             Topnav=True,
                                             startseite=False,
                                             error="SAP ID ist keine Zahl")

            if (sex == "" or SAPID == "" or Age == ""):
                #NotAllowed("Eingabe inkomplett",False,False)
                return flask.render_template('site_2.html',
                                             Topnav=True,
                                             startseite=False,
                                             error="Eingabe einkomplett")
                #Check if SAPID already in system

            cursor = mydb.cursor()
            cursor.execute(querySAPID)
            sid = cursor.fetchall()
            print(sid)

            for ids in sid:
                print(ids)
                if ids == (int(SAPID), ):
                    try:
                        dt_string = datetime.datetime.now().strftime(
                            "%Y/%m/%d %H:%M:%S")
                        val = (int(SAPID), sex, Age, dt_string, int(SAPID))
                        cursor.execute(Columns.sql_update, val)
                        mydb.commit()
                        return flask.render_template(
                            'site_2.html',
                            Topnav=True,
                            startseite=False,
                            success="Daten überschrieben")
                    except:
                        return flask.render_template(
                            'site_2.html',
                            Topnav=True,
                            startseite=False,
                            error="Konnte nicht in Datenbank geschrieben werden"
                        )

            #Insert the new data into the SQL Database
            try:
                dt_string = datetime.datetime.now().strftime(
                    "%Y/%m/%d %H:%M:%S")
                print(dt_string)
                val = (int(SAPID), sex, Age, dt_string)
                cursor = mydb.cursor()
                cursor.execute(Columns.sql, val)
                mydb.commit()

                return flask.render_template('site_2.html',
                                             Topnav=True,
                                             startseite=False,
                                             success="Eingabe erfolgreich")

            except Exception as e:
                print(e)
                #NotAllowed("Fehler", False)
                return flask.render_template(
                    'site_2.html',
                    Topnav=True,
                    startseite=False,
                    error="Konnte nicht in Datenbank geschrieben werden")
            #Merging both dataframes

        return flask.render_template('site_2.html',
                                     Topnav=True,
                                     startseite=False)

    #end of test for buttons
    return flask.render_template('site_2.html', Topnav=True, startseite=False)


@app.route("/export")
def export_to_csv():
    if flask.session["df"]:
        df = pandas.read_json(flask.session.get('df'))
        print(df)
        output = flask.make_response(df.to_csv(date_format="%d.%m.%Y"))
        output.headers[
            "Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    else:
        return flask.redirect(flask.url_for('page_3'))


@app.route("/datenausgabe", methods=['POST', 'GET'])
def page_3():
    if ("username" in flask.session):
        # dateneingabelogik
        if "datenausgabe" in flask.request.form:
            print("hi")

            cursor = mydb.cursor()
            dfcolumns = Columns.d

            def Analyse() -> pandas.DataFrame:

                global sql
                sql = "SELECT * FROM KRK_Tabelle "
                global firstsql
                firstsql = False

                #SAP ID Finden
                def CheckSQL(sex):
                    global firstsql
                    global sql
                    global sexbefore

                    if firstsql == False:
                        sql += "WHERE "
                        firstsql = True
                        return
                    if firstsql == True:
                        if sex:
                            if sexbefore == False:
                                sql += "AND ("
                                sexbefore = True
                            else:
                                sql += "OR "
                        else:
                            sql += "AND "
                            return

                try:
                    sapid = flask.request.form["sapcheck"]
                except:
                    sapid = ""
                if sapid:
                    try:
                        IDin = flask.request.form["sapid"]
                    except:
                        IDin = ""
                    if IDin != "":
                        if IDin.isnumeric():
                            CheckSQL(False)
                            sql += "SAPID = " + str(IDin) + " "

                # Geschlecht finden
                try:
                    sexcheck = flask.request.form["sexcheck"]
                except:
                    sexcheck = ""

                if sexcheck:

                    try:
                        mann = flask.request.form["männlichcheck"]
                    except:
                        mann = ""
                    if mann:
                        CheckSQL(True)
                        sql += "Geschlecht = 'Männlich' "
                    try:
                        frau = flask.request.form["weiblichcheck"]
                    except:
                        frau = ""
                    if frau:
                        CheckSQL(True)
                        sql += "Geschlecht = 'Weiblich' "
                    try:
                        divers = flask.request.form["diverscheck"]
                    except:
                        divers = ""
                    if divers:
                        CheckSQL(True)
                        sql += "Geschlecht = 'Divers' "
                    if sexbefore == True:
                        sql += ")"

                    # alter Finden
                try:
                    datum = flask.request.form["geburtcheck"]
                except:
                    datum = ""
                if datum:
                    print("In Alt schleife")
                    try:
                        von = flask.request.form["von_geburt"]
                    except:
                        von = ""
                    try:
                        date = datetime.datetime.strptime(von,'%d.%m.%Y')
                        date = datetime.datetime.strftime(date, "%Y-%m-%d")
                        print(date)
                        isadate = True
                    except Exception as e:
                        print(e)
                        isadate = False
                    if isadate == False:
                        von = "1900 - 1 - 1"
                    else:
                        von = date
                    CheckSQL(False)
                    sql += "Geburtsdatum > '" + str(von) + "' "
                    try:
                        bis = flask.request.form["bis_geburt"]
                    except:
                        bis == ""
                    try:
                        date2 = datetime.datetime.strptime(bis,'%d.%m.%Y')
                        date2 = datetime.datetime.strftime(date2, "%Y-%m-%d")
                        print(bis)
                        isadate2 = True
                    except Exception as e:
                        print("fehler bei date2")
                        print(e)
                        isadate2 = False
                    if isadate == True:
                        bis = datetime.date.today().strftime("%Y-%m-%d")
                    else:
                        bis = date2
                    CheckSQL(False)
                    sql += "Geburtsdatum < '" + bis + "' "


                print(sql)
                cursor.execute(sql)
                myresult = cursor.fetchall()
                df = pandas.DataFrame(myresult, columns=dfcolumns)
                df = df.drop(columns=["LastChanged"])
                print(df.dtypes)
                df["Geburtsdatum"] = pandas.to_datetime(df["Geburtsdatum"])
                df['Geburtsdatum'] = df['Geburtsdatum'].dt.strftime('%d.%m.%Y')
                dfjson = df.to_json(date_format="%d.%m.%Y")
                print("df_to_json: " + dfjson)
                flask.session['df'] = dfjson
                print("from session: ")
                print(flask.session.get("df"))
                return df

            #Process output

            df = Analyse()
            #Darstellung der Tabelle
            print(df)

            cell_hover = {  # for row hover use <tr> instead of <td>
                'selector': 'td:hover',
                'props': [('background-color', '#ffffb3')]
            }
            index_names = {
                'selector': '.index_name',
                'props':
                'font-style: italic; color: darkgrey; font-weight:normal;'
            }
            headers = {
                'selector': 'th:not(.index_name)',
                'props': 'background-color: #000066; color: white;'
            }

            htmltext = flask.Markup(
                df.style.set_table_styles([
                    cell_hover,
                    index_names,
                    headers,
                    {
                        'selector': 'th.col_heading',
                        'props': 'text-align: center;'
                    },
                    {
                        'selector': 'th.col_heading.level0',
                        'props': 'font-size: 1.5em;'
                    },
                    {
                        'selector': 'td',
                        'props': 'text-align: center; font-weight: bold;'
                    },
                ],
                                          overwrite=False).to_html())
            

            return flask.render_template('site_3.html',
                                         Topnav=True,
                                         startseite=False,
                                         htmltext=htmltext)

            #def export():
            # datapath1 = Config.SaveFile(fenster)
            #print(datapath1)
            #df = Analyse()
            #print("dataframe for export: ")
            #print(df)
            #df.to_csv(datapath1)

            #weiterleitung zum Datenanalyse
            if "analysebutton" in flask.request.form:
                # Datenbankvariable zur analyse noch setzen
                return flask.redirect(flask.url_for('page_4'))

        return flask.render_template('site_3.html',
                                     Topnav=True,
                                     startseite=False)
    else:
        return flask.redirect(flask.url_for('login'))


@app.route("/datenanalyse", methods=['POST', 'GET'])
def page_4():
    if ("username" in flask.session):
        return flask.render_template('site_4.html',
                                     Topnav=True,
                                     startseite=False)
    else:
        return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
