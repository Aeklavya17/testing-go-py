from app.models import Item
from app.db.database import get_db

db = get_db()

class ItemService:

    @staticmethod
    def get_all_items():
        return Item.query.all()

    @staticmethod
    def get_item_by_id(item_id):
        """
        Get item by id
        :param item_id:
        :return: Item Details
        """
        return Item.query.get(item_id)

    @staticmethod
    def create_item(data):
        new_item = Item(name=data['name'], description=data.get('description', ""))
        db.session.add(new_item)
        db.session.commit()
        return new_item

    @staticmethod
    def update_item(item, data):
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        db.session.commit()
        return item

    @staticmethod
    def delete_item(item):
        db.session.delete(item)
        db.session.commit()
