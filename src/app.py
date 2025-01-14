"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member),200

@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"message": "Bad request"}), 400
    jackson_family.add_member(data)
    return jsonify({"message": "Member added successfully"}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    jackson_family.delete_member(id)
    return jsonify({"done": True}), 200

# Route to update a family member by id
@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"message": "Bad request"}), 400
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"message": "Member not found"}), 404
    jackson_family.update_member(id, data)
    return jsonify({"message": "Member updated successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
