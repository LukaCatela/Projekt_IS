from flask import Flask, render_template, request, jsonify,make_response
from pony import orm
from datetime import datetime, time

db = orm.Database()

app = Flask(__name__, static_url_path='/static')


class Konzultacije(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    JMBG_student = orm.Required(str)
    id_profesor = orm.Required(int)
    id_predmet = orm.Required(int)
    naziv_predmet = orm.Required(str)
    soba = orm.Required(str)
    vrijeme = orm.Required(time)
    datum = orm.Required(datetime)


db.bind(provider="sqlite", filename="konzultacije.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

@app.route("/prijava.html", methods=["POST","GET"])
def dodaj_prijavu():
        return make_response(render_template("prijava.html"),200)

@app.route("/", methods=["GET"])
def home():
    return make_response(render_template("index.html"),200)

if __name__ == '__main__':
    app.run(port=8080)
