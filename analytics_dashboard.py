from flask import Flask
from backend import fetch_interaction_logs

app = Flask(__name__)

@app.route("/")
def dashboard():
    logs = fetch_interaction_logs()
    html = "<h1>Voice Bot Interaction Logs</h1>"
    html += "<table border='1' cellspacing='0' cellpadding='5'><tr><th>ID</th><th>User Query</th><th>Intent</th><th>Response</th><th>Timestamp</th></tr>"
    for log in logs:
        html += f"<tr><td>{log[0]}</td><td>{log[1]}</td><td>{log[2]}</td><td>{log[3]}</td><td>{log[4]}</td></tr>"
    html += "</table>"
    return html

if __name__ == "__main__":
    app.run(debug=True, port=5001)
