from flask import Flask, jsonify, request, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ntaticat:Password123!@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
marshmallow_client = Marshmallow(app)

app.app_context().push()
db.create_all()

class SensorData(db.Model):
    sensordata_id = db.Column(db.Integer, primary_key=True)
    sensor_mac = db.Column(db.String(20))
    data = db.Column(db.String(20))

    def __init__(self, sensor_mac, data):
        self.sensor_mac = sensor_mac
        self.data = data


class Sensor(db.Model):
    sensor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mac_addr = db.Column(db.String(20))
    description = db.Column(db.String(150))
    topic = db.Column(db.String(70))

    def __init__(self, name, mac_addr, description, topic):
        self.name = name
        self.mac_addr = mac_addr
        self.description = description
        self.topic = topic

class SensorSchema(marshmallow_client.Schema):
    class Meta:
        fields = ('sensor_id', 'name', 'mac_addr', 'description', 'topic')

class SensorDataSchema(marshmallow_client.Schema):
    class Meta:
        fields = ('sensordata_id', 'sensor_mac', 'data')

sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)

sensordata_schema = SensorDataSchema()
sensorsdata_schema = SensorDataSchema(many=True)

@app.route("/api/sensors")
def get_sensores():
    return sensors_schema.jsonify(), 200

@app.route("/api/sensors", methods=['POST'])
def post_sensores():
    
    sensor_name = request.json['name']
    sensor_mac_addr = request.json['mac_addr']
    sensor_description = request.json['description']
    sensor_topic = request.json['topic']

    new_sensor = Sensor(sensor_name, sensor_mac_addr, sensor_description, sensor_topic)
    
    db.session.add(new_sensor)
    db.session.commit()
    
    return sensor_schema.jsonify(new_sensor), 201


if __name__ == '__main__':
    app.run(host='192.168.0.166', port=5000, debug=True)