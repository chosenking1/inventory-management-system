# inventory-management-system


This is a Django-based Inventory Management System application.

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate


pip install django djangorestframework

python manage.py migrate

python manage.py runserver


python manage.py test