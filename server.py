#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 8421
DIRECTORY = os.path.expanduser("~/satory-us")

class PortalHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        clean = self.path.split('?')[0].rstrip('/')
        if clean == "/api/gateway":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"ok": true, "status": "running"}')
            return
        return super().do_GET()

    def translate_path(self, path):
        clean = path.split('?')[0].rstrip('/')
        if clean == "" or clean == "/portal":
            path = "/portal.html"
        elif clean == "/fridge":
            path = "/fridge.html"
        elif clean == "/family":
            path = "/family.html"
        elif clean == "/weight":
            path = "/weight.html"
        return super().translate_path(path)

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), PortalHandler) as httpd:
        print(f"Portal serving on http://127.0.0.1:{PORT}")
        httpd.serve_forever()
