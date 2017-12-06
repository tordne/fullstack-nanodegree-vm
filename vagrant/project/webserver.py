from http.server import HTTPServer, BaseHTTPRequestHandler


class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "".encode()
                output += "<html><body>Hello!</body></html>".encode()
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "".encode()
                output += "<html><body>&#161Hola <a href = '/hello'>Back to Hello \
                </a></body></html>".encode()
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))


def main():
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
