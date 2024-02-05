#!/usr/bin/python3
"""
Handles RESTFul API actions for review
"""

from flask import abort
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models.place import Place
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def all_place_amenities(place_id):
    """
    Returns all amenities in a place
    """
    place = storage.get("Place", place_id)
    if place:
        amenities = place.amenities
        list_amenities = []
        for amenity in amenities:
            list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an amenity of a place
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    place_amenities = place.amenities
    for amenity in place_amenities:
        if amenity.id == amenity_id:
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'],
                 strict_slashes=False)
def add_place_amenity(place_id, amenity_id):
    """
    Adds an amenity to a place
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    place_amenities = place.amenities
    for amenity in place_amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
