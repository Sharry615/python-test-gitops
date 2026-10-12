from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import socket
from datetime import datetime, timezone

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/health"):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error":"not found"}')
            return

        payload = {
            "application": "python-test",
            "status": "ok",
            "hostname": socket.gethostname(),
            "time_utc": datetime.now(timezone.utc).isoformat()
        }
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
