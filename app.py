from flask import Flask, render_template, request, jsonify,make_response
from pony import orm
from datetime import datetime
from itertools import groupby


db = orm.Database()

app = Flask(__name__, static_url_path='/static')

class Konzultacije(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    naziv_profesor = orm.Required(str)
    naziv_predmet = orm.Required(str)
    soba = orm.Optional(str, auto=None)
    datum = orm.Required(datetime)


db.bind(provider="sqlite", filename="konzultacije.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

def format_datum(datum):
    return datum.strftime('%d-%m-%Y') if datum else None
def dodaj_prijavu(json_request):
    try:
        naziv_profesor = json_request.get("profesor")
        naziv_predmet = json_request.get("predmeti")
        soba = json_request.get("mjesto")
        datum = json_request.get("datum")

        if not naziv_profesor or not naziv_predmet or not datum:
            return {"response": "Fail", "error": "Missing required fields"}

        try:
            datum = datetime.fromisoformat(datum)
        except (ValueError, TypeError):
            return {"response": "Fail", "error": "Invalid date format"}

        with orm.db_session:
            Konzultacije(naziv_profesor=naziv_profesor, naziv_predmet=naziv_predmet, soba=soba, datum=datum)
            return {"response": "Success"}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def get_konzultacija():
    try:
        with orm.db_session:
            konzultacije_query = orm.select((k.id, k.naziv_profesor, k.naziv_predmet, k.soba, k.datum)
                                            for k in Konzultacije)[:]
            list_rezultat = []
            for element in konzultacije_query:
                termin_dict = {
                    "id": element[0],
                    "naziv_profesor": element[1],
                    "naziv_predmet": element[2],
                    "soba": element[3],
                    "datum": format_datum(element[4])
                }
                list_rezultat.append(termin_dict)
            response = {"response": "Success", "termini": list_rezultat}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def edit_konzultacija(konzultacija_id, json_request):
    try:
        with orm.db_session:
            to_update = Konzultacije[konzultacija_id]
            if 'naziv_profesor' in json_request:
                to_update.naziv_profesor = json_request['naziv_profesor']
            if 'naziv_predmet' in json_request:
                to_update.naziv_predmet = json_request['naziv_predmet']
            if 'datum' in json_request:
                datum = datetime.strptime(json_request['datum'], '%d-%m-%Y')
                to_update.datum = datum
            if 'soba' in json_request:
                to_update.soba = json_request['soba']

            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


def delete_konzultaciju(konzultacija_id):
    try:
        with orm.db_session:
            konzultacija = Konzultacije[konzultacija_id]
            konzultacija.delete()
            return {"response": "Success"}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

@orm.db_session
def get_obaveze_subject():
    try:
        konzultacije = orm.select(k for k in Konzultacije).order_by(Konzultacije.naziv_predmet)
        group_predmet = groupby(konzultacije, lambda k:k.naziv_predmet)
        rezultat = [{"Predmet": naziv_predmet, "broj_konzultacija": len(list(konzultacije))} for naziv_predmet, konzultacije in group_predmet]

        response = {"response": "Success", "data": {"Predmeti": rezultat}}

        return response

    except Exception as e:
        error_response = {"response": "Error", "error_message": str(e)}
        return error_response


@app.route("/dodaj/konzultaciju", methods=["POST","GET"])
def dodaj_konzultacije():
    if request.method == "POST":
        try:
            json_request = {key: (value if value != "" else None) for key, value in request.form.items()}
            response = dodaj_prijavu(json_request)
            if response["response"] == "Success":
                return make_response(render_template("prijava.html"), 200)
            return make_response(jsonify(response), 400)
        except Exception as e:
            response = {"response": str(e)}
            return make_response(jsonify(response), 400)
    else:
        return make_response(render_template("prijava.html"), 200)
@app.route("/pregled/konzultacije", methods=["GET"])
def pregled():
    try:
        with orm.db_session:
            konzultacije_query = orm.select((k.id, k.naziv_profesor, k.naziv_predmet, k.soba, k.datum)
                                            for k in Konzultacije)[:]
            list_rezultat = []
            for element in konzultacije_query:
                termin_dict = {
                    "id": element[0],
                    "naziv_profesor": element[1],
                    "naziv_predmet": element[2],
                    "soba": element[3],
                    "datum": format_datum(element[4])
                }
                list_rezultat.append(termin_dict)
            response = {"response": "Success", "termini": list_rezultat}
            return make_response(render_template("pregled.html", termini=response["termini"]), 200)
    except Exception as e:
        response = {"response": "Fail", "error": str(e)}
        return make_response(jsonify(response), 400)

@app.route("/vrati/obaveze/vizualizacija", methods=["GET"])
def vizualizacija():
    try:
        chart_data = get_obaveze_subject()

        print(chart_data)

        predmeti = chart_data.get("data", {}).get("Predmeti", [])
        x_axis = [p['Predmet'] for p in predmeti]
        y_axis = [p['broj_konzultacija'] for p in predmeti]

        response = {"response": "Success"}

        if response["response"] == "Success":
            return make_response(render_template("graf.html", y_axis=y_axis, x_axis=x_axis), 200)
        return make_response(jsonify(response), 400)

    except Exception as e:
        error_response = {"response": "Error", "error_message": str(e)}
        return make_response(jsonify(error_response), 500)


@app.route("/konzultacije/<int:konzultacija_id>", methods=["PATCH"])
def uredi_konzultaciju(konzultacija_id):
    try:
        json_request = request.json
    except Exception as e:
        response = {"response": "Invalid JSON format"}
        return make_response(jsonify(response), 400)

    response = edit_konzultacija(konzultacija_id, json_request)
    if response["response"] == "Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)


@app.route("/konzultacije/<int:konozultacija_id>", methods=["DELETE"])
def obrisi_konzultaciju(konozultacija_id):
    response = delete_konzultaciju(konozultacija_id)
    if response["response"] == "Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)

@app.route("/", methods=["GET"])
def home():
    return make_response(render_template("index.html"), 200)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
