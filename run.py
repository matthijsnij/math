"""Entry point: `python run.py` starts the local Flask server.

Reachable from a phone on the same local network (e.g. phone hotspot
tethering the laptop) via http://<this-machine's-LAN-IP>:5000 — see README.md.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
