import json
import time
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        try:
            requested = float(params.get("seconds", ["140"])[0])
        except (TypeError, ValueError):
            requested = 140.0

        if requested < 0:
            requested = 0.0

        start = time.time()
        time.sleep(requested)
        elapsed = time.time() - start

        body = json.dumps({"requested": requested, "elapsed": elapsed}).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
