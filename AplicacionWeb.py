from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)
listasPersonas = []

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="J1057603278p",
    database="sabadoJulio"
)
cursor = db.cursor(dictionary=True)

query = "SELECT * FROM personas"


@app.route('/mensaje', methods=['GET'])
def mensaje():
    return "Primera aplicacion web"


@app.route('/listarPersonas', methods=['GET'])
def listar():
    return jsonify(listasPersonas)


@app.route('/agregarPersona', methods=['POST'])
def agregar():
    nuevaPersona = request.json.get('persona')
    listasPersonas.append(nuevaPersona)
    cursor.execute("INSERT INTO personas (identificacion, nombre, edad) VALUES (%s, %s, %s)",
                   (nuevaPersona['identificacion'], nuevaPersona['nombre'], nuevaPersona['edad']))
    db.commit()
    return 'Nueva Persona agregada correctamente'


@app.route('/datosDeLaData', methods=['GET'])
def datosBase():
    cursor.execute(query)
    resultadosPersonas = cursor.fetchall()
    return jsonify(resultadosPersonas)


@app.route('/buscarPersona/<identificacion>', methods=['GET'])
def buscar(identificacion):
    cursor.execute(
        "SELECT * FROM personas WHERE identificacion = %s", (identificacion,))
    resultadoPersona = cursor.fetchall()
    return jsonify(resultadoPersona)


@app.route('/actualizarPersona/<identificacion>', methods=['PUT'])
def actualizar(identificacion):
    datos_nuevos = request.json
    cursor.execute("UPDATE personas SET nombre = %s, edad = %s WHERE identificacion = %s",
                   (datos_nuevos['nombre'], datos_nuevos['edad'], identificacion))
    db.commit()
    return 'Persona actualizada correctamente'


@app.route('/eliminarPersona/<identificacion>', methods=['DELETE'])
def eliminar(identificacion):
    cursor.execute(
        "DELETE FROM personas WHERE identificacion = %s", (identificacion,))
    db.commit()
    return 'Persona eliminada correctamente'


if __name__ == '__main__':
    app.run(debug=True)
