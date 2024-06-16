# Online Store Inventory and Supplier Management API

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Duade10/ims.git
    cd ims
    ```

2. Install dependencies:
    ```sh
    pipenv/pip install -r requirements.txt
    ```

3. Apply migrations:
    ```sh
    python manage.py migrate
    ```

4. Run the development server:
    ```sh
    python manage.py runserver
    ```

## API Endpoints
### Users
- POST `/api/users/register` - Register a new user
- POST `/api/users/token` - Get the user's tokens ['access' and 'refresh']
- POST `/api/users/token/refresh` - Get a new access token

### Suppliers
- GET `/api/suppliers/` - List all suppliers
- POST `/api/suppliers/` - Create a new supplier
- GET `/api/suppliers/<id>/` - Retrieve a specific supplier
- PUT `/api/suppliers/<id>/` - Update a specific supplier
- DELETE `/api/suppliers/<id>/` - Delete a specific supplier
- GET `api/suppliers/<id>/items/` - Get all items related to suppliers

### Inventory Items
- GET `/api/inventory-items/` - List all inventory items
- POST `/api/inventory-items/` - Create a new inventory item
- GET `/api/inventory-items/<id>/` - Retrieve a specific inventory item
- PUT `/api/inventory-items/<id>/` - Update a specific inventory item
- DELETE `/api/inventory-items/<id>/` - Delete a specific inventory item
- GET `/api/inventory-items/<id>/suppliers` - Get all inventory item suppliers

## Testing

To run tests:
```sh
python manage.py test
