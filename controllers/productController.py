from flask import jsonify, request
from models.schemas.productionSchema import production_schema
from marshmallow import ValidationError
from services import productionService

def save():
    if request.json is None:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        production_data = production_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        production_save = productionService.save(production_data)
        return production_schema.jsonify(production_save), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500
