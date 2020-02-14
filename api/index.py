from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        # Attempt to read the body of the request
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length"))))

        message = 'Hello from Python from a ZEIT Now Serverless Function!   You submitted: '+str(body["gifUrl"]) +" with a density of " + body["density"]
        self.wfile.write(message.encode())
        return