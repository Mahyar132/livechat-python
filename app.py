from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os

MESSAGES_FILE = "messages.json"

if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, "w") as f:
        json.dump({"chat": []}, f)

def load_messages():
    with open(MESSAGES_FILE, "r") as f:
        return json.load(f)

def save_messages(data):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(data, f)

class ChatServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            ua = self.headers.get("User-Agent", "").lower()
            is_mobile = any(w in ua for w in ["iphone", "android", "mobile", "ipad"])
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.render_page(is_mobile).encode("utf-8"))
        elif self.path.startswith("/messages"):
            messages = load_messages().get("chat", [])
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode("utf-8"))
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)
        name = data.get("name", [""])[0].strip()
        msg = data.get("msg", [""])[0].strip()

        if name and msg:
            messages = load_messages()
            messages["chat"].append({"name": name, "msg": msg})
            save_messages(messages)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(400)
            self.end_headers()

    def render_page(self, is_mobile):
        return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Live Chat</title>
    <style>
        body {{
            background: #222;
            color: #ddd;
            font-family: sans-serif;
            margin: 0;
            padding: 0;
            font-size: 1rem;
        }}
        #messages {{
            height: 70vh;
            overflow-y: scroll;
            padding: 10px;
        }}
        .msg {{ margin: 5px 0; }}
        .me {{ color: lightgreen; }}
        .bar {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #333;
            display: flex;
            padding: 10px;
        }}
        input[type=text] {{
            flex: 1;
            padding: 10px;
            background: #222;
            color: #ddd;
            border: none;
            font-size: 1rem;
        }}
        button {{
            background: #444;
            color: #ddd;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 1rem;
            margin-left: 5px;
        }}

        body.mobile {{
            background: #111;
            color: #eee;
            font-size: 1.4rem;
        }}
        body.mobile #messages {{
            height: 60vh;
            font-size: 1.2rem;
        }}
        body.mobile .bar {{
            padding: 15px;
        }}
        body.mobile input[type=text], body.mobile button {{
            font-size: 1.2rem;
        }}
    </style>
</head>
<body{" class='mobile'" if is_mobile else ""}>
    <div id="messages"></div>
    <div class="bar">
        <input type="text" id="input" placeholder="Type your message..." onkeydown="checkEnter(event)">
        <button onclick="send()">Send</button>
    </div>

    <script>
        let name = "";
        while (!name) name = prompt("Enter your name:");

        function loadMessages() {{
            fetch("/messages")
                .then(res => res.json())
                .then(data => {{
                    let html = "";
                    for (let m of data) {{
                        let cls = m.name === name ? "me" : "";
                        html += `<div class="msg ${{cls}}"><b>${{m.name}}:</b> ${{m.msg}}</div>`;
                    }}
                    const box = document.getElementById("messages");
                    box.innerHTML = html;
                    box.scrollTop = box.scrollHeight;
                }});
        }}

        function send() {{
            const msg = document.getElementById("input").value.trim();
            if (!msg) return;
            fetch("/", {{
                method: "POST",
                headers: {{"Content-Type": "application/x-www-form-urlencoded"}},
                body: "name=" + encodeURIComponent(name) + "&msg=" + encodeURIComponent(msg)
            }}).then(() => {{
                document.getElementById("input").value = "";
                loadMessages();
            }});
        }}

        function checkEnter(e) {{
            if (e.key === "Enter") send();
        }}

        setInterval(loadMessages, 1500);
        loadMessages();
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), ChatServer)
    print("Server running at http://localhost:8080")
    server.serve_forever()
