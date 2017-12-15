from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import pdb

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
    page_title = "List of Restaurants"
    restaurant = session.query(Restaurant).all()
    return render_template(
        "restaurants.html",
        title=page_title,
        restaurant=restaurant
    )


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def restaurantNew():
    if request.method == 'POST':
        restaurant = Restaurant(
            name=request.form['name'])
        session.add(restaurant)
        session.commit()
        return redirect(url_for('restaurantList'))
    return render_template("restaurants_new.html")


@app.route('/restaurants/edit/<int:restaurant_id>/', methods=['GET', 'POST'])
def restaurantEdit(restaurant_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    page_title = "Rename " + restaurant.name
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('restaurantList'))
    return render_template(
        "restaurants_edit.html",
        title=page_title,
        restaurant=restaurant)


@app.route('/restaurants/delete/<int:restaurant_id>/', methods=['GET', 'POST'])
def restaurantDelete(restaurant_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    page_title = "Delete " + restaurant.name
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('restaurantList'))
    return render_template(
        "restaurants_delete.html",
        title=page_title,
        restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def menuList(restaurant_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    page_title = restaurant.name + " Menu"
    return render_template(
        "menu.html",
        title=page_title,
        restaurant=restaurant,
        items=restaurant.menu_items)


@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def menuItemNew(restaurant_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    page_title = "Create New Menu Item for " + restaurant.name
    if request.method == 'POST':
        item = MenuItem(
            name=request.form['name'],
            course=request.form['course'],
            description=request.form['description'],
            price=request.form['price'],
            restaurant_id=restaurant.id
            )
        session.add(item)
        session.commit()
        return redirect(url_for('menuList', restaurant_id=restaurant.id))
    return render_template(
        "menu_item_new.html",
        title=page_title,
        restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/edit/<int:menu_id>')
def menuItemEdit(restaurant_id, menu_id):
    query = session.query(Restaurant, MenuItem).join(MenuItem).filter(MenuItem.id == menu_id).one()
    page_title = "Edit Menu Item: " + query.MenuItem.name
    return render_template(
        "menu_item_edit.html",
        title=page_title,
        restaurant=query.Restaurant,
        item=query.MenuItem)


@app.route('/restaurants/<int:restaurant_id>/menu/delete/<int:menu_id>')
def menuItemDelete(restaurant_id, menu_id):
    query = session.query(Restaurant, MenuItem).join(MenuItem).filter(MenuItem.id == menu_id).one()
    page_title = "Delete Menu Item: " + query.MenuItem.name
    return render_template(
        "menu_item_delete.html",
        title=page_title,
        restaurant=query.Restaurant,
        item=query.MenuItem)


if __name__ == '__main__':
    # Debug the application
    app.debug = True
    # Run the server
    app.run(host='0.0.0.0', port=5000)
