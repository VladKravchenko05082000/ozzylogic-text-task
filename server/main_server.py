import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from configs.routes import ROUTES

class APIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self._dispatch("GET")

    def _dispatch(self, method: str) -> None:
        parsed = urlparse(self.path)
        query = {
            k: (v[0] if len(v) == 1 else v)
            for k, v in parse_qs(parsed.query).items()
        }

        for route_method, pattern, handler in ROUTES:
            if route_method != method:
                continue
            m = pattern.match(parsed.path)
            if not m:
                continue

            result = handler(query=query, **m.groupdict())
            status = result.get("status")
            response = result.get("response", {})
            return self._respond(status, response)

        self._respond(404, {"error": "not found"})

    def _respond(self, status: int, response: dict):
        payload = json.dumps(response, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def run(host: str, port: int):
    server = ThreadingHTTPServer((host, port), APIHandler)
    print(f"Listening on {host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.shutdown()