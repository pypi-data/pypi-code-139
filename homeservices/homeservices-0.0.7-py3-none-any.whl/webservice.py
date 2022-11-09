from flask import Flask, request, jsonify, make_response
from flask_compress import Compress
from influxdb import InfluxDBClient, client
from urllib import parse

class HomeServices:

    def __init__(self,  template_folder, static_folder):
        self.app = Flask(__name__,  template_folder=template_folder, static_folder=static_folder)
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.app.add_url_rule('/alexaintent', 'alexaintent', self.alexa_intent, methods=['GET'])
        Compress(self.app)

        host = 'pi02'
        user = 'writer'
        password = '24$Qw7LVRjOI'
        bucket = 'hometelemetry'

        self.influx_conn = InfluxDBClient(host=host, username=user, password=password, database=bucket)

    def getApp(self):
        return self.app

    def run(self):
        self.app.run()

    def index(self):
        return 'This is the Pi server.'

    def alexa_intent(self):
        if request.method == 'GET':
            # Parse GET param
            sensor = parse.parse_qs(parse.urlparse(request.url).query)['sensor'][0]

            sensor_table = {'jardin': 2, 'salón': 1, 'buhardilla': 3}

            if sensor in sensor_table.keys():
                query = "SELECT * from DHT22 WHERE sensorid='{}' ORDER BY time DESC LIMIT 1".format(sensor_table[sensor])
                result_set = self.influx_conn.query(query)
                points = list(result_set.get_points())

                response_dict = "La temperatura es de {} grados, y la humedad es del {:0f} por ciento."\
                                .format(points[0]['temp'], points[0]['humidity'])
            else:
                response_dict = "Ese sensor es desconocido"

            response = make_response(response_dict.encode('UTF-8'))
            response.mimetype = "text/plain"
            response.headers['Pragma'] = 'no-cache'
            response.headers["Expires"] = 0
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response


