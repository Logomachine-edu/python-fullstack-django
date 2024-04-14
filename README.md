# Demo Shop LOGO

### Tech Stack: 
- Python 3.12
- Django 5
- SQLite 3

#### Prepare virtual environment:
```shell
python -m pip install poetry
poetry install
```

#### Prepare app for usage
```shell
python manage.py migrate  # Run migrations into database
python manage.py createsuperuser  # Create admin to log in admin panel
python manage.py loaddata fixtures.json  # Load initial data into database
```

#### Run app
```shell
python manage.py runserver
```

### Suggest application features:
#### Example for Demo Shop LOGO:

- Landing with featured items
- Catalog, displaying items in order by cost
- Add any item to cart
- Display cart for every client individually
