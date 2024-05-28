import logging
import os

from flask import Blueprint, jsonify, request, abort, render_template, after_this_request, send_file
from werkzeug.security import safe_join

from app.services.item_service import ItemService
from app.schemas.item_schema import ItemSchema
from flask_restx import Namespace, Resource,Api
from flask_swagger_ui import get_swaggerui_blueprint


item_bp = Blueprint('item_bp', __name__)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

api = Api(item_bp, version='1.0', title='Items API', description='CRUD operations on items')
item_ns = api.namespace('items', description='Operations related to items')
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


@item_bp.route('/', methods=['GET'])
@item_ns.doc('list_items')
def get_items():
    """
    Get all items
    :return:
    """
    items = ItemService.get_all_items()
    logging.info(f"Request Recieved: / , Method: {request.method}, Result: {items}")
    return render_template('item_list.html', items=items)


@item_bp.route('/<int:item_id>', methods=['GET'])
@item_ns.doc('create_item')
@item_ns.expect(item_schema)
@item_ns.marshal_with(item_schema, code=201)
def get_item(item_id):
    try:
        item = ItemService.get_item_by_id(item_id)
        if item:
            return render_template('item_detail.html', item=item)
        else:
            abort(404, description="Item not found")
    except Exception as e:
        logging.error("Excepation at get_item {}".format(item_id))
        raise e
    finally:
        abort(404, description="Item Nahi h re")

@item_bp.route('/', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        abort(400, description="Bad Request: Missing 'name'")

    new_item = str(ItemService.create_item(request.json))
    return item_schema.jsonify(new_item), 201

@item_bp.route('/pass', methods=['POST'])
def create_item_pass():
    if not request.json or not 'name' in request.json:
        abort(400, description="Bad Request: Missing 'name'")

    new_item = str(ItemService.create_item(request.json))
    return item_schema.jsonify("New Item"), 201


@item_bp.route('/<int:item_id>', methods=['PUT'])
@item_ns.doc('update_item')
@item_ns.expect(item_schema)
@item_ns.response(404, 'Item not found')
@item_ns.marshal_with(item_schema)
def update_item(item_id):
    item = ItemService.get_item_by_id(item_id)
    if not item:
        abort(404, description="Item not found")

    if not request.json:
        abort(400, description="Bad Request: Missing request body")

    updated_item = str(ItemService.update_item(item, request.json))
    return item_schema.jsonify(updated_item), 200


@item_bp.route('/<int:item_id>', methods=['DELETE'])
@item_ns.doc('delete_item')
@item_ns.response(204, 'Item deleted')
@item_ns.response(404, 'Item not found')
def delete_item(item_id):
    item = ItemService.get_item_by_id(item_id)
    if not item:
        abort(404, description="Item not found")

    ItemService.delete_item(item)
    return '', 204

@item_bp.route('/divide', methods=['DELETE'])
def divide():
    try:
        data = request.get_json()
        numerator = data['numerator']
        denominator = data['denominator']
        result = numerator / denominator

        # Log successful request
        logging.info(f"Request: /divide, Method: {request.method}, Data: {data}, Result: {result}")

        return jsonify({'result': result}), 200
    except KeyError as e:
        # Log error for missing key in request data
        logging.error(f'Missing key in request data: {e}')
        return jsonify({'error': 'Missing key in request data'}), 400
    except ZeroDivisionError as e:
        # Log error for division by zero
        logging.error(f'Division by zero: {e}')
        return jsonify({'error': 'Division by zero'}), 400
    except Exception as e:
        # Log unexpected errors
        logging.error(f'An unexpected error occurred: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

# @item_bp.route('/swagger')
# class HelloSwagger(Resource):
#     def get(self):
#         data = json.loads(json.dumps(api.__schema__))
#         with open('yamldoc.yml', 'w') as yamlf:
#             yaml.dump(data, yamlf, allow_unicode=True, default_flow_style=False)
#             file = os.path.abspath(os.getcwd())
#             try:
#                 @after_this_request
#                 def remove_file(resp):
#                     try:
#                         os.remove(safe_join(file, 'yamldoc.yml'))
#                     except Exception as error:
#                         logging.error("Error removing or closing downloaded file handle", error)
#                     return resp
#
#                 return send_file(safe_join(file, 'yamldoc.yml'), as_attachment=True, attachment_filename='yamldoc.yml', mimetype='application/x-yaml')
#             except FileExistsError:
#                 abort(404)