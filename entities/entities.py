# Clases

class SensorData(sqlalchemy_client.Model):
    id = sqlalchemy_client.Column(sqlalchemy_client.Integer, primary_key=True),
    sensor_mac = sqlalchemy_client.Column(sqlalchemy_client.String(20)),
    data = sqlalchemy_client.Column(sqlalchemy_client.String(20))

    def __init__(self, sensor_mac, data):
        self.sensor_mac = sensor_mac
        self.data = data


class Sensor(sqlalchemy_client.Model):
    id = sqlalchemy_client.Column(sqlalchemy_client.Integer, primary_key=True),
    name = sqlalchemy_client.Column(sqlalchemy_client.String(50)),
    mac_addr = sqlalchemy_client.Column(sqlalchemy_client.String(20)),
    description = sqlalchemy_client.Column(sqlalchemy_client.String(150)),
    topic = sqlalchemy_client.Column(sqlalchemy_client.String(70))

    def __init__(self, name, mac_addr, description, topic):
        self.name = name
        self.mac_addr = mac_addr
        self.description = description
        self.topic = topic

sqlalchemy_client.create_all()

class SensorSchema(marshmallow_client.Schema):
    class Meta:
        fields = ('id', 'name', 'mac_addr', 'description', 'topic')

class SensorDataSchema(marshmallow_client.Schema):
    class Meta:
        fields = ('id', 'sensor_mac', 'data')

sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)

sensordata_schema = SensorDataSchema()
sensorsdata_schema = SensorDataSchema(many=True)

# Clases