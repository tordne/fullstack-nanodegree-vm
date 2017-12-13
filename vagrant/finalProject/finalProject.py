from flask import Flask

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create an engine connecting to the DB
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the tables metadata to the engine
Base.metadata.bind = engine

# Create a staging zone with the engine
DBSession = sessionmaker(bind=engine)
# Create a session connecting to the staging zone
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def restaurantList():
	return "List of restaurants"


@app.route('/restaurants/new/')
def restaurantNew():
	return "Add a New Restaurant"


@app.route('/restaurants/edit/<int:restaurant_id>/')
def restaurantEdit():
	return "Edit a Restaurant"

@app.route('/restaurants/delete/<int:restaurant_id>/')
def restaurantDelete():
	return "Delete a Restaurant"


@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def menuList():
	return "List of the Menu"


@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def menuItemNew():
	return "Add a New Menu Item"


@app.route('/restaurants/<int:restaurant_id>/menu/edit/<int:menu_id>')
def menuItemEdit():
	return "Edit a Menu Item"


@app.route('/restaurants/<int:restaurant_id>/menu/delete/<int:menu_id>')
def menuItemDelete():
	return "Delete a Menu Item"


if __name__ == '__main__':
    # Debug the application
    app.debug = True
    # Run the server
    app.run(host='0.0.0.0', port=5000)
