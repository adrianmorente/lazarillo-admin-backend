import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin


# Create app and connect to database
application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})
application.config["CORS_HEADERS"] = 'Content-Type'
application.config["MONGO_URI"] = 'mongodb://' + \
    os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
    '@' + os.environ['MONGODB_HOSTNAME'] + \
    ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db


# Route to listen to broadcast messages from Lazarillo devices exposing their Websocket server
@application.route("/broadcast", methods=['POST'])
def read_device_broadcast():
    """Read parameters from device and store them into db"""
    name = request.form.get('name')
    version = request.form.get('version')
    address = request.form.get('address')

    # add device to list of websocket servers
    db.devices.insert_one({
        'name': name,
        'version': version,
        'address': address
    })
    return jsonify(message='success'), 201


# Route to receive the devices that exposed their WS server
@application.route("/devices", methods=['GET'])
@cross_origin()
def send_devices():
    """Retrieve devices from database and send them as JSON"""
    device = {}
    response = []

    for item in db.devices.find():
        device = {
            'id': item['_id'].__str__(),
            'name': item['name'],
            'version': item['version'],
            'address': item['address']
        }
        response.append(device)

    return jsonify(status=True, data=response)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT,
                    debug=ENVIRONMENT_DEBUG)
