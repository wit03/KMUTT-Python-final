from flask import Flask, render_template, request
import sqlite3

from API import house_pricing_model

app = Flask(__name__)

conn = sqlite3.connect("database.db")

conn.execute('CREATE TABLE IF NOT EXISTS houses (area REAL, bathrooms NUM, stories NUM, airconditioning NUM, parking NUM, prefarea TEXT)')


app.register_blueprint(house_pricing_model.api)
if house_pricing_model.API_EXIST:
    print("API loaded")
else:
    print("API not found")

@app.route('/', methods=['GET'])
def renderIndex():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * from houses")

    rows = cur.fetchall()
    return render_template("index.html", rows= rows)


@app.route('/sell')
def renderSell():
    return render_template("sell.html")


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        msg = ""
        try:
            area = request.form['area']
            bathrooms = request.form['bathrooms']
            stories = request.form['stories']
            airconditioning = request.form['airconditioning']
            parking = request.form['parking']
            prefarea = request.form['prefarea']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    f"INSERT INTO houses (area, bathrooms, stories, airconditioning, parking, prefarea) VALUES ({area},{bathrooms},{stories},{airconditioning},{parking},'{prefarea}')")
                con.commit()
                msg = "Sell Record successfully added"
        except:
            con.rollback()
            msg = "There's some problem"

        finally:
            con.close()
            return render_template("sell-result.html", msg=msg)

@app.route('/calculation', methods=['GET'])
def testapi():
    return render_template("price-cal.html")
