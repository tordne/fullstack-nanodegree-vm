#!/usr/bin/env python3.5

from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import pdb


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

    The Class also has several variables which contain the html
        * main_page_head :
            This contains the basic header for all the pages
        * hello_page_content :
            This contains the body for the hello pages.
    '''

    main_page_head = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>{title}</title>
    </head>
    '''


    def do_GET(self):
        '''
        do_GET method will try to search for the requested path else
        it will send a 404 error
        '''
        try:
            if self.path.endswith("/hello"):
                # Send a 200 response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"></form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>&#161Hola </h1>"
                output += '''
                <form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2>
                    <input name="message" type="text" ><input type="submit" value="Submit">
                </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()



        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        '''
        do_POST method will send a 301 response with the content retrieved
        from the form
        '''
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers['content-type'])

            # pdict['boundary'] is of string type and needs to be byte-type
            pdict['boundary'] = pdict['boundary'].encode()

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> {} </h1>".format(messagecontent[0].decode())
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output.encode())
            print(output)

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
