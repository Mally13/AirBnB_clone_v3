#!/usr/bin/python3
"""
Handles RESTFul API actions for review
"""

from flask import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models.review import Review
from models.place import Place
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id):
    """
    Returns all reviews of a place
    """
    place = storage.get("Place", place_id)
    if place:
        reviews = place.reviews
        list_reviews = []
        for review in reviews:
            list_reviews.append(review.to_dict())
        return jsonify(list_reviews)
    abort(404)


@app_views.route("/review/<review_id>", methods=['GET'],
                 strict_slashes=False)
def one_review(review_id):
    """
    Returns a review object based on id
    """
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/review/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a review object based on id
    """
    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """
    Adds a review to a place
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    if 'text' not in data:
        abort(400, "Missing text")

    user_id = data['user_id']
    text = data['text']
    user = storage.get("User", user_id)
    if user:
        new_review = Review(
            place_id=place_id,
            user_id=user_id,
            text=text
            )
        new_review.save()
        return jsonify(new_review.to_dict()), 201
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a review object based on data provided
    """
    review = storage.get("Review", review_id)
    if review:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        keys_to_ignore = [
            "created_at",
            "user_id",
            "id",
            "place_id",
            "updated_at"
            ]
        for k, v in data.items():
            if k not in keys_to_ignore:
                setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200
    abort(404)
