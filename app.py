from flask import Flask, jsonify, request, json
from flask_cors import CORS

# Crear aplicación de tipo Flask
app = Flask(__name__)

# Permite que cualquier cliente se pueda conectar a esta aplicación de tipo REST API
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ruta simple que puede ser una pagina web
@app.route("/") # localhost:5000/ GET
def root():
    # Devuelve texto
    return "root"

# Ruta para listar recursos al cliente
@app.route("/api/sensores") # localhost:5000/api/sensores GET
def get_sensores():
    
    f = open('db.json')
    json_data = json.load(f)
    f.close()
    
    # Devuelve el diccionario convertido en JSON
    return jsonify(json_data["sensores"]), 200

# Ruta para crear un recurso
@app.route("/api/sensores", methods=['POST']) # localhost:5000/api/sensores/ POST
def post_sensores():
    f = open('db.json', "+r")
    json_data = json.load(f)
    
    post_data = request.get_json()
    json_data["sensores"].append(post_data)

    new_json = json.dumps(json_data)
    
    f.seek(0)
    f.truncate()
    f.write(new_json)
    
    f.close()
    
    # Devuelve el diccionario convertido en JSON, pero este incluye el nuevo objeto ingresado
    return jsonify(json_data["sensores"]), 201


# Cosa que esta en la mayoria de los proyectos de Python pero no se para que sirve 
if __name__ == '__main__':
    app.run(debug=True)

