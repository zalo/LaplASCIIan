from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        message = 'Hello from Python from a ZEIT Now Serverless Function!'
        self.wfile.write(message.encode())
        return