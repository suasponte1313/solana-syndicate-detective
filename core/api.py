import os
import json
import urllib.parse
from http.server import SimpleHTTPRequestHandler
from core.investigator import INVESTIGATOR
from core.supabase_bridge import BRIDGE

UI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui")

class DetectiveHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/board":
            self.send_json(INVESTIGATOR.get_crime_board_data())
            return

        elif path == "/api/unravel":
            query = urllib.parse.parse_qs(parsed.query)
            addr = query.get("address", [""])[0]
            if not addr:
                self.send_json({"error": "Missing address parameter"}, 400)
                return
            res = INVESTIGATOR.unravel_wallet(addr)
            self.send_json(res)
            return

        elif path == "/api/sql":
            sql = BRIDGE.export_sql_migration()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(sql)))
            self.end_headers()
            self.wfile.write(sql.encode("utf-8"))
            return

        elif path == "/":
            self.path = "/index.html"
            return super().do_GET()
        else:
            return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/sync_supabase":
            res = BRIDGE.sync_to_supabase()
            self.send_json(res)
            return
        else:
            self.send_error(404, "Unknown API Route")

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.end_headers()
        self.wfile.write(body)
