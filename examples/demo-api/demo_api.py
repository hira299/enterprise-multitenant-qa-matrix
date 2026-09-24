"""A small fictional multi-tenant ordering API with deliberate defects.

It exists to practise and demonstrate matrix-driven testing. Two tenants
(acme, globex) each have an admin, a manager, a field agent, and a viewer.
Tokens are fixed strings so tests are reproducible. Standard library only.

Deliberate defects (see README.md in this folder):
  D1  another tenant's order returns 403 instead of 404 (existence leak)
  D2  a manager can submit proof of delivery for a delivery assigned to an agent
  D3  a deactivated user's token still works
  D4  a payment larger than the outstanding balance is accepted
  D5  the viewer role can approve orders through the API (the UI hides the button)

Run: python3 demo_api.py [port]    (default 8099, binds 127.0.0.1)
"""

import copy
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

USERS = {
    "acme-admin": {"tenant": "acme", "role": "admin", "active": True},
    "acme-manager": {"tenant": "acme", "role": "manager", "active": True},
    "acme-agent": {"tenant": "acme", "role": "agent", "active": True},
    "acme-agent-2": {"tenant": "acme", "role": "agent", "active": True},
    "acme-viewer": {"tenant": "acme", "role": "viewer", "active": True},
    "acme-deactivated": {"tenant": "acme", "role": "manager", "active": False},
    "globex-admin": {"tenant": "globex", "role": "admin", "active": True},
    "globex-manager": {"tenant": "globex", "role": "manager", "active": True},
}

SEED = {
    "orders": {
        "A-100": {"tenant": "acme", "status": "submitted", "total": 500.0},
        "G-200": {"tenant": "globex", "status": "submitted", "total": 900.0},
    },
    "deliveries": {
        "DL-1": {"tenant": "acme", "order": "A-100", "agent": "acme-agent", "proof": None},
    },
    "invoices": {
        "INV-1": {"tenant": "acme", "total": 500.0, "paid": 0.0},
        "INV-2": {"tenant": "globex", "total": 900.0, "paid": 0.0},
    },
}
DB = copy.deepcopy(SEED)


class Handler(BaseHTTPRequestHandler):
    server_version = "demo-api"

    def log_message(self, *args):
        pass

    def send(self, code, body=None):
        data = json.dumps(body if body is not None else {}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def user(self):
        auth = self.headers.get("Authorization", "")
        token = auth[7:] if auth.startswith("Bearer ") else None
        user = USERS.get(token)
        # D3: account state is never checked, so deactivated tokens keep working.
        return (token, user) if user else (None, None)

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return None

    def do_GET(self):
        self.route("GET")

    def do_POST(self):
        self.route("POST")

    def route(self, method):
        global DB
        path = self.path.split("?")[0]
        if method == "POST" and path == "/__reset":
            DB = copy.deepcopy(SEED)
            return self.send(200, {"reset": True})
        if method == "GET" and path == "/health":
            return self.send(200, {"ok": True})

        token, user = self.user()
        if not user:
            return self.send(401, {"error": "authentication required"})
        tenant, role = user["tenant"], user["role"]

        if method == "GET" and path == "/api/orders":
            return self.send(200, [dict(id=k, **v) for k, v in DB["orders"].items() if v["tenant"] == tenant])

        m = re.fullmatch(r"/api/orders/([\w-]+)", path)
        if method == "GET" and m:
            order = DB["orders"].get(m.group(1))
            if not order:
                return self.send(404, {"error": "not found"})
            if order["tenant"] != tenant:
                return self.send(403, {"error": "forbidden"})  # D1: should be 404
            return self.send(200, dict(id=m.group(1), **order))

        if method == "POST" and path == "/api/orders":
            if role not in ("admin", "manager"):
                return self.send(403, {"error": "forbidden"})
            b = self.body()
            if not b or not isinstance(b.get("total"), (int, float)) or b["total"] <= 0:
                return self.send(400, {"error": "total must be a positive number"})
            oid = f"A-{100 + len(DB['orders'])}"
            DB["orders"][oid] = {"tenant": tenant, "status": "submitted", "total": float(b["total"])}
            return self.send(201, {"id": oid})

        m = re.fullmatch(r"/api/orders/([\w-]+)/approve", path)
        if method == "POST" and m:
            order = DB["orders"].get(m.group(1))
            if not order or order["tenant"] != tenant:
                return self.send(404, {"error": "not found"})
            if role not in ("admin", "manager", "viewer"):  # D5: viewer should not be here
                return self.send(403, {"error": "forbidden"})
            if order["status"] != "submitted":
                return self.send(409, {"error": f"cannot approve an order that is {order['status']}"})
            order["status"] = "approved"
            return self.send(200, {"id": m.group(1), "status": "approved"})

        m = re.fullmatch(r"/api/deliveries/([\w-]+)/proof", path)
        if method == "POST" and m:
            d = DB["deliveries"].get(m.group(1))
            if not d or d["tenant"] != tenant:
                return self.send(404, {"error": "not found"})
            # D2: checks "staff of this tenant" instead of "the assigned agent".
            if role not in ("agent", "manager") or (role == "agent" and d["agent"] != token):
                return self.send(403, {"error": "forbidden"})
            d["proof"] = {"by": token}
            return self.send(200, {"id": m.group(1), "proof": "recorded"})

        m = re.fullmatch(r"/api/invoices/([\w-]+)", path)
        if method == "GET" and m:
            inv = DB["invoices"].get(m.group(1))
            if not inv or inv["tenant"] != tenant:
                return self.send(404, {"error": "not found"})
            return self.send(200, dict(id=m.group(1), outstanding=round(inv["total"] - inv["paid"], 2), **inv))

        m = re.fullmatch(r"/api/invoices/([\w-]+)/payments", path)
        if method == "POST" and m:
            inv = DB["invoices"].get(m.group(1))
            if not inv or inv["tenant"] != tenant:
                return self.send(404, {"error": "not found"})
            if role != "admin":
                return self.send(403, {"error": "forbidden"})
            b = self.body()
            if not b or not isinstance(b.get("amount"), (int, float)) or b["amount"] <= 0:
                return self.send(400, {"error": "amount must be a positive number"})
            inv["paid"] = round(inv["paid"] + b["amount"], 2)  # D4: no check against the outstanding balance
            return self.send(201, {"invoice": m.group(1), "paid": inv["paid"]})

        return self.send(404, {"error": "not found"})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8099
    print(f"demo API on http://127.0.0.1:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
