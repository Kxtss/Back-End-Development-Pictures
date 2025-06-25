from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for d in data:
        if d["id"] == id: 
            return jsonify(d), 200
            
    return {"message": f"Picture with id '{id}' not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    
    if not picture or "id" not in picture:
        return jsonify({"message": "Missing picture data or 'id' field"}), 400
    
    for d in data:
        if d["id"] == picture["id"]:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture_data = request.get_json()

    if not updated_picture_data:
        return jsonify({"message": "No data provided for update"}), 400

    found_picture_index = -1
    for i, pic in enumerate(data):
        if pic["id"] == id:
            found_picture_index = i
            break

    if found_picture_index != -1:
        data[found_picture_index] = updated_picture_data
        return jsonify(data[found_picture_index]), 200
    else:
        return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    found_picture_index = -1
    for i, pic in enumerate(data):
        if pic["id"] == id:
            found_picture_index = i
            break

    if found_picture_index != -1:
        data.pop(found_picture_index)
        return "", 204
    else:
        return jsonify({"message": "picture not found"}), 404