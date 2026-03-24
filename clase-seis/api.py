from flask import Flask, jsonify
 
app = Flask(__name__)
personas = [
    {"id": 1, "nombre": "Juan", "edad": 30},
    {"id": 2, "nombre": "María", "edad": 25},
    {"id": 3, "nombre": "Pedro", "edad": 35}
]
 
@app.route("/api/personas")
def obtener_personas():
    return jsonify(personas)
 
app.run(debug=True)