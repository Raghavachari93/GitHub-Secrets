cat > app.py <<'PY' 
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Project 6 - secured with GitHub Secrets!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
PY

