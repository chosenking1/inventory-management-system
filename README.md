
# Inventory Management System

This is a Django-based Inventory Management System application.

## Installation

**Prerequisites:**

* Python 3.x

**Steps:**

1. **Create a virtual environment:**
    * Windows: `python -m venv venv`
    * macOS/Linux: `python3 -m venv venv`
2. **Activate the virtual environment:**
    * Windows: `venv\Scripts\activate`
    * macOS/Linux: `source venv/bin/activate`
3. **Install dependencies:**
   ```bash
   pip install django djangorestframework
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

1. **Login**
   - **Endpoint:** `api/login/`
   - **Method:** POST
   - **Description:** Log in a user and obtain an authentication token.
   - **Request Body:**
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```

2. **Signup**
   - **Endpoint:** `api/signup/`
   - **Method:** POST
   - **Description:** Register a new user.
   - **Request Body:**
     ```json
     {
       "username": "your_username",
       "password": "your_password",
       "email": "your_email"
     }
     ```

3. **Test Token**
   - **Endpoint:** `api/test_token/`
   - **Method:** GET
   - **Description:** Verify if the provided token is valid.
   - **Headers:**
     ```json
     {
       "Authorization": "Bearer your_token"
     }
     ```

4. **Logout**
   - **Endpoint:** `api/logout/`
   - **Method:** POST
   - **Description:** Log out the currently authenticated user.
   - **Headers:**
     ```json
     {
       "Authorization": "Bearer your_token"
     }
     ```

### Products

5. **Product List**
   - **Endpoint:** `api/products/`
   - **Method:** GET
   - **Description:** Retrieve a list of all products.

6. **Product Detail**
   - **Endpoint:** `api/products/{pk}/`
   - **Method:** GET
   - **Description:** Retrieve details of a specific product.
   - **URL Parameters:**
     - `pk`: ID of the product

### Orders

7. **Order List**
   - **Endpoint:** `api/orders/`
   - **Method:** GET
   - **Description:** Retrieve a list of all orders.

8. **Order Detail**
   - **Endpoint:** `api/orders/{pk}/`
   - **Method:** GET
   - **Description:** Retrieve details of a specific order.
   - **URL Parameters:**
     - `pk`: ID of the order

9. **Update Order Status**
   - **Endpoint:** `api/orders/{pk}/update_status/`
   - **Method:** PATCH
   - **Description:** Update the status of a specific order (admin only).
   - **URL Parameters:**
     - `pk`: ID of the order
   - **Request Body:**
     ```json
     {
       "status": "new_status"
     }
     ```
   - **Headers:**
     ```json
     {
       "Authorization": "Bearer your_token"
     }
     ```

### Reports

10. **Low Stock Products**
    - **Endpoint:** `api/low-stock-products/`
    - **Method:** GET
    - **Description:** Retrieve a list of products with low stock (admin only).
    - **Headers:**
      ```json
      {
        "Authorization": "Bearer your_token"
      }
      ```

11. **Sales Report**
    - **Endpoint:** `api/sales-report/{period}/`
    - **Method:** GET
    - **Description:** Retrieve a sales report for a specified period (admin only).
    - **URL Parameters:**
      - `period`: `day`, `week`, or `month`
    - **Headers:**
      ```json
      {
        "Authorization": "Bearer your_token"
      }
      ```

### Admin Panel

12. **Django Admin**
    - **Endpoint:** `admin/`
    - **Method:** GET
    - **Description:** Access the Django admin panel for managing the application.
    - **Note:** Requires admin login.

## Testing

Run tests with:

```bash
python manage.py test
```

With these instructions, you should be able to set up, run, and interact with the provided API endpoints in your Inventory Management System.