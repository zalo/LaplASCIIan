from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

  def do_POST(self):


    message = "Conversion Failed for mysterious reasons... try something different?"
    try:
      # Attempt to read the body of the request
      body = json.loads(self.rfile.read(int(self.headers.get("Content-Length"))).decode("utf-8"))

      # Construct a Reponse
      message = 'Hello from Python from a ZEIT Now Serverless Function!   You submitted: ' + str(body)  # +" with a density of " + body["density"]
      
      self.send_response(200)
      self.send_header('Content-type','text/plain')
      self.end_headers()
    except Exception as e:
      message = "Conversion Failed; Error ({0}): {1}".format(e.errno, e.strerror)

      self.send_response(400)
    finally:
      self.wfile.write(message.encode())

    return