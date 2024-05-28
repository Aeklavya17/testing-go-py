import json

from flask import Response
from marshmallow import Schema, fields, validate

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str()


    def jsonify(self, new_item):
        """
           Serialize data to JSON and create a Flask Response object with the JSON data.
           :param data: The data to be serialized.
           :param status_code: The HTTP status code to be returned (default is 200).
           :return: Flask Response object with JSON data and Content-Type header.
           """
        json_data = json.dumps(new_item)
        response = Response(json_data, content_type='application/json')
        return response


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
