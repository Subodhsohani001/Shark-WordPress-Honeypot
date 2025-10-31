# web_honeypot.py — debugged for visible logging
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request

# --------- log file & folder (absolute path so no cwd confusion) ----------
LOG_DIR = os.path.abspath("logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "http_audits.log")

# --------- formatter & logger ----------
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

funnel_logger = logging.getLogger("web_honeypot_http")
funnel_logger.setLevel(logging.INFO)
funnel_logger.propagate = False  # avoid double logging to root

# Add handlers only once (prevents duplicates with Flask reloader)
if not funnel_logger.handlers:
    # Rotating file handler (bigger file size so it doesn't rotate constantly)
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    funnel_logger.addHandler(file_handler)

    # Also add a stream handler so entries are visible in terminal immediately
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    funnel_logger.addHandler(stream_handler)

# write a startup/test entry so we know the logger is alive
funnel_logger.info("Logger initialized — startup test entry")

# --------- web honeypot ----------
def web_honeypot(input_username="admin", input_password="password"):
    # point Flask to templates dir by default; ensure templates/wp-admin-login.html exists
    app = Flask(__name__, template_folder="templates")

    @app.route("/")
    def index():
        return render_template("wp-admin-login.html")

    @app.route("/wp-admin-login", methods=["POST"])
    def login():
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        ip_address = request.remote_addr or "unknown"

        # logs credentials locally — lab use only
        funnel_logger.info(f"Client with IP Address: {ip_address} entered")
        funnel_logger.info(f"Username: {username}, Password: {password}")


        # correct comparison
        if username == input_username and password == input_password:
            funnel_logger.info(f"{ip_address} succeeded login for user={username}")
            return "DEEBOODAH!"
        else:
            funnel_logger.info(f"{ip_address} failed login for user={username}")
            return "Invalid username or password. Please Try Again."

    return app


def run_web_honeypot(port=5000, input_username="admin", input_password="password"):
    app = web_honeypot(input_username=input_username, input_password=input_password)

    # IMPORTANT: When Flask debug reloader is ON, the app module is imported twice.
    # The "if not funnel_logger.handlers" above guards against duplicate handlers.
    app.run(debug=True, port=port, host="0.0.0.0")


if __name__ == "__main__":
    run_web_honeypot(port=5000, input_username="admin", input_password="password")
