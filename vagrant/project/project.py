from flask import Flask, render_template, redirect, \
    url_for, request, flash, jsonify
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


# Making an API Endpoint for full JSON menu
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# Making an API Endpoint for single JSON menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def MenuItemJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(
        id=menu_id).one()
    return jsonify(MenuItem=[item.serialize])


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id)
    return render_template(
        'menu.html',
        page_title=restaurant.name,
        restaurant=restaurant,
        items=items
    )


# Create a new Menu Item
@app.route('/restaurants/<int:restaurant_id>/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            restaurant_id=restaurant_id
        )
        session.add(newItem)
        session.commit()
        flash("New menu item: {name} created.".format(name=newItem.name))
        return redirect(url_for(
            'restaurantMenu',
            restaurant_id=restaurant_id
        ))
    else:
        return render_template(
            'newmenuitem.html',
            page_title="Create a new item for " + restaurant.name,
            restaurant=restaurant
        )


# Edit a Menu Item
@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(
        id=menu_id).one()
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            menuitem.name = request.form['name']
            session.add(menuitem)
            session.commit()
            flash("Menu Item: {name} is edited".format(name=menuitem.name))
        return redirect(url_for(
            'restaurantMenu',
            restaurant_id=restaurant_id
        ))
    else:
        return render_template(
            'editmenuitem.html',
            page_title="Edit " + menuitem.name + " from " + restaurant.name,
            restaurant=restaurant,
            menuitem=menuitem
        )


# Delete a Menu Item
@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(
        id=menu_id).one()
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(menuitem)
        session.commit()
        flash("Menu Item: {name} is deleted.".format(name=menuitem.name))
        return redirect(url_for(
            'restaurantMenu',
            restaurant_id=restaurant_id
        ))
    else:
        return render_template(
            'deletemenuitem.html',
            page_title="Are you sure you want to delete " + menuitem.name,
            restaurant=restaurant,
            menuitem=menuitem
        )


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
