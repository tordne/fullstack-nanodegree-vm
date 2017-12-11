from flask import Flask, render_template, redirect, url_for, request
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
@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
