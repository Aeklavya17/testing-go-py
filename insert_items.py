import requests

# Define the base URL of your Flask application
base_url = 'http://localhost:5000'

# Define the endpoint for creating items
create_item_url = f'{base_url}/items/'

# Data for creating new items (replace with your actual item data)
new_items_data = [
    {'name': 'Item 1', 'description': 'Description for Item 1'},
    {'name': 'Item 2', 'description': 'Description for Item 2'},
    {'name': 'Item 3', 'description': 'Description for Item 3'},
    {'name': 'Item 4', 'description': 'Description for Item 4'},
    {'name': 'Item 5', 'description': 'Description for Item 5'},
    {'name': 'Item 6', 'description': 'Description for Item 6'},
    {'name': 'Item 7', 'description': 'Description for Item 7'},
    {'name': 'Item 8', 'description': 'Description for Item 8'},
    {'name': 'Item 9', 'description': 'Description for Item 9'},
    {'name': 'Item 10', 'description': 'Description for Item 10'}
]

# Send POST requests to create new items
for item_data in new_items_data:
    response = requests.post(create_item_url, json=item_data)
    if response.status_code == 201:
        print(f'Item created successfully: {item_data["name"]}')
    else:
        print(f'Failed to create item: {item_data["name"]}, Error: {response.text}')
