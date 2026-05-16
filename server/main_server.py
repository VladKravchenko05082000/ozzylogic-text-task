import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from configs.routes import ROUTES

log = logging.getLogger(__name__)

def _normalized_headers(raw_headers) -> dict:
    return {k.lower(): v for k, v in raw_headers.items()}

class APIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self._dispatch("GET")

    def do_POST(self):
        self._dispatch("POST")

    def do_PATCH(self):
        self._dispatch("PATCH")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*") #We can change this to our client domain
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def _dispatch(self, method: str) -> None:
        parsed = urlparse(self.path)
        query = {
            k: (v[0] if len(v) == 1 else v)
            for k, v in parse_qs(parsed.query).items()
        }

        body = {}
        if method in ("POST", "PATCH", "PUT"):
            length = int(self.headers.get("Content-Length", 0) or 0)
            if length > 0:
                try:
                    body = json.loads(self.rfile.read(length).decode("utf-8"))
                    if not isinstance(body, dict):
                        return self._respond(400, {"error": "body must be a JSON object"})
                except (json.JSONDecodeError, UnicodeDecodeError):
                    return self._respond(400, {"error": "invalid JSON body"})

        for route_method, pattern, handler in ROUTES:
            if route_method != method:
                continue
            m = pattern.match(parsed.path)
            if not m:
                continue

            try:
                result = handler(query=query, body=body, headers=_normalized_headers(self.headers), **m.groupdict())
                status = result.get("status")
                response = result.get("response", {})
            except ValueError as e:
                status, response = 400, {"error": str(e)}
            except Exception:
                log.exception("Handler error on %s %s", method, parsed.path)
                status, response = 500, {"error": "internal server error"}

            return self._respond(status, response)

        self._respond(404, {"error": "not found"})

    def _respond(self, status: int, response: dict):
        payload = json.dumps(response, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*") #We can change this to our client domain
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
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