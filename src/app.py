from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def list_single_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_jackson():
    print(request.data)
    data = request.json
    print(data)
    members = jackson_family.add_member(data)
    if members == "added":
        return jsonify('Has creado un nuevo integrante!'), 200
    else:
        return jsonify("Aun no se integra a la familia"), 400

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_jackson(id):
    members = jackson_family.delete_member(id)
    print(members)
    if members == "not found":
        return jsonify('Falleció'), 400
    else: 
        return jsonify(members), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=PORT, debug=True)













