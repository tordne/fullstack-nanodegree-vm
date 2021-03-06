#!/usr/bin/env python3.5

from os import getcwd

from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

import pdb

# Create the db engine
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the Base.metadata
Base.metadata.binnd = engine

# Create the DBSession staging zone
DBSession = sessionmaker(bind=engine)
# Create a session for the DB
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    '''
    webserverHandler is a subclass of BaseHTTPRequestHandler
    The class has  2 methods added:
        * do_GET :
            This method will retrieve the path requested and
            output the HTML
        * do_POST :
            This method will post new data to the server and
            respond with the requested HTML and data

    The Class also has several class variables which contain the html
        * main_page_head :
            This contains the basic header for all the pages
        * hello_get_page_content :
            This contains the body for the hello pages
        * hello_post_page_content:
            This contains the body for the posted hello pages
    '''

    main_page_head = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>{title}</title>
      <link rel="stylesheet" type="text/css" href="/static/css/styles.css">
    </head>
    '''

    hello_get_page_content = '''
    <body>
      <header class="header">
        <div class="header-inner">
          <h2>{title}</h2>
        </div>
      </header>
      <main>
        <section class="main-inner">
          <form method='POST' enctype='multipart/form-data' action='/hello'>
            <h3>What would you like me to say?</h3>
            <input name="message" type="text" >
            <input type="submit" value="Submit">
          </form>
        </section>
      </main>
    </body>
    </html>
    '''

    hello_post_page_content = '''
    <body>
      <header class="header">
        <div class="header-inner">
          <h2>Okay, how about this:</h2>
          <h3>{message}</h3>
        </div>
      </header>
      <main>
        <section class="main-inner">
          <form method='POST' enctype='multipart/form-data' action='/hello'>
            <h3>What would you like me to say?</h3>
            <input name="message" type="text" >
            <input type="submit" value="Submit">
          </form>
        </section>
      </main>
    </body>
    </html>
    '''

    restaurant_list_content = '''
    <div>
      <h3>{restaurant_name}</h3>
      <a href="/restaurant/edit/{restaurant_id}">Edit</a>
      <a href="/restaurant/delete/{restaurant_id}">Delete</a>
    </div>
    '''

    restaurant_list_get_page_content = '''
    <body>
      <header class="header">
        <div class="header-inner">
          <h2>{title}</h2>
        </div>
      </header>
      <main>
        <section class="main-inner">
          {restaurant_list}
          <div class='create_restaurant'>
            <a href="/restaurant/new">Make a New Restaurant Here</a>
          </div>
        </section>
      </main>
    </body>
    </html>
    '''

    restaurant_new_GaP_page_content = '''
    <body>
      <header class="header">
        <div class="header-inner">
          <h2>{title}</h2>
        </div>
      </header>
      <main>
        <section class="main-inner">
          <form method='POST' enctype='multipart/form-data' action='/restaurant/new'>
            <input name="restaurant_name" type="text" >
            <input type="submit" value="Create">
          </form>
        </section>
      </main>
    </body>
    </html>
    '''

    restaurant_edit_get_page_content = '''
    <body>
      <header class="header">
        <div class="header-inner">
          <h2>{title}</h2>
        </div>
      </header>
      <main>
        <section class="main-inner">
          <h3>Rename {restaurant_name}</h3>
          <form method='POST' enctype='multipart/form-data' action='/restaurant/edit'>
            <input type="hidden" value="{restaurant_id}" name="restaurant_id">
            <input name="restaurant_name" type="text" >
            <input type="submit" value="Edit">
          </form>
        </section>
      </main>
    </body>
    </html>
    '''

    restaurant_delete_get_page_content = '''
    <body>
      <header class="header">
        <div class="header-inner">
          <h2>{title}</h2>
        </div>
      </header>
      <main>
        <section class="main-inner">
          <h3>Are you sure you want to delete {restaurant_name}</h3>
          <form method='POST' enctype='multipart/form-data' action='/restaurant/delete'>
            <input type="hidden" value="{restaurant_id}" name="restaurant_id">
            <input type="submit" value="Delete">
          </form>
        </section>
      </main>
    </body>
    </html>
    '''

    def do_GET(self):
        '''
        do_GET method will try to search for the requested path
        else it will send a 404 error
        '''
        try:
            # Try to get the CSS file
            if self.path.endswith("css"):
                # send a 200 response
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()

                # retrieve the css and put it in an output variable
                with open(getcwd() + self.path, 'r') as css_file:
                    output = css_file.read()

                # Add the output to the output stream to respond back to the
                # client
                self.wfile.write(output.encode())
                print(output)
                return

            # Try the hello path
            if self.path.endswith("/hello"):
                # Send a 200 response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Set the page_title
                page_title = 'Hello!'

                # combine all the html into 1 output variable
                output = self.main_page_head.format(title=page_title)
                output += self.hello_get_page_content.format(title=page_title)

                # Add all the output to the output stream to respond back to
                # client
                self.wfile.write(output.encode())
                print(output)
                return

            # Try the hola path
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Set the page_title
                page_title = '&#161Hola'

                # combine all the html into 1 output variable
                output = self.main_page_head.format(title=page_title)
                output += self.hello_get_page_content.format(title=page_title)

                # Add all the output to the output stream to respond back to
                # client
                self.wfile.write(output.encode())
                print(output)
                return

            # Try the Restaurant listing path
            if self.path.endswith("restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Set the page title
                page_title = 'Restaurant List'

                # Connect to the restaurant DB and query for all restaurant names
                # Place all the names in the restaurant list HTML
                full_list = ''
                for restaurant in session.query(Restaurant).order_by(
                        Restaurant.id):
                    full_list += self.restaurant_list_content.format(
                        restaurant_name=restaurant.name,
                        restaurant_id=restaurant.id)

                # Combine all the html into 1 output variable
                output = self.main_page_head.format(title=page_title)
                output += self.restaurant_list_get_page_content.format(
                    title=page_title,
                    restaurant_list=full_list)

                # Add all the output to the output stream to respond back to
                # client
                self.wfile.write(output.encode())
                print(output)
                return

            # Try the Restaurant/new path
            if self.path.endswith("restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Set the page title
                page_title = 'Create a New Restaurant'

                # combine all the html into 1 output variable
                output = self.main_page_head.format(title=page_title)
                output += self.restaurant_new_GaP_page_content.format(
                    title=page_title)

                # Add all the output to the output stream to respond back to
                # client
                self.wfile.write(output.encode())
                print(output)
                return

            # Try the Restaurant/edit path
            if self.path.startswith("/restaurant/edit/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Get restaurant ID from the path
                restaurant_id = self.path.strip('/restaurant/edit/')

                # Get the restaurant name from the DB
                for restaurant in session.query(Restaurant).filter(
                        Restaurant.id == restaurant_id):
                    restaurant_name = restaurant.name

                # Set the page title
                page_title = 'Rename {name}'.format(name=restaurant_name)

                # combine all the html into 1 output variable
                output = self.main_page_head.format(title=page_title)
                output += self.restaurant_edit_get_page_content.format(
                    title=page_title,
                    restaurant_name=restaurant_name,
                    restaurant_id=restaurant.id)

                # Add all the output to the output stream to respond back to
                # client
                self.wfile.write(output.encode())
                print(output)
                return

            # Try the Restaurant/delete path
            if self.path.startswith("/restaurant/delete/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Get restaurant ID from the path
                restaurant_id = self.path.strip('/restaurant/delete/')

                # Get the restaurant name from the DB
                for restaurant in session.query(Restaurant).filter(
                        Restaurant.id == restaurant_id):
                    restaurant_name = restaurant.name

                # Set the page title
                page_title = 'Delete {name}'.format(name=restaurant_name)

                # combine all the html into 1 output variable
                output = self.main_page_head.format(title=page_title)
                output += self.restaurant_delete_get_page_content.format(
                    title=page_title,
                    restaurant_name=restaurant_name,
                    restaurant_id=restaurant.id)

                # Add all the output to the output stream to respond back to
                # client
                self.wfile.write(output.encode())
                print(output)
                return

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        '''
        do_POST method will send a 301 response with the content retrieved
        from the form
        '''
        try:
            if self.path.endswith("hello"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Parse a MIME header and save the content-type values in ctype and
                # pdict
                ctype, pdict = cgi.parse_header(
                    self.headers['content-type'])

                # encode the boundary into a byte-type
                pdict['boundary'] = pdict['boundary'].encode()

                # Check if the Content-type is a multipart,
                # then parse it according to the boundary and extract the message
                # data
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                # Set the page_title
                page_title = 'Hello!'

                # combine all the html into 1 output variable
                output = self.main_page_head.format(title=page_title)
                output += self.hello_post_page_content.format(
                    message=messagecontent[0].decode())

                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("restaurant/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

                # Parse a MIME header and save the content-type values in ctype and
                # pdict
                ctype, pdict = cgi.parse_header(
                    self.headers['content-type'])

                # encode the boundary into a byte-type
                pdict['boundary'] = pdict['boundary'].encode()

                # Check if the Content-type is a multipart,
                # then parse it according to the boundary, extract the name
                # and add it to the DB using SQLAlchemy
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('restaurant_name')

                    # add the new restaurant
                    session.add(Restaurant(name=name[0].decode()))
                    session.commit()
                return

            if self.path.endswith("restaurant/delete"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

                # Parse a MIME header and save the content-type values in ctype and
                # pdict
                ctype, pdict = cgi.parse_header(
                    self.headers['content-type'])

                # encode the boundary into a byte-type
                pdict['boundary'] = pdict['boundary'].encode()

                # Check if the Content-type is a multipart,
                # then parse it according to the boundary, extract the name
                # and add it to the DB using SQLAlchemy
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_id = fields.get('restaurant_id')[0].decode()

                    restaurant = session.query(Restaurant).filter(
                        Restaurant.id == restaurant_id).one()

                    # Delete the restaurant
                    session.delete(restaurant)
                    session.commit()
                return

            if self.path.endswith("restaurant/edit"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

                # Parse a MIME header and save the content-type values in ctype and
                # pdict
                ctype, pdict = cgi.parse_header(
                    self.headers['content-type'])

                # encode the boundary into a byte-type
                pdict['boundary'] = pdict['boundary'].encode()

                # Check if the Content-type is a multipart,
                # then parse it according to the boundary, extract the name
                # and add it to the DB using SQLAlchemy
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_id = fields.get('restaurant_id')[0].decode()
                    restaurant_name = fields.get('restaurant_name')[0].decode()

                    restaurant = session.query(Restaurant).filter(
                        Restaurant.id == restaurant_id).one()

                    # Update the restaurants name
                    restaurant.name = restaurant_name
                    session.commit()
                return

        except:
            pass


def main():
    '''
    Start a HTTPServer on port 8080
    and let the server run forever
    Untill there is a KeyboardInterrupt by ^C
    '''
    try:
        port = 8080

        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
