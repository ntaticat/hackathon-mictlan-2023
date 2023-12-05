from flask import Flask, jsonify, request, json
from flask_cors import CORS
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

mqtt = Mqtt()
db = SQLAlchemy()
ma = Marshmallow()

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


class SensorSchema(ma.Schema):
    class Meta:
        fields = ('sensor_id', 'name', 'mac_addr', 'description', 'topic')

class SensorDataSchema(ma.Schema):
    class Meta:
        fields = ('sensordata_id', 'sensor_mac', 'data')

sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)

sensordata_schema = SensorDataSchema()
sensorsdata_schema = SensorDataSchema(many=True)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to mqtt successfully')
        mqtt.subscribe('flask/esp32/#')
    else:
        print('Bad connection. Code:', rc)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    sensor_topic = message.topic
    sensor_data = message.payload.decode()

    new_sensordata = SensorData('wea', sensor_data)

    db.session.add(new_sensordata)
    db.session.commit()

    print('Received message on topic: {topic} with payload: {payload}'.format(**data))

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    if level == MQTT_LOG_ERR:
        print('Error: {}'.format(buf))

@app.route("/api/sensors")
def get_sensores():
    return sensors_schema.jsonify(Sensor.query.all()), 200

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

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ntaticat:Password123!@localhost/flaskmysql'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MQTT_BROKER_URL'] = 'localhost'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 5
    app.config['MQTT_TLS_ENABLED'] = False

    mqtt.init_app(app=app)
    db.init_app(app=app)
    ma.init_app(app=app)

    app.app_context().push()
    db.create_all()