from flask import request, Flask, jsonify, render_template
import os
from flask_cors import CORS
from funciones import llm_t1, llm_t2, llm_t3, bbdd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=BASE_DIR)
CORS(app)
app.config["DEBUG"] = True

@app.route("/", methods = ["GET"])
def main():
    return render_template("index_3.html")

@app.route("/t1", methods = ["POST"])
def fp():

    data = request.get_json()
    question = data.get("question")

    response = llm_t1(question)

    respuesta_bbdd = bbdd(question,response)

    if respuesta_bbdd == "ok":
        return jsonify({"question": question, "response": response})
    else:
        return jsonify({"error":"Error al preguntar"})
    

@app.route("/t2", methods = ["POST"])
def imf():

    data = request.get_json()
    question = data.get("question")

    response = llm_t2(question)

    respuesta_bbdd = bbdd(question,response)

    if respuesta_bbdd == "ok":
        return jsonify({"question": question, "response": response})
    else:
        return jsonify({"error":"Error al preguntar"})
    

@app.route("/t3", methods = ["POST"])
def ibr():

    data = request.get_json()
    question = data.get("question")

    response = llm_t3(question)

    respuesta_bbdd = bbdd(question,response)

    if respuesta_bbdd == "ok":
        return jsonify({"question": question, "response": response})
    else:
        return jsonify({"error":"Error al preguntar"})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

app.run()