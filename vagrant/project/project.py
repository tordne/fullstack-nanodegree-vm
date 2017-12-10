from flask import Flask, render_template, url_for
app = Flask(
    __name__
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create the DB engine
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the Base.metadata
Base.metadata.bind = engine

# Create the DBSession staging zone
DBSession = sessionmaker(bind=engine)
# Create a session for the DB
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# Create a new Menu Item
@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"


# Edit a Menu Item
@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


# Delete a Menu Item
@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
