import re



ROUTES = [
    ("GET", re.compile(r"^/api/health/?$"), lambda **_: ({"status":200, "response":{"status": "ok"}})),
]