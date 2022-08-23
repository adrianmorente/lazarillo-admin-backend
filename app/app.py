import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

# Create app and connect to database
application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + \
    os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
    '@' + os.environ['MONGODB_HOSTNAME'] + \
    ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db


@application.route("/broadcast", methods=['POST'])
# Route to listen to broadcast messages from Lazarillo devices exposing their Websocket server
def read_device_broadcast():
    """Read parameters from device and store them into db"""
    name = request.form.get('name')
    version = request.form.get('version')
    address = request.form.get('address')

    # add device to list of websocket servers
    db.todos.insert_one({
        'name': name,
        'version': version,
        'address': address
    })
    return jsonify(message='success'), 200


@application.route("/", methods=['GET'])
# Route to receive the devices that exposed their WS server
def send_devices():
    """Retrieve devices from database and send them as JSON"""
    # todos = db.todos.find()
    # return jsonify([todo for todo in todos])
    return jsonify(
        status=True,
        message='success'
    )


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT,
                    debug=ENVIRONMENT_DEBUG)
